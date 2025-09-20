---
category:
  - Posts
title: How To Use More Than 10 Columns in Matrix
date: "2022-04-10T00:00:00+08:00"
tags:
  - LaTeX
---

```latex
\begin{bmatrix}
  v_1 & 1  & 1  & 1  &    &    &    &    &    &    &    \\
  v_2 & -1 &    &    & 1  & 1  &    &    & -1 &    &    \\
  v_3 &    &    &    & -1 &    & 1  & -1 &    & -1 &    \\
  v_4 &    & -1 &    &    &    & -1 & 1  &    &    & -1 \\
  v_5 &    &    & -1 &    & -1 &    &    & 1  & 1  & 1  \\
\end{bmatrix}
```

## Problem

```
Extra alignment tab has been changed to \cr.
<recently read> \endtemplate
```

## Solution[^1]

```latex
\setcounter{MaxMatrixCols}{20} % enables you to use 20 columns
\begin{bmatrix}
  v_1 & 1  & 1  & 1  &    &    &    &    &    &    &    \\
  v_2 & -1 &    &    & 1  & 1  &    &    & -1 &    &    \\
  v_3 &    &    &    & -1 &    & 1  & -1 &    & -1 &    \\
  v_4 &    & -1 &    &    &    & -1 & 1  &    &    & -1 \\
  v_5 &    &    & -1 &    & -1 &    &    & 1  & 1  & 1  \\
\end{bmatrix}
```

## Reference

[^1]: https://tex.stackexchange.com/questions/3519/how-to-use-more-than-10-tab-stops-in-bmatrix-or-other-amsmath-matrix-environment
