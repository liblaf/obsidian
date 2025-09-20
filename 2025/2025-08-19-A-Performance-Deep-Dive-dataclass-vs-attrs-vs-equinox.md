---
date: 2025-08-19T20:32:16+08:00
modified: 2025-09-20T18:38:10+08:00
tags:
  - Programming/Python
title: "A Performance Deep Dive: `dataclass` vs. `attrs` vs. `equinox`"
---

## TL;DR

| Operation (Relative) | `Class()` | `obj.x` | `obj.x = 42` | `obj.method` |
| -------------------- | --------: | ------: | -----------: | -----------: |
| `attrs`              |     1.00x |   1.00x |        1.00x |        1.00x |
| `dataclass`          |     1.25x |   1.73x |        2.08x |        1.07x |
| `eqx.Module`         |   132.90x |  25.06x |            - |     1121.94x |

| Operation (sec) | `Class()`  |  `obj.x`   | `obj.x = 42` | `obj.method` |
| --------------- | :--------: | :--------: | :----------: | :----------: |
| `attrs`         | 1.0180e-07 | 1.0463e-08 |  1.0519e-08  |  3.7334e-08  |
| `dataclass`     | 1.2739e-07 | 1.8139e-08 |  2.1912e-08  |  4.0077e-08  |
| `eqx.Module`    | 1.3529e-05 | 2.6220e-07 |      -       |  4.1887e-05  |

- **[`attrs`](https://www.attrs.org/) is the fastest** across the board in all tested categories: instantiation, attribute access, and method access.
- **[`dataclasses`](https://docs.python.org/3/library/dataclasses.html)** are a very close second, showing excellent performance with the benefit of being in the standard library.
- **[`equinox.Module`](https://docs.kidger.site/equinox/) is significantly slower** in these micro-benchmarks. This is not a flaw, but a deliberate trade-off. `equinox` adds a considerable amount of functionality --- most importantly, deep integration with the JAX PyTree ecosystem --- which introduces overhead. This overhead is the price for features that are essential when building complex, JAX-native models.

## Introduction

When defining structured data in Python, developers have several excellent choices. The standard library offers `dataclasses`, the popular third-party library `attrs` provides even more features, and for the JAX ecosystem, `equinox` presents a powerful way to build models as PyTrees.

But how do they compare in terms of performance? I ran a series of micro-benchmarks to find out. This post presents the results, the code to reproduce them, and a deep dive into the "why" behind the numbers.

## The Contenders

1. **`dataclass` (`from dataclasses import dataclass`)**: Introduced in Python 3.7, this is the standard library's solution for reducing boilerplate. It's the baseline for convenience and performance.
2. **`attrs` (`import attrs`)**: The project that inspired `dataclass`. It's a mature, feature-rich library that offers more functionality and flexibility than the standard library version.
3. **`eqx.Module` (`import equinox as eqx`)**: A part of the Equinox library, which is built on JAX. Its primary goal is to be a powerful framework for building neural networks and scientific computing models, treating PyTrees as first-class citizens. Its performance characteristics are interesting in a general context.

## Benchmark Results

See [TL;DR](#TL;DR).

## Analysis: Why is `equinox` Slower?

The results are clear: `equinox` has significant overhead. Let's dive into its source code to understand where this comes from.

#### 1. Instantiation Overhead (>130x slower)

When you create an instance of an `equinox.Module`, it does much more than just assign variables. Its metaclass, `_ModuleMeta`, performs several setup steps:

- **PyTree Registration:** It calls `jtu.register_pytree_with_keys` to register the new class with JAX. This allows JAX transformations like `jax.jit` and `jax.grad` to understand the module's structure.
- **Field Validation:** The `__call__` method of the metaclass (which acts as the constructor) performs extensive checks after the object is created. It verifies that all fields were initialized, checks for converters, warns about using JAX arrays in `static` fields, and runs any user-defined `__check_init__` methods.
- **JAX Function Warnings:** It inspects arguments to warn users if they are assigning a JAX-transformed function (like one wrapped with `@jax.jit`) as a field, which is a common source of bugs.

This setup work is crucial for integrating seamlessly with JAX but adds a fixed cost to instantiation.

#### 2. Method Access Overhead (>1100x slower)

The most dramatic difference is in getting a method. This is because `equinox` cleverly makes bound methods part of the PyTree structure. It achieves this by [overriding `__getattribute__`](https://github.com/patrick-kidger/equinox/blob/65d93fc1cf68a8b913c818687346a88efe312761/equinox/_module/_module.py#L646-L663):

```python
def __getattribute__(self, name: str, /) -> Any:
    out = super().__getattribute__(name)
    # ...
    if (
        not _is_magic(name)
        and isinstance(out, types.MethodType)
        and out.__self__ is self
    ):
        out = BoundMethod(object.__getattribute__(out, "__func__"), self)
    return out
```

Every time you access an attribute, this code runs. If the attribute is a method, it dynamically wraps it in a `BoundMethod` object. This `BoundMethod` is itself a small `equinox.Module` that holds a reference to the original function (`__func__`) and the instance (`__self__`).

This wrapping ensures that you can pass a method directly to a JAX transformation (`jax.jit(my_module.my_method)`), which is a powerful feature. However, the cost is creating a new `BoundMethod` object on every single method access, leading to the massive performance difference seen in the benchmark.

## Conclusion

- For general-purpose Python programming where performance is key, **`attrs` remains the top choice**. It's lightweight, fast, and feature-rich.
- **`dataclasses`** are an excellent, zero-dependency alternative that is nearly as fast as `attrs` for most operations.
- **`equinox.Module`** is a specialized tool for a specialized job: building neural networks and other complex models in JAX. Its performance overhead is a direct result of the features that make it so powerful and easy to use within the JAX ecosystem. When you are `jit`-compiling your code, these Python-side overheads become negligible, while the benefits of a robust PyTree structure remain.

The right choice depends on your needs. If you're building a JAX model and value developer experience, correctness guarantees, and seamless integration, equinox is an outstanding choice. However, if micro-second performance in Python-land is critical, a more manual approach with `attrs` and JAX's core utilities may be the better path.

## Appendix

### Source Code

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "attrs",
#     "equinox",
#     "rich",
# ]
# ///

# ruff: noqa: N801

import dataclasses
import time
import timeit
from collections.abc import Callable, Mapping, Sequence
from typing import Any

import attrs
import equinox as eqx
import rich

type Stmt = str | Callable[[], Any]
type Timer = Callable[[], float]


def bench_it(
    stmt: Stmt = "pass",
    setup: Stmt = "pass",
    timer: Timer = time.perf_counter,
    globals: dict[str, Any] | None = None,  # noqa: A002
) -> float:
    bencher = timeit.Timer(stmt=stmt, setup=setup, timer=timer, globals=globals)
    number: int
    time_taken: float
    number, time_taken = bencher.autorange()
    return time_taken / number


def summary(benchmarks: Mapping[str, float], group: str) -> None:
    items: Sequence[tuple[str, float]] = sorted(benchmarks.items(), key=lambda x: x[1])
    rich.print(f"[bold]Benchmark {group}:[/bold]")
    for name, duration in items:
        print(f"  {name:<10}: {duration:.5g} seconds")
    fastest_name: str
    fastest_duration: float
    fastest_name, fastest_duration = items[0]
    rich.print(f"  [cyan]{fastest_name}[/cyan] ran")
    for name, duration in items[1:]:
        ratio: float = duration / fastest_duration
        rich.print(
            f"  [green]{ratio:.2f}[/green] times faster than [magenta]{name}[/magenta]"
        )


@dataclasses.dataclass
class A_dataclass:
    x: int = dataclasses.field(default=0)

    def fun(self) -> None: ...


@attrs.define
class A_attrs:
    x: int = attrs.field(default=0)

    def fun(self) -> None: ...


class A_equinox(eqx.Module):
    x: int = eqx.field(default=0)

    def fun(self) -> None: ...


def bench_instantiate() -> None:
    benchmarks: dict[str, float] = {}
    benchmarks["dataclass"] = bench_it(
        "A_dataclass()", globals={"A_dataclass": A_dataclass}
    )
    benchmarks["attrs"] = bench_it("A_attrs()", globals={"A_attrs": A_attrs})
    benchmarks["equinox"] = bench_it("A_equinox()", globals={"A_equinox": A_equinox})
    summary(benchmarks, group="Instantiation")


def bench_get_property() -> None:
    benchmarks: dict[str, float] = {}
    benchmarks["dataclass"] = bench_it("a.x", globals={"a": A_dataclass()})
    benchmarks["attrs"] = bench_it("a.x", globals={"a": A_attrs()})
    benchmarks["equinox"] = bench_it("a.x", globals={"a": A_equinox()})
    summary(benchmarks, group="Get Property")


def bench_set_property() -> None:
    benchmarks: dict[str, float] = {}
    benchmarks["dataclass"] = bench_it("a.x = 42", globals={"a": A_dataclass()})
    benchmarks["attrs"] = bench_it("a.x = 42", globals={"a": A_attrs()})
    # `eqx.Module` are frozen
    summary(benchmarks, group="Set Property")


def bench_get_method() -> None:
    benchmarks: dict[str, float] = {}
    benchmarks["dataclass"] = bench_it("a.fun", globals={"a": A_dataclass()})
    benchmarks["attrs"] = bench_it("a.fun", globals={"a": A_attrs()})
    benchmarks["equinox"] = bench_it("a.fun", globals={"a": A_equinox()})
    summary(benchmarks, group="Get Method")


def main() -> None:
    bench_instantiate()
    bench_get_property()
    bench_set_property()
    bench_get_method()


if __name__ == "__main__":
    main()
```

### Environment

- **CPU:** Intel(R) Core(TM) i7-10700 (16) @ 4.80 GHz
- **Kernel:** Linux 6.12.42-2-cachyos-lts-lto
- **Python:** 3.12.10
- **Packages:**
  - `attrs`: 25.3.0
  - `equinox`: 0.13.0
  - `jax`: 0.7.0

### Outputs

```
Benchmark Instantiation:
  attrs     : 1.018e-07 seconds
  dataclass : 1.2739e-07 seconds
  equinox   : 1.3529e-05 seconds
  attrs ran
  1.25 times faster than dataclass
  132.90 times faster than equinox
Benchmark Get Property:
  attrs     : 1.0463e-08 seconds
  dataclass : 1.8139e-08 seconds
  equinox   : 2.622e-07 seconds
  attrs ran
  1.73 times faster than dataclass
  25.06 times faster than equinox
Benchmark Set Property:
  attrs     : 1.0519e-08 seconds
  dataclass : 2.1912e-08 seconds
  attrs ran
  2.08 times faster than dataclass
Benchmark Get Method:
  attrs     : 3.7334e-08 seconds
  dataclass : 4.0077e-08 seconds
  equinox   : 4.1887e-05 seconds
  attrs ran
  1.07 times faster than dataclass
  1121.94 times faster than equinox
```
