---
category:
  - Reading Notes
  - Research
date: 2023-05-18T08:00:00+08:00
modified: 2025-09-20T23:07:38+08:00
tags:
  - Physics
  - Projective_Dynamics
title: "Projective Dynamics: Fusing Constraint Projections for Fast Simulation"
---

## Formula

$$
G = \frac{E}{2 (1 + \nu)}
$$

- $G$ --- shear modulus[^1]
- $E$ --- Young's modulus
- $\nu$ --- Poisson's ratio

[^1]: [Shear modulus - Wikipedia](https://en.wikipedia.org/wiki/Shear_modulus)

### Energy

$$
W(\vb{q}, \vb{T}) = \frac{w}{2} A \norm{\vb{X}_f \vb{X}_g^{-1} - \vb{T}}_F^2
$$

- $W$ --- potential energy
- $w$ (aka. $G$) --- shear modulus
- (constant) $A$ --- triangle area / tetrahedron volume
- $\vb{X}_f = \bmqty{\vb{q}_{0, 1, 2} - \vb{q}_3}$ --- deformed shape
- (constant) $\vb{X}_g = \bmqty{\tilde{\vb{q}}_{0, 1, 2} - \tilde{\vb{q}}_3}$ --- undeformed shape
- (auxiliary) $\vb{T}$ --- rotation matrix

### Force

$$
\vb{f}_{i}
= \pdv{W(\vb{q}, \vb{T})}{\vb{q}_i}
= w A \pqty{\vb{X}_f \vb{X}_g^{-1} - \vb{T}} \odot \pqty{\pdv{\vb{X}_f}{\vb{q}_i} \vb{X}_g^{-1}}
$$

- $\vb{f}$ --- force
- (variable) $\vb{q}$ --- deformed position

### Hessian Matrix

$$
\vb{H}_{ij}
= \pdv{f_i}{\vb{q}_j}
= w A \pqty{\pdv{\vb{X}_f}{\vb{q}_j} \vb{X}_g^{-1}} \odot \pqty{\pdv{\vb{X}_f}{\vb{q}_i} \vb{X}_g^{-1}}
$$

- $\vb{H}$ --- Hessian matrix

::: tip
$\vb{H}$ is constant. The non-zero values of $\vb{H}_{ij}$ only appear in cases when $\vb{q}_i$ and $\vb{q}_j$ are both located within the same tetrahedron.
:::

## Detailed Formula

### Force

$$
f_{a i}
= \pdv{W}{q_{a i}}
= w A \pqty{\vb{X}_f \vb{X}_g^{-1} - \vb{T}} \odot \pqty{\pdv{\vb{X}_f}{q_{a i}} \vb{X}_g^{-1}}
$$

- $i = 0, 1, 2, 3$ --- id of vertex
- $a = x, y, z$ --- axis

$$
\vb{X}_f =
\begin{bmatrix}
  q_{x 0} - q_{x 0} & q_{x 0} - q_{x 0} & q_{x 0} - q_{x 0} \\
  q_{y 0} - q_{y 0} & q_{y 0} - q_{y 0} & q_{y 0} - q_{y 0} \\
  q_{z 0} - q_{z 0} & q_{z 0} - q_{z 0} & q_{z 0} - q_{z 0}
\end{bmatrix}
$$

$$
\pqty{\pdv{\vb{X}_f}{q_{a i}}}_{l m} = 1 \iff i = 0, 1, 2 \qc a = x, y, z \qc l = a \qc m = i \\
\pqty{\pdv{\vb{X}_f}{q_{a i}}}_{l m} = -1 \iff i = 3 \qc a = x, y, z \qc l = a \qc m = 0, 1, 2
$$

Therefore, when $i = 0, 1, 2$

$$
\begin{equation*}
  \begin{split}
    f_{a i}
     & = \sum_{l n} w A \pqty{\vb{X}_f \vb{X}_g^{-1} - \vb{T}}_{l n} \pqty{\pdv{\vb{X}_f}{q_{0 x}} \vb{X}_g^{-1}}_{l n}                \\
     & = \sum_{l m n} w A \pqty{\vb{X}_f \vb{X}_g^{-1} - \vb{T}}_{l n} \pqty{\pdv{\vb{X}_f}{q_{0 x}}}_{l m} \pqty{\vb{X}_g^{-1}}_{m n} \\
     & = \sum_n w A \pqty{\vb{X}_f \vb{X}_g^{-1} - \vb{T}}_{a n} \pqty{\vb{X}_g^{-1}}_{i n}                                            \\
     & = \sum_n w A \pqty{\vb{X}_f \vb{X}_g^{-1} - \vb{T}}_{a n} \pqty{\vb{X}_g^{-T}}_{n i}
  \end{split}
\end{equation*}
$$

$$
\bmqty{\vb{f}_0 & \vb{f}_1 & \vb{f}_2} = f_{a i} = w A \pqty{\vb{X}_f \vb{X}_g^{-1} - \vb{T}} \vb{X}_g^{-T}
$$

### Hessian Matrix

When $i, j = 0, 1, 2$

$$
\begin{equation*}
  \begin{split}
    H_{a i b j}
     & = \sum_{l n} w A \pqty{\pdv{\vb{X}_f}{q_{a i}} \vb{X}_g^{-1}}_{l n} \pqty{\pdv{\vb{X}_f}{q_{b j}} \vb{X}_g^{-1}}_{l n}                                              \\
     & = \sum_{l m n k} w A \pqty{\pdv{\vb{X}_f}{q_{a i}}}_{l m} \pqty{\vb{X}_g^{-1}}_{m n} \pqty{\pdv{\vb{X}_f}{q_{b j}}}_{l k} \pqty{\vb{X}_g^{-1}}_{k n}                \\
     & = \sum_n w A \pqty{\pdv{\vb{X}_f}{q_{a i}}}_{a i} \pqty{\vb{X}_g^{-1}}_{i n} \pqty{\pdv{\vb{X}_f}{q_{b j}}}_{b j} \pqty{\vb{X}_g^{-1}}_{j n} \quad \pqty{l = a = b} \\
     & = \sum_n w A \pqty{\vb{X}_g^{-1}}_{i n} \pqty{\vb{X}_g^{-T}}_{n j}
  \end{split}
\end{equation*}
$$

$$
\vb{H} = H_{i j} = w A \vb{X}_g^{-1} \vb{X}_g^{-T}
$$

When $i = 0, 1, 2 \qc j = 3$

$$
\begin{equation*}
  \begin{split}
    H_{a i b j}
     & = \sum_{l n} w A \pqty{\pdv{\vb{X}_f}{q_{a i}} \vb{X}_g^{-1}}_{l n} \pqty{\pdv{\vb{X}_f}{q_{b j}} \vb{X}_g^{-1}}_{l n}                                                  \\
     & = \sum_{l m n k} w A \pqty{\pdv{\vb{X}_f}{q_{a i}}}_{l m} \pqty{\vb{X}_g^{-1}}_{m n} \pqty{\pdv{\vb{X}_f}{q_{b j}}}_{l k} \pqty{\vb{X}_g^{-1}}_{k n}                    \\
     & = \sum_{n k} w A \pqty{\pdv{\vb{X}_f}{q_{a i}}}_{a i} \pqty{\vb{X}_g^{-1}}_{i n} \pqty{\pdv{\vb{X}_f}{q_{b j}}}_{b k} \pqty{\vb{X}_g^{-1}}_{k n} \quad \pqty{l = a = b} \\
     & = \sum_{n k} - w A \pqty{\vb{X}_g^{-1}}_{i n} \pqty{\vb{X}_g^{-T}}_{n k}
  \end{split}
\end{equation*}
$$

$$
H_{i 3} = \sum_{k} - w A \pqty{\vb{X}_g^{-1} \vb{X}_g^{-T}}_{i k}
$$

When $i = j = 3$

$$
\begin{equation*}
  \begin{split}
    H_{a i b j}
     & = \sum_{l n} w A \pqty{\pdv{\vb{X}_f}{q_{a i}} \vb{X}_g^{-1}}_{l n} \pqty{\pdv{\vb{X}_f}{q_{b j}} \vb{X}_g^{-1}}_{l n}                                                    \\
     & = \sum_{l m n k} w A \pqty{\pdv{\vb{X}_f}{q_{a i}}}_{l m} \pqty{\vb{X}_g^{-1}}_{m n} \pqty{\pdv{\vb{X}_f}{q_{b j}}}_{l k} \pqty{\vb{X}_g^{-1}}_{k n}                      \\
     & = \sum_{m n k} w A \pqty{\pdv{\vb{X}_f}{q_{a i}}}_{a m} \pqty{\vb{X}_g^{-1}}_{m n} \pqty{\pdv{\vb{X}_f}{q_{b j}}}_{b k} \pqty{\vb{X}_g^{-1}}_{k n} \quad \pqty{l = a = b} \\
     & = \sum_{m n k} w A \pqty{\vb{X}_g^{-1}}_{m n} \pqty{\vb{X}_g^{-T}}_{n k}
  \end{split}
\end{equation*}
$$

$$
H_{3 3} = \sum_{m k} - w A \pqty{\vb{X}_g^{-1} \vb{X}_g^{-T}}_{m k}
$$

## Solver

$$
\vb{s}_n = \vb{q}_n + h \vb{v}_n + h^2 \vb{M}^{-1} \vb{f}
$$

- $h$ (aka. $\Delta{t}$) --- time step
- $\vb{M}$ --- mass matrix

$$
\begin{align*}
   & \text{For} \ k = 0 \dots K                                                                                                                                 \\
   & \quad \text{Solve} \pqty{\frac{1}{h^2} \vb{M} + \vb{H}} \Delta{\vb{q}} = - \frac{1}{h^2} \vb{M} \pqty{\vb{q}^{(k)} - \vb{s}_n} + \vb{f}\pqty{\vb{q}^{(k)}} \\
   & \quad \vb{q}^{(k + 1)} \leftarrow \vb{q}^{(k)} + \Delta{\vb{q}}                                                                                            \\
   & \vb{q}_{n + 1} = \vb{q}^{(k + 1)}                                                                                                                          \\
   & \vb{v}_{n + 1} = (\vb{q}_{n + 1} - \vb{q}_{n}) / h
\end{align*}
$$

### Conjugate gradient method

- used to solve $\vb{A} \vb{x} = \vb{b}$
- $\vb{A} = \frac{1}{h^2} \vb{M} + \vb{H}$
- $\vb{b} = - \frac{1}{h^2} \vb{M} \pqty{\vb{q}^{(k)} - \vb{s}_n} + \vb{f}\pqty{\vb{q}^{(k)}}$

$$
\begin{align*}
   & \vb{r}_0 = \vb{b} - \vb{A} \vb{x}_0                                                                                                                \\
   & \text{if $\vb{r_0}$ is sufficiently small, then return $\vb{x}_0$ as the result}                                                                   \\
   & \vb{p}_0 = \vb{r}_0                                                                                                                                \\
   & \text{repeat}                                                                                                                                      \\
   & \qquad \alpha_k = \frac{\vb{r}_k^T \vb{r}_k}{\vb{p}_k^T \vb{A} \vb{p}_k} = \frac{\vb{r}_k \vdot \vb{r}_k}{\vb{p}_k \vdot \vb{A} \vb{p}_k}          \\
   & \qquad \vb{x}_{k + 1} = \vb{x}_k + \alpha_k \vb{p}_k                                                                                               \\
   & \qquad \vb{r}_{k + 1} = \vb{r}_k - \alpha_k \vb{A} \vb{p}_k                                                                                        \\
   & \qquad \text{if $\vb{r}_{k + 1}$ is sufficiently small, then exit loop}                                                                            \\
   & \qquad \beta_k = \frac{\vb{r}_{k + 1}^T \vb{r}_{k + 1}}{\vb{r}_k^T \vb{r}_k} = \frac{\vb{r}_{k + 1} \vdot \vb{r}_{k + 1}}{\vb{r}_k \vdot \vb{r}_k} \\
   & \qquad \vb{p}_{k + 1} = \vb{r}_{k + 1} + \beta_k \vb{p}_k                                                                                          \\
   & \qquad k = k + 1                                                                                                                                   \\
   & \text{end repeat}                                                                                                                                  \\
   & \text{return $\vb{x}_{k + 1}$ as the result}
\end{align*}
$$
