---
category:
- Reading Notes
- Research
date: '2023-01-26T00:00:00+08:00'
tags:
- Body_Model
title: 'SCAPE: Shape Completion and Animation of People'
---

## TL;DR

- **Pose Deformation**
  - **Input** --- mesh, align with template, different poses of a human
  - **Params** --- pose deformation ( twist vector )
  - **Output** -- mesh
- **Body Deformation**
  - **Input** --- mesh, different individuals
  - **Params** --- body deformation ( PCA )
  - **Output** -- mesh

## 3. Acquiring and Processing Data Meshes

#### Range Scanning

#### Correspondence

#### Non-rigid Registration

#### Recovering the Articulated Skeleton

#### Data Format and Assumptions

## 4. Pose Deformation

### 4.1. Deformation Process

$$
v_{k, j}^i = R_{\ell[k]}^i Q_k^i \hat{v}_{k, j} \qc j = 2, 3
$$

- ( input ) $Y^i$ --- mesh in the data set containing different poses of a human
- ( input ) $p_k$ --- triangle of the template
- ( input ) $x_{k, 1}, x_{k, 2}, x_{k, 3}$ --- points of triangle $p_k$
- ( input ) $\hat{v}_{k, j}^i = x_{k, j} - x_{k, 1} \qc j = 2, 3$ --- triangle edges
- ( params ) $Q_k^i$ --- $3 \times 3$ linear transformation matrix
- ( input ) $R_{\ell}^i$ --- rotation of the polygon's rigid part in the articulated skeleton
- ( input ) $\ell[k]$ --- body part associated with triangle $p_k$

> However, the **predictions for the edges** in different triangles **are rarely consistent**. Thus, to construct a single coherent mesh, we solve for the location of the points $y_1, \dots, y_M$ that **minimize** the overall least squares error:

$$
\mathop{\mathrm{argmin}}_{y_1, \dots, y_M} \sum_k \sum_{j = 2, 3} \norm{R_{\ell[k]}^i Q_k^i \hat{v}_{j, k} - \pqty{y_{j, k} - y_{1, k}}}^2
$$

### 4.2. Learning the Pose Deformation Model

$$
\begin{align*}
  t & = \frac{\norm{\theta}}{2 \sin{\norm{\theta}}} \bmqty{m_{32} - m_{23} \\ m_{13} - m_{31} \\ m_{21} - m_{12}} \\
  \qq{with} \theta & = \cos^{-1}\pqty{\frac{\mathop{\mathrm{tr}}(M) - 1}{2}}
\end{align*}
$$

- ( analogous to $Q_k^i$ ) $M$ --- any $3 \times 3$ rotation matrix
- $m_{ij}$ --- $M$'s $i$-th row and $j$-th column
- $t$ --- twist for the joint angle, a 3D vector
  - direction of $t$ --- axis of rotation
  - magnitude of $t$ --- rotation amount

predicts the transformation matrices $Q_k^i$ as a function of the twists of its two nearest joints $\Delta{r_{\ell[k]}^i} = \pqty{\Delta{r_{\ell[k], 1}^i}, \Delta{r_{\ell[k], 2}^i}}$

$$
q_{k, l m}^i = \vb{a}_{k, l m}^T \vdot \begin{bmatrix}
\Delta{r_{\ell[k]}^i} \\
1\\
\end{bmatrix} \quad
l, m = 1, 2, 3
$$

- ( params ) $\vb{a}_{k, l m}$ --- $7 \times 1$ regression vector

$$
Q_k^i = \mathscr{Q}_{\vb{a}_k}\pqty{\Delta{r_{\ell[k]}^i}}
$$

$$
\mathop{\mathrm{argmin}}_{\vb{a}_{k, l m}} \sum_i \pqty{\bmqty{\Delta{r}^i & 1} \vb{a}_{k, l m} - q_{k, l m}^i}^2
$$

$$
\mathop{\mathrm{argmin}}_{\Bqty{Q_1^i, \dots, Q_P^i}} \sum_k \sum_{j = 2, 3} \norm{R_k^i Q_k^i \hat{v}_{k, j} - v_{k, j}}^2 + w_s \sum_{k_1, k_2 \text{ adj}} I(\ell_{k_1} = \ell_{k_2}) \vdot \norm{Q_{k_1}^i - Q_{k_2}^i}^2
$$

- ( input ) $w_s = 0.001 \rho$
- ( input ) $\rho$ --- resolution of the model mesh $X$
- $I(\cdot)$ --- indicator function

## 5. Body-Shape Deformation

### 5.1. Deformation Process

$$
v_{k, j}^i = R_{\ell[k]}^i S_k^i Q_k^i \hat{v}_{k, j}
$$

- $S^i = \Bqty{S_k^i : k = 1, \dots, P}$ --- model the body deformation associated with subject $i$

### 5.2. Learning the Shape Deformation Model

PCA:

$$
S^i = \mathscr{S}_{U, \mu}\pqty{\beta^i} = \overline{U \beta^i + \mu}
$$

- ( params ) $S^i$ --- $9 \times N$

$$
\mathop{\mathrm{argmin}}_{S^i} \sum_k \sum_{j = 2, 3} \norm{R_k^i S_k^i Q_k^i \hat{v}_{k, j}^i - v_{k, j}^i}^2 + w_s \sum_{k_1, k_2 \text{ adj}} \norm{S_{k_1}^i - S_{k_2}^i}^2
$$

## 6. Shape Completion

## 7. Partial View Completion

## 8. Motion Capture Animation
