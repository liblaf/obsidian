---
category:
- Course Work
layout: Slide
reveal:
  width: 1440
title: Exploration and Practice in Software Engineering (2)
date: '2023-03-28T00:00:00+08:00'
tags:
- Exploration and Practice in Software Engineering (2)
---

@slidestart

## Exploration and Practice in Software Engineering (2)

> 2023-03-28

---

### Deformation Transfer

--

#### x64 `12th Gen Intel(R) Core(TM) i7-1260P (16)`

| Task               | Iterations | Time             | Kernel Time |
| ------------------ | ---------- | ---------------- | ----------- |
| `s1 -> t1`         | `131072`   | `0:01:12.125142` | `40.411 s`  |
| `u0 -> u0-aligned` | `4096`     | `0:00:03.423797` | `1.429 s`   |
| `s1 -> u1-aligned` | `131072`   | `0:01:20.373831` | `44.751 s`  |
| `all`              |            | `2m44s`          |             |

--

#### cuda `NVIDIA GeForce RTX 3090`

| Task               | Iterations | Time             | Kernel Time |
| ------------------ | ---------- | ---------------- | ----------- |
| `s1 -> t1`         | `131072`   | `0:01:25.160106` | `9.193 s`   |
| `u0 -> u0-aligned` | `4096`     | `0:00:06.077657` | `0.453 s`   |
| `s1 -> u1-aligned` | `131072`   | `0:01:23.951527` | `8.746 s`   |
| `all`              |            | `3m18s`          |             |

---

### Tiny Mesh Viewer

--

#### Develop Environment

- Build System: `CMake`
- Dependencies: `boost-signals2`, `cxxopts`, `glad`, `glfw3`, `glm`, `openmesh`, `spdlog`
- Documentation: `Doxygen`
- Editor: `VS Code`
- Language Server: `clangd`
- Package Manager: `vcpkg`
- Sanitizers: `ASan`, `UBSan`
- Static Analysis: `clang-tidy`
- Style: `clang-format` (Based on Google), `cpplint`
- Toolchain: `LLVM/Clang-15`

--

#### Gouraud & Phong Shading

- Gouraud: compute color in **Vertex Shader**
- Phong: compute color in **Fragment Shader**

--

#### Shaders (Phong)

- Vertex Shader:
  - IN: `Pos`, `Normal`
  - OUT: `FragPos`, `Normal` (`gl_Position`)
- Fragment Shader:
  - IN: `FragPos`, `Normal`
  - OUT: `Color`

@slideend
