---
date: 2025-06-20T14:33:59+08:00
modified: 2025-09-20T18:38:05+08:00
title: "Exploring Dispatch Performance in Python: Plum vs. `singledispatch` vs. Custom"
---

Dynamic dispatch, or choosing which function implementation to call based on argument types at runtime, is a powerful feature in programming. Python, with its dynamic typing, offers several ways to achieve this. In this post, I'll share some micro-benchmark results from an experiment comparing three dispatch mechanisms: the standard library's [`functools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatchmethod), the third-party library [`plum`](https://github.com/beartype/plum), and a simple custom conditional dispatcher.

## The Contenders

### `functools.singledispatch`

**[`functools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatchmethod):** This decorator from Python's standard library enables registering specialized functions to be called based on the type of the first argument. It's a common tool for creating generic functions in Python.

### Plum

**[`plum`](https://github.com/beartype/plum):** A third-party library designed for multiple dispatch (dispatching on the types of multiple arguments) and offering support for parametric types. Its documentation [notes](https://beartype.github.io/plum/types.html#performance-and-faithful-types):

> Although parametric types such as `List[int]` and `Dict[int, str]` are fully supported, they do incur a performance penalty.
> Methods which have signatures that depend only on faithful types will be performant. On the other hand, methods which have one or more signatures with one or more unfaithful types cannot use caching and will therefore be less performant.

### Custom Conditional Dispatcher

**Custom `ConditionalDispatcher`:** A straightforward dispatcher I built using a list of conditions and corresponding functions. It iterates through registered candidates, executing the function for the first condition that evaluates to true. This often relies on [`isinstance()`](https://docs.python.org/3/library/functions.html#isinstance) checks. The Python documentation for [`typing.runtime_checkable`](https://docs.python.org/3/library/typing.html#typing.runtime_checkable) (which I used to define a protocol) warns:

> `runtime_checkable()` will check only the presence of the required methods or attributes, not their type signatures or types. For example, [`ssl.SSLObject`](https://docs.python.org/3/library/ssl.html#ssl.SSLObject "ssl.SSLObject") is a class, therefore it passes an [`issubclass()`](https://docs.python.org/3/library/functions.html#issubclass "issubclass") check against [Callable](https://docs.python.org/3/library/typing.html#annotating-callables). However, the `ssl.SSLObject.__init__` method exists only to raise a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "TypeError") with a more informative message, therefore making it impossible to call (instantiate) [`ssl.SSLObject`](https://docs.python.org/3/library/ssl.html#ssl.SSLObject "ssl.SSLObject").
> An [`isinstance()`](https://docs.python.org/3/library/functions.html#isinstance "isinstance") check against a runtime-checkable protocol can be surprisingly slow compared to an `isinstance()` check against a non-protocol class. Consider using alternative idioms such as [`hasattr()`](https://docs.python.org/3/library/functions.html#hasattr "hasattr") calls for structural checks in performance-sensitive code.

## The Experiment

I set up a benchmark to test dispatch performance for three types of input data:
- A simple string (`"str"`)
- A dictionary (`{"a": 1, "b": 2}`), intended to be dispatched via a `runtime_checkable` protocol `SupportsKeysAndGetItem[KT, VT]`.
- A list of tuples (`[("a", 1), ("b", 2)]`), intended to be dispatched as an `Iterable[tuple[Any, Any]]`.

For each dispatch method, I registered functions to handle these types:
- `fun_xxx_str(name: str)`
- `fun_xxx_mapping(data: SupportsKeysAndGetItem)`
- `fun_xxx_iterable(data: Iterable[tuple[Any, Any]])`

The `ConditionalDispatcher` registered checks in the order: `str`, then `SupportsKeysAndGetItem`, then `Iterable`. This order is crucial to ensure, for example, that a string isn't incorrectly treated as a generic `Iterable` before its specific string handler is found.

I used [`timeit.Timer.autorange()`](https://docs.python.org/3/library/timeit.html#timeit.Timer.autorange) to measure the time taken per loop for each method and test case. An `object()` instance was used as an invalid input to test error handling, but those timings are not part of the performance comparison.

## The Results

Here's how the different dispatch mechanisms performed (time in seconds per loop):

|     Method     |      Test Case      | Time per loop (sec) |
| :------------: | :-----------------: | :-----------------: |
|      plum      |       `'str'`       |      2.028e-05      |
|      plum      | `{'a': 1, 'b': 2}`  |      1.208e-05      |
|      plum      | `[('a',1),('b',2)]` |      1.921e-05      |
| singledispatch |       `'str'`       |      2.794e-07      |
| singledispatch | `{'a': 1, 'b': 2}`  |      2.811e-07      |
| singledispatch | `[('a',1),('b',2)]` |      2.813e-07      |
|  conditional   |       `'str'`       |      2.520e-07      |
|  conditional   | `{'a': 1, 'b': 2}`  |      6.751e-07      |
|  conditional   | `[('a',1),('b',2)]` |      5.114e-06      |

## Dissecting the Numbers

Several interesting patterns emerge from these results:

1. **`functools.singledispatch` is consistently fast:** Across all test cases, `singledispatch` was remarkably quick and consistent, clocking in around 0.28 microseconds per call. This is expected, as it's a highly optimized part of the standard library.
2. **Custom `ConditionalDispatcher` shows good performance, with caveats:**
    - For the `str` test case, it was nearly as fast as `singledispatch` (around 0.25 microseconds). This is likely because the `isinstance(data, str)` check is the first in its chain and very efficient.
    - For the dictionary (`SupportsKeysAndGetItem` protocol), performance dropped to ~0.68 microseconds. This involved a successful second check, `isinstance(data, SupportsKeysAndGetItem)`, which is a protocol check.
    - For the list of tuples (`Iterable`), the time increased further to ~5.11 microseconds. This was the third check in the chain (`isinstance(data, Iterable)`), following failed checks for `str` and `SupportsKeysAndGetItem`. The Python documentation's warning about `runtime_checkable` protocol `isinstance` checks potentially being slow might play a role in the cumulative time, particularly for the path taken by the list.
3. **`plum` is notably slower in this benchmark:**
	- `plum` was significantly slower than the other two methods, with times ranging from 12 to 20 microseconds. This is roughly 40-70 times slower than `singledispatch`.
	- The `plum` documentation states that parametric types (like `Iterable[tuple[Any, Any]]`) can incur a performance penalty, and methods with "unfaithful types" (which protocols might be considered) might not benefit from caching. It's plausible that the presence of `SupportsKeysAndGetItem` (a protocol) and `Iterable[tuple[Any, Any]]` as registered types for `fun_plum` forces `plum` into a less optimized dispatch path, potentially impacting all its registered functions, even the one for the simple `str` type.
	- Interestingly, for `plum`, the dispatch on `SupportsKeysAndGetItem` (`dict` case, 12.08 µs) was slightly faster than on `str` (20.28 µs) and `Iterable` (19.21 µs). The reason for this specific variation isn't immediately obvious from the documentation snippets but underscores that performance can have nuances.

## Conclusion

This experiment highlights that the choice of dispatch mechanism can have a significant performance impact, especially in tight loops or performance-sensitive code.

- For single-argument dispatch based on type, **`functools.singledispatch`** offers excellent, consistent performance and is readily available in the standard library.
- A **custom conditional dispatcher** using `isinstance` can also be very performant, particularly if common cases are checked early. However, its performance can degrade with more conditions or complex `isinstance` checks (like those involving `runtime_checkable` protocols). The order of registration is also critical for correctness.
- **`plum`**, while offering powerful features like multiple dispatch and sophisticated type handling, showed higher overhead in this specific micro-benchmark. This seems to align with its documentation regarding performance characteristics with parametric or "unfaithful" types. It's designed for more complex scenarios, where its added flexibility might outweigh the raw speed of simpler dispatchers.

As always, these are micro-benchmarks. The best choice depends on your specific needs, the complexity of your dispatch logic, and the types you're working with. If performance is critical, benchmarking your actual use case is invaluable.

## Code

```python
import functools
import timeit
from collections.abc import Callable, Iterable
from typing import Any, Protocol, runtime_checkable

import attrs
import plum


@runtime_checkable
class SupportsKeysAndGetItem[KT, VT](Protocol):
    def keys(self) -> Iterable[KT]: ...
    def __getitem__(self, key: KT) -> VT: ...


@plum.dispatch.abstract
def fun_plum(data: Any) -> None: ...
@fun_plum.register
def fun_plum_str(name: str) -> None: ...
@fun_plum.register
def fun_plum_mapping(data: SupportsKeysAndGetItem) -> None: ...
@fun_plum.register
def fun_plum_iterable(data: Iterable[tuple[Any, Any]]) -> None: ...


@functools.singledispatch
def fun_singledispatch() -> None:
    raise TypeError


@fun_singledispatch.register
def fun_singledispatch_str(name: str) -> None: ...
@fun_singledispatch.register
def fun_singledispatch_mapping(data: SupportsKeysAndGetItem) -> None: ...
@fun_singledispatch.register(Iterable)
def fun_singledispatch_iterable(data: Iterable[tuple[Any, Any]]) -> None: ...


@attrs.define
class ConditionalDispatchCandidate:
    condition: Callable[..., bool]
    func: Callable


@attrs.define
class ConditionalDispatcher:
    functions: list[ConditionalDispatchCandidate] = attrs.field(factory=list)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        for candidate in self.functions:
            if candidate.condition(*args, **kwargs):
                return candidate.func(*args, **kwargs)
        raise TypeError

    def register[C: Callable](self, condition: Callable[..., bool]) -> Callable[[C], C]:
        def decorator(func: C) -> C:
            self.functions.append(ConditionalDispatchCandidate(condition, func))
            return func

        return decorator


fun_conditional = ConditionalDispatcher()


@fun_conditional.register(lambda data: isinstance(data, str))
def fun_conditional_str(name: str) -> None: ...
@fun_conditional.register(lambda data: isinstance(data, SupportsKeysAndGetItem))
def fun_conditional_mapping(data: SupportsKeysAndGetItem) -> None: ...
@fun_conditional.register(lambda data: isinstance(data, Iterable))
def fun_conditional_iterable(data: Iterable[tuple[Any, Any]]) -> None: ...


testcases = [
    "str",
    {"a": 1, "b": 2},
    [("a", 1), ("b", 2)],
    object(),  # invalid input
]

for method in ["plum", "singledispatch", "conditional"]:
    for testcase in testcases:
        timer = timeit.Timer(
            f"fun_{method}(data)", globals=globals() | {"data": testcase}
        )
        try:
            number: int
            time_taken: float
            number, time_taken = timer.autorange()
        except (LookupError, TypeError):
            continue
        else:
            print(f"{method} {testcase!r}: {time_taken / number:.3e} sec per loop")
```
