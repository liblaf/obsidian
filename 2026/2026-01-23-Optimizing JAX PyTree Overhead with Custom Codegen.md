---
date: 2026-01-23T17:00:44+08:00
modified: 2026-01-23T17:28:01+08:00
title: Optimizing JAX PyTree Overhead with Custom Codegen
---

JAX is famous for its compilation speedups, but often we forget that the Python "glue" code surrounding our JIT-compiled kernels still runs in the Python interpreter. When working with complex PyTrees (nested classes, models, or state objects), the overhead of flattening and unflattening these trees can become a silent bottleneck.

If your JIT-ed kernel takes 50ms, a 2µs Python overhead is negligible. But if your kernel takes **50µs**, that same overhead starts to eat into your throughput. In tight loops (like RL environments or ODE solvers), this adds up fast.

I benchmarked five different ways to define PyTrees in JAX to see how much overhead each introduces. The results were surprising: **custom bytecode generation is nearly 10x faster than standard library tools.**

## The Benchmarks

Here is the breakdown of the time it takes to `flatten` (convert object to arrays) and `unflatten` (reconstruct object from arrays) a simple class with 7 data fields and 3 static fields.

|                   Method                   |   Flatten    |  Unflatten   | Notes                               |
| :----------------------------------------: | :----------: | :----------: | ----------------------------------- |
|          **my codegen + `attrs`**          | **~0.29 µs** | **~0.18 µs** | **🚀 Fastest.**                     |
|     `jtu.register_dataclass` + `attrs`     |   ~0.64 µs   |   ~1.04 µs   | Fast C++ flatten.                   |
|   `jtu.register_dataclass` + `dataclass`   |   ~0.64 µs   |   ~1.16 µs   | Fast C++ flatten.                   |
|       manual registeration + `attrs`       |   ~1.60 µs   |   ~2.01 µs   | Standard Python iteration overhead. |
|              `equinox.Module`              |   ~2.16 µs   |   ~1.87 µs   | Safe codegen with dynamic overhead. |
| `jtu.register_dataclass` + slow `__init__` |   ~0.67 µs   | **~1000 µs** | ⚠️ The trap of native JAX support.  |

### The "Slow Init" Trap

You might notice the terrible performance in the last row. JAX's native `register_dataclass` is generally fast because it uses C++ bindings for flattening. However, for unflattening, **it calls the class constructor (`__init__`)**.

If your class has heavy logic in `__init__`, validators, or slow converters (like the benchmark example below), JAX executes that logic **every time** it reconstructs the tree.

```python
def _slow_converter(x: Any) -> int:
    time.sleep(0.001) # simulating heavy validation/conversion
    return x

@attrs.define
class A:
    # this kills performance during jax.jit boundaries
    g: int = attrs.field(default=0, converter=_slow_converter) 
```

## The Solution: Custom Code Generation

To achieve sub-microsecond performance (~180ns unflatten), we need to do two things:
1. **Unroll loops:** Avoid iterating over field names in Python.
2. **Bypass `__init__`:** Directly allocate memory and set slots, ignoring converters and validators during JAX internal operations.

The fastest approach involves generating Python source code strings at runtime, compiling them with `compile()`, and loading them with `exec()`.

### How It Works

Instead of using `getattr` in a loop, we generate a function that looks exactly like hard-coded Python.

**Generated Flatten Code:**

```python
def tree_flatten(obj: _cls) -> tuple[tuple, tuple]:
    # direct attribute access, no loops
    return (obj.a, obj.b, obj.c, obj.d, obj.e, obj.f, obj.g,), (obj.h, obj.i, obj.j,)
```

**Generated Unflatten Code:**
Even more importantly, the unflatten function uses `object.__new__` to skip initialization logic:

```python
def tree_unflatten(aux: tuple, children: tuple) -> _cls:
    # bypass __init__ completely
    obj = _object_new(_cls) 
    # direct slot setting
    _object_setattr(obj, "h", aux[0])
    _object_setattr(obj, "i", aux[1])
    # ... (rest of fields)
    _object_setattr(obj, "g", children[6])
    return obj
```

### Implementing the Codegen

Here is the core logic for the code generator. It constructs the source code string and executes it into a namespace.

```python
import types

def codegen(
    cls: type, data_fields: Sequence[str], meta_fields: Sequence[str]
) -> tuple[Callable, Callable, Callable]:
    # 1. generate the source code as a string
    source: str = _codegen_tree(data_fields, meta_fields)
    
    # 2. compile into a code object
    filename = f"<generated {cls.__qualname__}>"
    code: types.CodeType = compile(source, filename, "exec")
    
    # 3. prepare namespace with required optimized builtins
    namespace: dict[str, Any] = {
        "_cls": cls,
        "_object_new": object.__new__,       # Speed optimization
        "_object_setattr": object.__setattr__, # Speed optimization
    }
    
    # 4. execute to define functions
    exec(code, namespace)
    
    return namespace["tree_flatten"], namespace["tree_flatten_with_keys"], namespace["tree_unflatten"]
```

The string construction logic (`_codegen_tree`) simply iterates over your fields once during registration to build the strings.

```python
def _codegen_tree_unflatten(data: Sequence[str], meta: Sequence[str]) -> str:
    lines = []
    # hardcode the assignment for every field
    for i, name in enumerate(meta):
        lines.append(f'_object_setattr(obj, "{name}", aux[{i}])')
    for i, name in enumerate(data):
        lines.append(f'_object_setattr(obj, "{name}", children[{i}])')
        
    body = "\n    ".join(lines)
    return f"""
def tree_unflatten(aux: tuple, children: tuple) -> _cls:
    obj = _object_new(_cls)
    {body}
    return obj
"""
```

## Why Equinox is Slower (Despite using Codegen)

Equinox is an excellent library that provides safe, filtered state management. Like the solution above, it **also uses runtime code generation**. However, the benchmarks show it is roughly 7x slower (~2.07µs vs ~0.29µs) than the bare-metal approach.

Looking at the generated source code for Equinox reveals why. Equinox prioritizes **correctness and dynamism** over raw speed.

**1. Dictionary Lookups vs. Direct Access:**
Equinox generates code that looks like this:

```python
get = obj.__dict__.get
# ...
val = get('field_name', MISSING)
```

Accessing `__dict__` and using `.get()` is significantly slower than direct attribute access (`obj.field`).

**2. Safety Checks (Branching):**
The unflatten code generated by Equinox includes safety branches to handle missing fields:

```python
if data[i] is not MISSING:
	object.__setattr__(self, 'field_name', data[i])
```

The "bare metal" codegen assumes a rigid structure and performs blind assignments. CPU branch prediction handles the linear execution of the bare metal code much better than the conditional logic in Equinox.

**3. Metadata Overhead:**
Equinox preserves wrapper fields (`__module__`, `__doc__`, etc.) during flattening/unflattening. While this ensures the object is perfectly reconstructed, it adds extra cycles that are often unnecessary for pure numerical computation loops.

## Conclusion

If you are writing high-performance JAX code where the kernel execution time is short (e.g., custom physics engines, environments, or complex control loops), Python overhead matters.

1. **Avoid `jax.register_dataclass`** if your class has heavy `__init__` logic or converters.
2. **Use Custom "Bare Metal" Codegen** to unroll loops, bypass initialization, and skip safety checks.
3. **Result:** You get the safety of Python classes with the serialization speed of raw tuples.

This technique reduces the Python-scope overhead from microseconds to nanoseconds, keeping your GPU hungry and your wait times low.

## Appendix

### Environments

```
python==3.13.11
attrs==25.4.0
equinox==0.13.2
jax==0.8.2
```

### Codegen + `attrs`

```python
import linecache
import textwrap
import timeit
import types
from collections.abc import Callable, Iterable, Sequence
from typing import Any

import attrs
import jax
import jax.tree_util as jtu

type KeyEntry = Any
type Leaf = Any
type PyTreeDef = Any


@attrs.define
class A:
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    e: int = 0
    f: int = 0
    g: int = 0
    h: int = attrs.field(default=0, metadata={"static": True})
    i: int = attrs.field(default=0, metadata={"static": True})
    j: int = attrs.field(default=0, metadata={"static": True})


def codegen(
    cls: type, data_fields: Sequence[str], meta_fields: Sequence[str]
) -> tuple[Callable, Callable, Callable]:
    filename: str = _make_filename(cls)
    source: str = _codegen_tree(data_fields, meta_fields)
    code: types.CodeType = compile(source, filename, "exec")
    namespace: dict[str, Any] = {
        "_cls": cls,
        "_object_new": object.__new__,
        "_object_setattr": object.__setattr__,
        **_make_key_entries(data_fields),
    }
    exec(code, namespace)  # noqa: S102
    _update_linecache(source, filename)
    flatten: Callable = _add_dunder(cls, namespace["tree_flatten"])
    flatten_with_keys: Callable = _add_dunder(cls, namespace["tree_flatten_with_keys"])
    unflatten: Callable = _add_dunder(cls, namespace["tree_unflatten"])
    return flatten, flatten_with_keys, unflatten


def register_fieldz[T: type](
    cls: T,
    *,
    data_fields: Sequence[str] | None = None,
    meta_fields: Sequence[str] | None = None,
) -> T:
    if data_fields is None:
        data_fields = _filter_fields(cls, static=False)
    if meta_fields is None:
        meta_fields = _filter_fields(cls, static=True)
    flatten: Callable
    flatten_with_keys: Callable
    unflatten: Callable
    flatten, flatten_with_keys, unflatten = codegen(cls, data_fields, meta_fields)
    jtu.register_pytree_with_keys(
        cls,
        flatten_with_keys=flatten_with_keys,
        unflatten_func=unflatten,
        flatten_func=flatten,
    )
    return cls


def _add_dunder[C: Callable](cls: type, func: C) -> C:
    func.__module__ = cls.__module__
    return func


def _codegen_tree(data: Sequence[str], meta: Sequence[str]) -> str:
    flatten: str = _codegen_tree_flatten(data, meta)
    flatten_with_keys: str = _codegen_tree_flatten_with_keys(data, meta)
    unflatten: str = _codegen_tree_unflatten(data, meta)
    return f"{flatten}\n{flatten_with_keys}\n{unflatten}"


def _codegen_tree_flatten(data: Sequence[str], meta: Sequence[str]) -> str:
    children: str = _codegen_tuple(f"obj.{name}" for name in data)
    aux: str = _codegen_tuple(f"obj.{name}" for name in meta)
    return f"""\
def tree_flatten(obj: _cls) -> tuple[tuple, tuple]:
    return {children}, {aux}
"""


def _codegen_tree_flatten_with_keys(data: Sequence[str], meta: Sequence[str]) -> str:
    children: str = _codegen_tuple(f"(_{name}_key, obj.{name})" for name in data)
    aux: str = _codegen_tuple(f"obj.{name}" for name in meta)
    return f"""\
def tree_flatten_with_keys(obj: _cls) -> tuple[tuple, tuple]:
    return {children}, {aux}
"""


def _codegen_tree_unflatten(data: Sequence[str], meta: Sequence[str]) -> str:
    lines: list[str] = []
    for i, name in enumerate(meta):
        lines.append(f'_object_setattr(obj, "{name}", aux[{i}])')
    for i, name in enumerate(data):
        lines.append(f'_object_setattr(obj, "{name}", children[{i}])')
    body: str = textwrap.indent("\n".join(lines), "    ")
    return f"""\
def tree_unflatten(aux: tuple, children: tuple) -> _cls:
    obj = _object_new(_cls)
{body}
    return obj
"""


def _codegen_tuple(elements: Iterable[str]) -> str:
    elements_str: str = "".join(f"{elem}, " for elem in elements).strip()
    return f"({elements_str})"


def _filter_fields(cls: type, *, static: bool) -> list[str]:
    names: list[str] = []
    for field in attrs.fields(cls):
        field: attrs.Attribute
        if field.metadata.get("static", False) == static:
            names.append(field.name)
    return names


def _make_filename(cls: type) -> str:
    return f"<liblaf.peach generated functions {cls.__module__}.{cls.__qualname__}>"


def _make_key_entries(fields: Iterable[str]) -> dict[str, KeyEntry]:
    return {f"_{name}_key": jtu.GetAttrKey(name) for name in fields}


def _update_linecache(source: str, filename: str) -> None:
    linecache.cache[filename] = (
        len(source),  # size
        None,  # mtime
        source.splitlines(keepends=True),  # lines
        filename,  # fullname
    )


def main() -> None:
    obj = A()
    number: int
    time_taken: float
    number, time_taken = timeit.Timer(lambda: jax.tree.flatten(obj)).autorange()
    print(f"codegen tree_flatten: {time_taken / number} sec")
    leaves: list[Leaf]
    treedef: PyTreeDef
    leaves, treedef = jax.tree.flatten(obj)
    number, time_taken = timeit.Timer(
        lambda: jax.tree.unflatten(treedef, leaves)
    ).autorange()
    print(f"codegen tree_unflatten: {time_taken / number} sec")


if __name__ == "__main__":
    main()
```

### `jtu.register_dataclass` + `dataclass`

```python
import dataclasses
import timeit
from typing import Any

import jax
import jax.tree_util as jtu

type Leaf = Any
type PyTreeDef = Any


@jtu.register_dataclass
@dataclasses.dataclass
class A:
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    e: int = 0
    f: int = 0
    g: int = 0
    h: int = dataclasses.field(default=0, metadata={"static": True})
    i: int = dataclasses.field(default=0, metadata={"static": True})
    j: int = dataclasses.field(default=0, metadata={"static": True})


def main() -> None:
    obj = A()
    number: int
    time_taken: float
    number, time_taken = timeit.Timer(lambda: jax.tree.flatten(obj)).autorange()
    print(f"dataclasses.dataclass tree_flatten: {time_taken / number} sec")
    leaves: list[Leaf]
    treedef: PyTreeDef
    leaves, treedef = jax.tree.flatten(obj)
    number, time_taken = timeit.Timer(
        lambda: jax.tree.unflatten(treedef, leaves)
    ).autorange()
    print(f"dataclasses.dataclass tree_unflatten: {time_taken / number} sec")


if __name__ == "__main__":
    main()
```

### `jtu.register_dataclass` + `attrs`

```python
import time
import timeit
from typing import Any

import attrs
import jax
import jax.tree_util as jtu

type Leaf = Any
type PyTreeDef = Any


def _slow_converter(x: Any) -> int:
    time.sleep(0.001)
    return x


@attrs.define
class A:
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    e: int = 0
    f: int = 0
    # g: int = 0
    g: int = attrs.field(default=0, converter=_slow_converter)
    h: int = attrs.field(default=0, metadata={"static": True})
    i: int = attrs.field(default=0, metadata={"static": True})
    j: int = attrs.field(default=0, metadata={"static": True})


def _filter_fields(cls: type, *, static: bool) -> list[str]:
    names: list[str] = []
    for field in attrs.fields(cls):
        field: attrs.Attribute
        if field.metadata.get("static", False) == static:
            names.append(field.name)
    return names


jtu.register_dataclass(
    A,
    data_fields=_filter_fields(A, static=False),
    meta_fields=_filter_fields(A, static=True),
)


def main() -> None:
    obj = A()
    number: int
    time_taken: float
    number, time_taken = timeit.Timer(lambda: jax.tree.flatten(obj)).autorange()
    print(f"dataclasses.dataclass tree_flatten: {time_taken / number} sec")
    leaves: list[Leaf]
    treedef: PyTreeDef
    leaves, treedef = jax.tree.flatten(obj)
    number, time_taken = timeit.Timer(
        lambda: jax.tree.unflatten(treedef, leaves)
    ).autorange()
    print(f"dataclasses.dataclass tree_unflatten: {time_taken / number} sec")


if __name__ == "__main__":
    main()
```

### Manual Register + `attrs`

```python
import timeit
from typing import Any

import attrs
import jax
import jax.tree_util as jtu

type Leaf = Any
type PyTreeDef = Any


@attrs.define
class A:
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    e: int = 0
    f: int = 0
    g: int = 0
    h: int = attrs.field(default=0, metadata={"static": True})
    i: int = attrs.field(default=0, metadata={"static": True})
    j: int = attrs.field(default=0, metadata={"static": True})


def register_attrs[T](cls: type[T]) -> None:
    data_fields: list[str] = _filter_fields(cls, static=False)
    meta_fields: list[str] = _filter_fields(cls, static=True)

    def tree_flatten(obj: T) -> tuple[tuple, tuple]:
        children: tuple = tuple(getattr(obj, name) for name in data_fields)
        aux: tuple = tuple(getattr(obj, name) for name in meta_fields)
        return children, aux

    def tree_flatten_with_keys(obj: T) -> tuple[tuple, tuple]:
        children: tuple = tuple(
            (jtu.GetAttrKey(name), getattr(obj, name)) for name in data_fields
        )
        aux: tuple = tuple(getattr(obj, name) for name in meta_fields)
        return children, aux

    def tree_unflatten(aux: tuple, children: tuple) -> T:
        obj: T = object.__new__(cls)
        for name, value in zip(meta_fields, aux, strict=True):
            object.__setattr__(obj, name, value)
        for name, value in zip(data_fields, children, strict=True):
            object.__setattr__(obj, name, value)
        return obj

    jtu.register_pytree_with_keys(
        cls,
        flatten_with_keys=tree_flatten_with_keys,
        unflatten_func=tree_unflatten,  # pyright: ignore[reportArgumentType]
        flatten_func=tree_flatten,
    )


def _filter_fields(cls: type, *, static: bool) -> list[str]:
    names: list[str] = []
    for field in attrs.fields(cls):
        field: attrs.Attribute
        if field.metadata.get("static", False) == static:
            names.append(field.name)
    return names


register_attrs(A)


def main() -> None:
    obj = A()
    number: int
    time_taken: float
    number, time_taken = timeit.Timer(lambda: jax.tree.flatten(obj)).autorange()
    print(f"attrs.define tree_flatten: {time_taken / number} sec")
    leaves: list[Leaf]
    treedef: PyTreeDef
    leaves, treedef = jax.tree.flatten(obj)
    number, time_taken = timeit.Timer(
        lambda: jax.tree.unflatten(treedef, leaves)
    ).autorange()
    print(f"attrs.define tree_unflatten: {time_taken / number} sec")


if __name__ == "__main__":
    main()
```

### `equinox.Module`

```python
import timeit
from typing import Any

import equinox as eqx
import jax

type Leaf = Any
type PyTreeDef = Any


class A(eqx.Module):
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    e: int = 0
    f: int = 0
    g: int = 0
    h: int = eqx.field(default=0, static=True)
    i: int = eqx.field(default=0, static=True)
    j: int = eqx.field(default=0, static=True)


def main() -> None:
    obj = A()
    number: int
    time_taken: float
    number, time_taken = timeit.Timer(lambda: jax.tree.flatten(obj)).autorange()
    print(f"equinox.Module tree_flatten: {time_taken / number} sec")
    leaves: list[Leaf]
    treedef: PyTreeDef
    leaves, treedef = jax.tree.flatten(obj)
    number, time_taken = timeit.Timer(
        lambda: jax.tree.unflatten(treedef, leaves)
    ).autorange()
    print(f"equinox.Module tree_unflatten: {time_taken / number} sec")


if __name__ == "__main__":
    main()
```
