---
date: 2024-10-24T22:13:20+08:00
modified: 2025-09-20T18:39:39+08:00
tags:
  - Programming/Python
title: "Comparing `lazy-loader` and `etils.epy`: A Deep Dive into Lazy Loading and API Exports"
---

In the world of Python development, optimizing import times and managing large codebases can be challenging. Two popular tools that aim to address these challenges are [lazy-loader](https://github.com/scientific-python/lazy-loader) and [etils.epy](https://github.com/google/etils). This blog post will compare these two libraries, focusing on their capabilities for lazy loading and lazy API exports. We'll explore their features, use cases, and how they can be integrated into your projects.

## Introduction

Lazy loading is a technique that delays the import of modules until they are actually needed. This can significantly reduce the initial load time of a package, especially for large libraries with many submodules. `lazy-loader` and `etils.epy` both provide mechanisms for lazy loading, but they approach the problem differently.

`lazy-loader` is a utility library designed to make it easier for projects to implement lazy loading of submodules and functions. It is part of the Scientific Python ecosystem and is endorsed by several core projects.

`etils.epy`, on the other hand, is a part of the `etils` library, which offers a collection of utilities for Python. It provides context managers for lazy imports and API exports, making it a versatile tool for managing imports in complex projects.

## Lazy Loading

### Comparison of Lazy Loading Methods

| Method               | Typing Friendly | Absolute Imports | Relative Imports |
| -------------------- | --------------- | ---------------- | ---------------- |
| `lazy.load()`        | NO              | YES              | NO               |
| `epy.lazy_imports()` | YES             | YES              | NO               |

### Demonstration of Lazy Loading Methods

::: tabs

@tab lazy.load()

```python
import lazy_loader as lazy

# Lazy load the 'numpy' module
np = lazy.load("numpy")

def myfunc():
    # The actual import happens here
    np.array([1, 2, 3])
```

@tab epy.lazy_imports()

```python
import etils.epy as epy

with epy.lazy_imports():
    import numpy as np

def myfunc():
    # The actual import happens here
    np.array([1, 2, 3])
```

:::

## Lazy API Exports

### Comparison of Lazy API Export Methods

| Method                   | Typing Friendly | Absolute Imports | Relative Imports | Compatible with [Sphinx AutoAPI](https://github.com/readthedocs/sphinx-autoapi) |
| ------------------------ | --------------- | ---------------- | ---------------- | ------------------------------------------------------------------------------- |
| `lazy.attach()`          | NO              | NO               | YES              | NO                                                                              |
| `lazy.attach_stub()`     | YES             | NO               | YES              | NO                                                                              |
| `epy.lazy_api_imports()` | YES             | YES              | NO               | NO                                                                              |

### Demonstration of Lazy API Export Methods

::: tabs

@tab lazy.attach()

```python
import lazy_loader as lazy

submodules = ['filters']
__getattr__, __dir__, __all__ = lazy.attach(__name__, submodules)
```

@tab lazy.attach_stub()

```python
import lazy_loader as lazy

# Assuming there is a `.pyi` file adjacent to this module
__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)
```

@tab epy.lazy_api_imports()

```python
import etils.epy as epy

with epy.lazy_api_imports(globals()):
    from my_project import Obj1
    from my_project import OtherObj
    from my_project import my_function
```

:::

## Conclusion

Both `lazy-loader` and `etils.epy` offer powerful tools for managing imports in Python projects. `lazy-loader` is particularly well-suited for projects that need to optimize import times and provide explicit submodule exports. It is widely adopted in the Scientific Python ecosystem and offers a straightforward way to implement lazy loading.

`etils.epy`, on the other hand, provides a more flexible approach with context managers for both lazy imports and API exports. It is ideal for projects that require more dynamic import management and can benefit from the additional control provided by context managers.

When choosing between these libraries, consider the specific needs of your project, including the complexity of your import structure and the level of control you require over the import process. Both libraries have their strengths and can significantly enhance the performance and maintainability of your Python code.

By leveraging the power of lazy loading and lazy API exports, you can create more efficient and user-friendly Python packages that cater to the needs of both developers and end-users.
