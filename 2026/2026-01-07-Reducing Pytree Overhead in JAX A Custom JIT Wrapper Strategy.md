---
date: 2026-01-07T12:04:58+08:00
modified: 2026-01-07T16:25:16+08:00
title: "Reducing pytree Overhead in JAX: A Custom JIT Wrapper Strategy"
---

If you have worked with [JAX](https://docs.jax.dev/) for long enough, you have likely run into the "static argument" problem. [`jax.jit`](https://docs.jax.dev/en/latest/jit-compilation.html) works wonders until you pass a pytree containing a string, an integer, or any non-array data. JAX throws a `TypeError` because it tries to trace these values.

The standard community solution is Patrick Kidger's excellent library, [Equinox](https://github.com/patrick-kidger/equinox), which provides [`equinox.filter_jit`](https://docs.kidger.site/equinox/api/transformations/#equinox.filter_jit). This function automatically partitions your arguments into "traced" (arrays) and "static" (everything else) parts.

However, convenience comes at a cost. While profiling a complex pytree setup, I noticed that `eqx.filter_jit` introduces significant overhead in the form of repeated `tree_flatten` and `tree_unflatten` operations.

In this post, I'll share an experiment demonstrating this overhead and introduce a custom "Object Wrapper" JIT strategy that handles static arguments seamlessly without the traversal penalty.

## The Experiment Setup

To measure the overhead, I instrumented a standard JAX pytree node (`Input`) and a wrapper class with a decorator that counts how many times `tree_flatten` and `tree_unflatten` are called.

Here is the scenario:
1. **`jax.jit`**: The baseline. Fast, but crashes on static data.
2. **`eqx.filter_jit`**: The standard solution for mixed static / dynamic args.
3. **`my_jit`**: A custom implementation using an `ObjectWrapper`.

### The Problem with `eqx.filter_jit` overhead

Let's look at the trace output when running a simple function `fun(x)` where `x` is a custom pytree node.

When running `jax.jit(fun)(x)`, the overhead is minimal:

```text
Input.tree_flatten
Input.tree_unflatten
Output.tree_unflatten
```

However, when running `equinox.filter_jit(fun)(x)`, the JIT boundary triggers a flurry of traversals:

```text
Input.tree_flatten
Input.tree_unflatten
Output.tree_unflatten
Input.tree_unflatten
Output.tree_unflatten
Output.tree_flatten
Input.tree_flatten
Output.tree_flatten
Input.tree_flatten
Input.tree_unflatten
Output.tree_unflatten
```

For small models, this is negligible. But for complex nested pytrees (common in LLMs or physics simulations), recursively flattening and unflattening the tree 10+ times per call can add measurable Python overhead before the XLA compilation even kicks in.

## The Solution: The `ObjectWrapper` Strategy

The core issue is how JAX decides what to trace. We want JAX to see **only** the arrays, while we secretly smuggle the static data through the JIT boundary.

Instead of relying on Equinox to filter the tree repeatedly, we can wrap our arguments in a container that strictly separates arrays from static data within its own `tree_flatten` method.

### The Wrapper Implementation

We define a class `ObjectWrapper` registered as a pytree node. Its job is to intercept `tree_flatten`, scan the wrapped object, and push non-array leaves into `AuxData` (metadata), which JAX ignores during tracing.

```python
@jtu.register_pytree_node_class
class ObjectWrapper:
    wrapped: Any

    @dataclasses.dataclass(frozen=True)
    class AuxData:
        static_leaves: Sequence[Any]
        treedef: Any

    def __init__(self, wrapped: Any) -> None:
        self.wrapped = wrapped

    def tree_flatten(self) -> tuple[Sequence[Any], AuxData]:
        # 1. Standard flatten of the inner object
        leaves, treedef = jax.tree.flatten(self.wrapped)
        
        dynamic_leaves = []
        static_leaves = []
        
        # 2. Manual Partitioning
        for leaf in leaves:
            if eqx.is_array(leaf):
                dynamic_leaves.append(leaf)
                static_leaves.append(None)
            else:
                dynamic_leaves.append(None)
                # 3. Hide static data in the metadata
                static_leaves.append(leaf)
                
        return tuple(dynamic_leaves), self.AuxData(static_leaves, treedef)

    @classmethod
    def tree_unflatten(cls, aux: AuxData, children: Sequence[Any]) -> Self:
        # Reconstruct the original leaves
        leaves = []
        for d, s in zip(children, aux.static_leaves, strict=True):
            leaves.append(d if d is not None else s)
            
        wrapped = jax.tree.unflatten(aux.treedef, leaves)
        return cls(wrapped)
```

### The Custom JIT

Now we can write `my_jit`. It accepts normal arguments, wraps them into the `ObjectWrapper`, passes them to the compiled function, and unwraps the result.

```python
def my_jit[**P, T](fun: Callable[P, T]) -> Callable[P, T]:
    @jax.jit
    def inner(inputs: ObjectWrapper) -> ObjectWrapper:
        # Inside JIT: unwrap, call, re-wrap
        args, kwargs = inputs.wrapped
        result = fun(*args, **kwargs)
        return ObjectWrapper(result)

    def wrapper(*args, **kwargs) -> T:
        inputs = ObjectWrapper((args, kwargs))
        output = inner(inputs)
        return output.wrapped

    return wrapper
```

## The Results

When we run the same test with `my_jit(fun)(x)`, even with static data present:

```text
ObjectWrapper.tree_flatten
Input.tree_flatten
ObjectWrapper.tree_unflatten
Input.tree_unflatten
Output.tree_unflatten
```

This is the best of both worlds:
1. **Robustness:** It handles static data (`string`s, `int`s) just like `eqx.filter_jit`.
2. **Efficiency:** It maintains a call count nearly identical to raw `jax.jit`.

### Why is this faster?

`equinox.filter_jit` is incredibly general-purpose. To handle arbitrary filtering safely, it performs multiple passes over the pytree structure to ensure consistency.

My `ObjectWrapper` approach moves the filtering logic to the **edge**. We filter exactly once during the initial flatten. As far as JAX's internal C++ engine is concerned, `ObjectWrapper` is just a simple node containing a list of arrays. It doesn't need to know about the strings or integers hidden in `AuxData`.

## Conclusion

If you are prototyping, stick with `equinox.filter_jit` --- it is battle-tested and easy to use. However, if you have complex custom pytrees and you observe high Python overhead during tracing or execution, implementing a "Wrap-and-Hide" strategy like `ObjectWrapper` can significantly reduce pytree traversal costs while maintaining the ability to mix static and dynamic arguments.

---

## Appendix: Full Runnable Code

```python
import collections
import contextvars
import dataclasses
import functools
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any, Self

import equinox as eqx
import jax
import jax.numpy as jnp
import jax.tree_util as jtu

# Type alias for clarity
type PyTreeDef = Any

# Global counter to track operations
counter: collections.Counter[str] = collections.Counter()
# ContextVar to toggle printing during execution
print_call: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "print_call", default=True
)


def count[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    """Decorator to count and print calls to tree operations."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Determine class name for logging
        cls: type = args[0] if isinstance(args[0], type) else type(args[0])
        name: str = f"{cls.__name__}.{func.__name__}"
        
        counter[name] += 1
        if print_call.get():
            print(name)
        return func(*args, **kwargs)

    return wrapper


@jtu.register_pytree_node_class
class ObjectWrapper[T]:
    """
    Wraps any object. Flattens into (dynamic_leaves, static_aux_data).
    Non-array leaves are automatically moved to AuxData.
    """
    wrapped: T

    @dataclasses.dataclass(eq=True, frozen=True)
    class AuxData:
        static_leaves: tuple[Any, ...]
        treedef: PyTreeDef

    def __init__(self, wrapped: Any) -> None:
        self.wrapped = wrapped

    @count
    def tree_flatten(self) -> tuple[list[Any], AuxData]:
        leaves: list[Any]
        treedef: PyTreeDef
        # Flatten the inner object first
        leaves, treedef = jax.tree.flatten(self.wrapped)
        
        dynamic_leaves: list[Any] = []
        static_leaves: list[Any] = []
        
        # Partition leaves
        for leaf in leaves:
            if eqx.is_array(leaf):
                dynamic_leaves.append(leaf)
                static_leaves.append(None)
            else:
                dynamic_leaves.append(None)
                static_leaves.append(leaf)
                
        return dynamic_leaves, self.AuxData(tuple(static_leaves), treedef)

    @classmethod
    @count
    def tree_unflatten(cls, aux: AuxData, children: Iterable[Any]) -> Self:
        leaves: list[Any] = []
        # Recombine
        for d, s in zip(children, aux.static_leaves, strict=True):
            leaves.append(d if d is not None else s)
        wrapped: T = jax.tree.unflatten(aux.treedef, leaves)
        return cls(wrapped)


# Helper type for the arguments passed to the inner jitted function
type ParamsWrapper = ObjectWrapper[tuple[tuple[Any, ...], dict[str, Any]]]


def my_jit[**P, T](fun: Callable[P, T]) -> Callable[P, T]:
    """
    Custom JIT that wraps inputs/outputs to handle static args automatically.
    """
    @jax.jit
    def inner(inputs: ParamsWrapper) -> ObjectWrapper[T]:
        args: Sequence[Any]
        kwargs: Mapping[str, Any]
        args, kwargs = inputs.wrapped
        result: T = fun(*args, **kwargs)  # pyright: ignore
        return ObjectWrapper(result)

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        inputs: ParamsWrapper = ObjectWrapper((args, kwargs))
        output: ObjectWrapper[T] = inner(inputs)
        return output.wrapped

    return wrapper


@jtu.register_pytree_node_class
class Input:
    """A simple test PyTree."""
    type AuxData = None
    type Children = tuple[Any]

    data: Any = None

    def __init__(self, data: Any = None) -> None:
        self.data = data

    @count
    def tree_flatten(self) -> tuple[Children, AuxData]:
        return (self.data,), None

    @classmethod
    @count
    def tree_unflatten(cls, _aux: AuxData, children: Children) -> Self:
        data: Any
        (data,) = children
        return cls(data)


@jtu.register_pytree_node_class
class Output(Input): 
    pass


def fun(x: Input) -> Output:
    return Output(x.data)


# Prepare variants
fun_jit = jax.jit(fun)
fun_filter_jit = eqx.filter_jit(fun)
fun_my_jit = my_jit(fun)


def test_without_static() -> None:
    x = Input(jnp.zeros((3,)))

    print_call.set(False)
    # Warmup to ensure we aren't counting compilation traces
    fun_jit(x)
    fun_filter_jit(x)
    fun_my_jit(x)

    print_call.set(True)
    print("--- jax.jit() ---")
    fun_jit(x)
    
    print("--- equinox.filter_jit() ---")
    fun_filter_jit(x)
    
    print("--- my_jit() ---")
    fun_my_jit(x)


def test_with_static() -> None:
    x = Input("static data")
    print_call.set(False)
    # Warmup
    try:
        fun_jit(x)
    except TypeError:
        # Expected failure
        pass
    fun_filter_jit(x)
    fun_my_jit(x)

    print_call.set(True)
    print("--- jax.jit() with static data (skipped, would fail) ---")
    
    print("--- equinox.filter_jit() with static data ---")
    fun_filter_jit(x)
    
    print("--- my_jit() with static data ---")
    fun_my_jit(x)


def main() -> None:
    print("Running experiments...")
    test_without_static()
    print("\n" + "="*30 + "\n")
    test_with_static()


if __name__ == "__main__":
    main()
```
