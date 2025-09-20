---
date: 2025-06-04T22:02:00+08:00
modified: 2025-09-20T18:38:01+08:00
tags:
  - JAX
  - JIT
  - Programming/Python
title: "JAX JIT and the Case of the Disappearing Cache: Understanding `PyTreeNodes` and `functools.cached_property`"
---

When working with [JAX](https://github.com/jax-ml/jax), especially when using [`jax.jit`](https://docs.jax.dev/en/latest/jit-compilation.html) for performance, you might encounter some surprising behaviors if you're not careful about how JAX "sees" and handles your objects. One such area is the interaction between `jax.jit` and Python's [`@functools.cached_property`](https://docs.python.org/3/library/functools.html#functools.cached_property). You might find that your property isn't as "cached" as you expect within JIT-compiled functions.

Let's dive into this with some test code.

## The Core Players

1. **[`jax.jit`](https://docs.jax.dev/en/latest/jit-compilation.html):** This powerful decorator compiles your Python functions into highly optimized XLA code. A key aspect of JIT is **tracing**. When a function is JIT-compiled, JAX calls it once with abstract representations of the inputs (called "Tracers"). It records all operations performed on these Tracers. The sequence of operations is then compiled.
2. **[`flax.struct.PyTreeNode`](https://flax.readthedocs.io/en/latest/api_reference/flax.struct.html#flax.struct.PyTreeNode):** These are classes that JAX knows how to treat as "PyTrees." This means JAX can iterate over their attributes (specified as type-annotated fields) and treat them as children in the PyTree structure. This is crucial for JIT, as it needs to know which parts of your object contain JAX arrays or other JAX-compatible data.
3. **[`@functools.cached_property`](https://docs.python.org/3/library/functools.html#functools.cached_property):** This decorator transforms a method of a class into a property whose value is computed once and then cached as an ordinary attribute in the instance's `__dict__`. Subsequent accesses retrieve the value from the `__dict__`.

## Scenario 1: `jax.jit` on `@functools.cached_property`

```python
import functools
import flax.struct
import jax
import jax.numpy as jnp

class Foo(flax.struct.PyTreeNode):
    a: jax.Array

    @functools.cached_property
    @jax.jit  # The property itself is JIT-compiled
    def b(self) -> jax.Array:
        jax.debug.print("Computing b ...")
        return jnp.sum(self.a)

@jax.jit
def use_b(foo: Foo) -> jax.Array:
    # print(foo.__dict__) # For debugging, would show only 'a' as a Tracer here
    return foo.b
```

Let's look at the behaviors:

### `foo.b, foo.b` (Outside JIT context)

```python
foo = Foo(a=jnp.ones((3, 3)))
print(foo.b) # Prints "Computing b ...", b is computed
# `b` is now cached in `foo.__dict__`
print(foo.b) # Does NOT print "Computing b ...", uses cached value
```

This works as expected. The first call to `foo.b` computes the sum, prints the message, and stores the result in `foo.__dict__['b']`. The second call finds `b` in `__dict__` and returns it directly.

### `foo.b, use_b(foo)` (Mixing JIT and non-JIT)

```python
foo = Foo(a=jnp.ones((3, 3)))
print(foo.b) # Prints "Computing b ...", b is computed and cached on original foo
# foo.__dict__ now contains 'b'
print(use_b(foo)) # Prints "Computing b ..." AGAIN!
```

Why the recomputation?

1. The first `foo.b` caches `b` in the `__dict__` of the _original_ `foo` object.
2. When `use_b(foo)` is called, JAX traces it. The `foo` object passed into `use_b` is treated as a `PyTreeNode`. JAX creates an _internal representation_ of `foo` for tracing purposes. This internal `foo` only contains the JAX-registered fields (in this case, `a`, which becomes a Tracer).
3. Crucially, the `__dict__` of the _original_ `foo` (and its cached `b`) is _not_ part of the JAX-registered fields. So, the internal `foo` inside `use_b` doesn't have `b` in its (non-existent or empty) `__dict__`.
4. When `foo.b` is accessed inside `use_b`, it's operating on this internal, traced `foo`. Since `b` isn't cached there, the `b` property's code (which is JIT-compiled itself) executes again, printing "Computing b ...".

### `use_b(foo), use_b(foo)` (Multiple JIT calls)

```python
foo = Foo(a=jnp.ones((3, 3)))
print(use_b(foo)) # Prints "Computing b ..."
print(use_b(foo)) # Prints "Computing b ..." AGAIN!
```

Each call to `use_b(foo)` JIT-compiles (on the first call) or reuses the compiled function. Each time, `foo` is passed as an input. The caching that `@functools.cached_property` tries to do (modifying `__dict__`) happens on an internal, temporary representation of `foo` _within_ that JITted execution. This cache does not persist across separate calls to `use_b` because the `__dict__` is not a returned value or a JAX-managed state.

### `use_b(foo), foo.b` (JIT call then outside JIT)

```python
foo = Foo(a=jnp.ones((3, 3)))
print(use_b(foo)) # Prints "Computing b ..."
print(foo.b)      # Prints "Computing b ..." AGAIN!
```

1. `use_b(foo)` computes `b` internally, as explained. This does not affect the `__dict__` of the _original, external_ `foo` object.
2. When `foo.b` is called on the _original_ `foo` object, its `__dict__` does not yet contain `b` (assuming it wasn't called before `use_b`), so it computes again.

### The Root Cause for Scenario 1

`@functools.cached_property` relies on Python's standard object attribute storage (`__dict__`). JAX's tracing mechanism for `PyTreeNode`s only considers the explicitly defined fields (like `a`). It doesn't know about or track changes to the `__dict__`. When the property `b` itself is JIT-compiled, the attempt to cache by modifying `self.__dict__` is a side effect that JAX's JIT compilation model doesn't reliably preserve or propagate in the way `cached_property` expects.

## Scenario 2: Manual Caching with a `PyTreeNode` Field

Now, let's look at your second approach, where you manually manage the cache using a field that JAX _does_ know about.

```python
class Foo(flax.struct.PyTreeNode, frozen=False): # frozen=False allows modification
    a: jax.Array
    _c_cache: jax.Array = flax.struct.field(default=None) # JAX is aware of this field

    @property
    # NOT JIT-compiled itself
    def c(self) -> jax.Array:
        if self._c_cache is not None:
            return self._c_cache
        jax.debug.print("Computing c ...")
        self._c_cache = jnp.sum(self.a) # Modify the registered field
        return self._c_cache

@jax.jit
def use_c(foo: Foo) -> jax.Array:
    # ic(foo.__dict__) # Would show 'a' and '_c_cache' as Tracers
    return foo.c
```

### `foo.c, foo.c` (Outside JIT context)

```python
foo = Foo(a=jnp.ones((3, 3)))
print(foo.c) # Prints "Computing c ...", _c_cache is populated
print(foo.c) # Does NOT print "Computing c ...", uses _c_cache
```

This works because `_c_cache` is a regular attribute on the `foo` instance. The `frozen=False` on `PyTreeNode` allows this attribute to be modified.

### `foo.c, use_c(foo)` (Mixing non-JIT property and JIT function)

```python
foo = Foo(a=jnp.ones((3, 3)))
print(foo.c) # Prints "Computing c ...", original foo._c_cache is populated
# Now, original foo has _c_cache set.
print(use_c(foo)) # Does NOT print "Computing c ..."
```

This is a key difference!

1. `foo.c` is called on the original `foo`. It computes `c` and stores it in `foo._c_cache`.
2. When `use_c(foo)` is called, `foo` is passed to the JIT-compiled function. JAX traces `foo`, including its registered fields `a` and `_c_cache`. The _value_ of `_c_cache` (which is now the computed sum) is part of the traced inputs.
3. Inside `use_c`, when `foo.c` is accessed, `self` is the traced `foo`. Its `_c_cache` field already holds the sum (as a traced value). The `if self._c_cache is not None:` check (which JAX can handle for `None` or JAX arrays) passes, and the cached value is returned. No recomputation.

### `use_c(foo), use_c(foo)` (Multiple JIT calls)

```python
foo = Foo(a=jnp.ones((3, 3)))
print(use_c(foo)) # Prints "Computing c ..."
print(use_c(foo)) # Prints "Computing c ..." AGAIN!
```

This recomputes, similar to the `use_b` case, but for a slightly different reason regarding state.

1. First call to `use_c(foo)`: The _original_ `foo` object (where `_c_cache` is initially `None`) is passed. Inside `use_c`, `foo.c` is called.
2. The `if self._c_cache is not None:` check is performed on the _traced version_ of `_c_cache`, which is `None`. So, "Computing c ..." is printed.
3. The line `self._c_cache = jnp.sum(self.a)` executes. Since `_c_cache` is a JAX-aware field, this assignment updates the `_c_cache` of the _internal, traced `foo` object_ for the duration of this JITted execution.
4. However, this modification to the internal `_c_cache` within `use_c` does _not_ affect the `_c_cache` of the _original, external_ `foo` object unless `use_c` were to return the modified `foo` and you were to use that returned instance.
5. Second call to `use_c(foo)`: The _same original_ `foo` object is passed in again. Its `_c_cache` is still `None` (because the first call to `use_c` didn't change the external `foo`). So, the computation happens again.

### `use_c(foo), foo.c` (JIT call then outside JIT)

```python
foo = Foo(a=jnp.ones((3, 3)))
print(use_c(foo)) # Prints "Computing c ..."
print(foo.c)      # Prints "Computing c ..." AGAIN!
```

1. `use_c(foo)` is called. As above, "Computing c ..." is printed. The `_c_cache` of the _external_ `foo` object remains `None`.
2. When `foo.c` is called on the _original, external_ `foo` object, its `_c_cache` is still `None`, so it computes again.

### Why the Manual Cache (`_c_cache`) Behaves This Way

- **Visibility to JAX**: Because `_c_cache` is a registered field in the `PyTreeNode`, JAX includes it in its tracing process. When `foo` is an input to a JITted function, the _current value_ of `foo._c_cache` is made available to the traced function.
- **Side Effects in JIT**: JITted functions are ideally pure from JAX's perspective. Modifying an input object's attribute (like `_c_cache = ...` inside the property `c` when called from `use_c`) is a side effect.
  - When `c` is called from `use_c`, the property `c` itself is _not_ JIT-compiled. It executes as regular Python code _during the JIT trace or execution of `use_c`_.
  - The assignment `self._c_cache = ...` happens on the _traced_ representation of `foo`. This update is visible _within the current execution_ of the JITted function `use_c`.
  - However, this internal update doesn't automatically propagate back to the original Python object `foo` that was passed into `use_c`. JAX usually requires you to explicitly return modified objects if you want to see their changes outside the JITted function.

## Key Takeaways & Best Practices

1. **JIT and Instance State:** `jax.jit` primarily cares about the data in the registered fields of your `PyTreeNode`s. Python's internal mechanisms like `__dict__` (used by `functools.cached_property`) are generally opaque to JIT and are not part of the traced state of a `PyTreeNode`.
2. **Caching Scope:**
   - `@functools.cached_property`: Caching works reliably outside JIT. Inside JIT, or when the property itself is JITted, its reliance on `__dict__` makes it behave unexpectedly because `__dict__` isn't a JAX-traced field.
   - **Manual Cache Field**: If the cache is a JAX-registered field (like `_c_cache`):
     - If populated _before_ calling the JITted function, the JITted function will see the cached value.
     - If the caching logic (property setter) is called _from within_ a JITted function, it modifies an _internal, traced version_ of the object. This change doesn't affect the original external object or persist to subsequent independent calls to the JITted function with the same original object, unless you explicitly return the modified object from the JITted function and use that returned instance for further operations.
3. **Purity and Side Effects:** JAX prefers pure functions (functions that don't have side effects). Modifying an object's state within a JITted function is a side effect. While JAX can sometimes handle updates to its own registered fields (like `_c_cache`), it's often clearer to design JITted functions to take inputs and produce outputs, with state updates handled by passing modified objects out of the function.

## In Conclusion

When you want to cache computations in JAX objects that interact with `jax.jit`:

- Avoid `@functools.cached_property` if the property is accessed within JIT-compiled code or if the property itself is JIT-compiled, as its caching mechanism is invisible to JAX's tracing.
- Using a manual cache field (like `_c_cache`) makes the cached data visible to JAX.
- Be mindful that modifications to such fields _within_ a JITted function call are typically on an internal representation and won't update the original external object unless that object is returned by the JITted function.
- For robust state management within JIT, especially for things like model parameters or optimizer states, consider Flax's `Module` system, which has its own mechanisms for handling state (`variables`, `sow`) that are designed to work correctly with JAX transformations.

Understanding how JAX traces and handles PyTreeNodes is key to avoiding these caching conundrums and writing effective JAX code!
