---
category:
- Reading Notes
- Research
title: Face Transfer with Multilinear Models
date: '2023-01-14T00:00:00+08:00'
tags:
- Face Model
---

- <https://dl.acm.org/doi/abs/10.1145/1185657.1185864>
- [[PDF] harvard.edu](https://dash.harvard.edu/bitstream/handle/1/4238955/Vlasic_Face.pdf?sequence=2&isAllowed=y)

## TL;DR

- **Multilinear Models**
- **Formula** --- See [Sec. 4](#_4-multilinear-face-model)
- **Building**
  - **Input** --- Motion Capture ( vertices $\cp$ ( $\cp$ visemes ) expressions $\cp$ identities )
  - **Correspondence** --- Meshes --> Scan ( See [Sec. 4.2](#_4-2-correspondence) )
  - **Missing Data** --- See [Sec. 4.4](#_4-4-missing-data)
  - **Method** --- SVD
- **Face Transfer**
  - **Input** --- Video Data
  - **Face Tracking** ( See [Sec. 5.1](#_5-1-face-tracking) )
  - **Initialization**

## Abstract

> Face Transfer is a method for mapping video recorded performances of one individual to facial animations of another. It extracts visemes (speech-related mouth articulations), expressions, and three-dimensional (3D) pose from monocular video or film footage. These parameters are then used to generate and drive a detailed 3D textured face mesh for a target identity, which can be seamlessly rendered back into target footage. The underlying face model automatically adjusts for how the target performs facial expressions and visemes. The performance data can be easily edited to change the visemes, expressions, pose, or even the identity of the target—the attributes are separably controllable. This supports a wide variety of video rewrite and puppetry applications.
>
> Face Transfer is based on a multilinear model of 3D face meshes that separably parameterizes the space of geometric variations due to different attributes (e.g., identity, expression, and viseme). Separability means that each of these attributes can be independently varied. A multilinear model can be estimated from a Cartesian product of examples (identities $\times$ expressions $\times$ visemes) with techniques from statistical analysis, but only after careful preprocessing of the geometric data set to secure one-to-one correspondence, to minimize cross-coupling artifacts, and to fill in any missing examples. Face Transfer offers new solutions to these problems and links the estimated model with a face-tracking algorithm to extract pose, expression, and viseme parameters.

## 1. Introduction

- multilinear model decouples the three attributes
- separability & consistency

## 3. Multilinear Algebra

#### Tensors

$$
\mathscr{T} = \pqty{t_{i_1 i_2 \dots i_N}}
$$

#### Mode Spaces

#### Mode-$n$ Product

- $\mathscr{T}$ --- tensor
- $\vb{M}$ --- matrix

$\mathscr{T} \cp_n \vb{M}$ indicates a linear transformation of vectors in $\mathscr{T}$'s mode-n space by the matrix $\vb{M}$. $\mathscr{T} \cp_2 \vb{M}$ would replace each mode-2 vector $\vb{v}$ with a transformed vector $\vb{M} \vb{v}$.

#### Tensor Decomposition

$$
\begin{align*}
                        & \mathscr{T}\cp_1 \vb{U}_1^{\top} \cp_2 \vb{U}_2^{\top} \cp_3 \vb{U}_3^{\top} \dots \cp_N \vb{U}_N^{\top} = \mathscr{C} \\
  \Longrightarrow \quad & \mathscr{T} = \mathscr{C} \cp_1 \vb{U}_1 \cp_2 \vb{U}_2 \cp_3 \vb{U}_3 \dots \cp_N \vb{U}_N
\end{align*}
$$

- $\mathscr{T}$ --- data tensor
- $\mathscr{C}$ --- core tensor
- $\vb{U}_i$ --- orthonormal matrix whose columns contain left singular vectors of the $i$-th mode space, and can be computes via SVD

$$
\mathscr{T} \simeq \mathscr{C}_{reduces} \cp_1 \check{\vb{U}}_1 \cp_2 \check{\vb{U}}_2 \cp_3 \check{\vb{U}}_3 \dots \cp_N \check{\vb{U}}_N
$$

- $\check{\vb{U}}_i$ --- truncated versions of $\vb{U}_i$ with last few columns removed

## 4. Multilinear Face Model

### 4.1. Face Data

#### Bilinear model

vertices $\times$ expressions $\times$ identities

#### Trilinear model

vertices $\times$ visemes $\times$ expressions $\times$ identities

### 4.2. Correspondence

manually specified 42 reference points

1. **align** the template and the scan
2. **deform** the template mesh into the scan
   1. at first, weighing the **marked correspondences** heavily
   2. afterward emphasizing **vertex proximity**

### 4.3. Face Model

$$
\begin{equation}
  \mathscr{T} \simeq \mathscr{M} \cp_2 \check{\vb{U}}_2 \cp_3 \check{\vb{U}}_3 \dots \cp_N \check{\vb{U}}_N
  \label{eq:4}
\end{equation}
$$

$$
\vb{f} = \mathscr{M} \cp_2 \vb{w}_2^{\top} \cp_3 \vb{w}_3^{\top} \dots \cp_N \vb{W}_N^{\top}
$$

- $\mathscr{M}$ --- **multilinear model** of face geometry
- $\vb{w}_i$ --- a column vector of parameters ( weights ) for the attribute corresponding to $i^{th}$ mode
- $\vb{f}$ --- a column vector of vertices describing the resulting face

### 4.4. Missing Data

#### Description

1. For each model we assemble an **incomplete** matrix whose columns are the corresponding mode vectors. We then seek a subspace decomposition that best reconstructs the known values of that matrix. ( PPCA )
2. The linear constraints are combined through the missing elements, because they are shared across all groups of modal vectors and must be filled in with consistent values. To that end, we **collect linear equations that determine a particular missing value in all the modes, and solve them together**.

#### Evaluation

#### Probabilistic Interpretation

$$
\mathscr{T} = \mathscr{M} \cp_2 \check{\vb{U}}_2 \cp_3 \check{\vb{U}}_3 \dots \cp_N \check{\vb{U}}_N + \nu
$$

- $\mathscr{T}, \mathscr{M}$ --- data and model tensors
- $\check{\vb{U}}_i$ --- the $i$-th modal subspace
- $\nu$ --- a Gaussian noise source

$$
p\pqty{\mathscr{T} \vert \mathscr{M}, \Bqty{\check{\vb{U}}_i}_{i = 2}^N}
\approx \prod_{j = 2}^N q_j\pqty{\mathscr{T}, \mathscr{M}, \Bqty{\check{\vb{U}}_i}_{i = 2}^N}^{1 / N}
$$

Each Gaussian $q_j\pqty{\mathscr{T}, \mathscr{M}, \Bqty{\check{\vb{U}}_i}_{i = 2}^N} \doteq \mathscr{N}\pqty{\mathscr{T} \vert \check{\vb{U}}_j \vb{J}_j, \sigma_j^2}$ is found by fixing $\Bqty{\check{\vb{U}}_j}_{i \neq j}$ and turning the tensor Equation $\eqref{eq:4}$ into matrix form: $\vb{T}_j = \check{\vb{U}}_j \vb{J}_j$. Here, columns of $\vb{T}_j$ are the mode-$j$ vectors of $\mathscr{T}$, and the columns of $\vb{J}_j$ are the mode-$j$ vectors of $\mathscr{M} \cp_2 \check{\vb{U}}_2 \dots \cp_{j - 1} \check{\vb{U}}_{j - 1} \cp_{j + 1} \check{\vb{U}}_{j + 1} \dots \cp_N \check{\vb{U}}_N$. The resulting likelihood becomes:

$$
p\pqty{\mathscr{T} \vert \mathscr{M}, \Bqty{\check{\vb{U}}_i}_{i = 2}^N}
\approx \prod_{j = 2}^N \mathscr{N}\pqty{\mathscr{T} \vert \check{\vb{U}}_j \vb{J}_j, \sigma_j^2}^{1 / N}
$$

Taking logarithms and discarding constant factors, we seek to minimize the sum-squared error

$$
\sum_{j = 2}^N \norm{\vb{T}_j - \check{\vb{U}}_j \vb{J}_j}_F^2
$$

Each term of the summation presents a matrix factorization problem with missing values, where $\check{\vb{U}}_j$ and $\vb{J}_j$ are treated as unknown factors of the incomplete matrix $\vb{T}_j$, and are solved for using PPCA.

## 5. Face Transfer

### 5.1. Face Tracking

**optical flow** + **weak-perspective camera model**

Using the symmetric Kanade-Lucas-Tomasi formulation, we express the frame-to-frame motion of a tracked point with a linear system:

$$
\vb{Z} \vb{d} = \vb{Z} \pqty{\vb{p} - \vb{p}_0} = \vb{e}
$$

- $\vb{d}$ --- describe the image-space motion of the point
- $\vb{p}$ --- the point's true location
- $\vb{p}_0$ --- its current best guess ( location from the previous frame if no guess )
- matrix $\vb{Z}$, vector $\vb{e}$ --- contain spatial and temporal intensity gradient information in the surrounding region

Using a weak-perspective imaging model, the point position $\vb{p}$ can be expanded in terms of rigid head-motion parameters and non-rigid facial shape parameters, which are constrained by the multilinear model:

$$
\begin{equation}
  \vb{Z} \pqty{s \vb{R} \vb{f}_i + \vb{t} - \vb{p}_0} = \vb{e}
  \label{eq:7}
\end{equation}
$$

- $s$ --- scale factor
- $\vb{R}$ --- 3D rotation matrix
- $\vb{t}$ --- image-space translation
- $\vb{f}_i$ --- the $i$-th 3D vertex being tracked

Solving for the pose and all the multilinear weights from a pair of frames using Equation $\eqref{eq:7}$ is not a well-constrained problem. To simplify the computation, we use a **coordinate-descent method**: we let only one of the face attributes vary at a time by fixing all the others to their current guesses. This transforms the multilinear problem into a linear one.

$$
\vb{Z} \pqty{s \vb{R} \vb{M}_{m, i} \vb{w}_m + \vb{t} - \vb{p}_0} = \vb{e}
$$

- $m$ --- the mode corresponding to non-fixed attribute

- $\vb{w}_m$ --- a vector of weights for that attribute

- $\vb{M}_{m, i}$ --- corresponding linear basis for the tracked vertex $i$ obtained from

  $$
  \vb{M}_m = \mathscr{M} \cp_2 \vb{w}_2^{\top} \dots \cp_{\pqty{m - 1}} \vb{w}_{\pqty{m - 1}}^{\top} \cp_{\pqty{m + 1}} \vb{w}_{\pqty{m + 1}}^{\top} \dots \cp_N \vb{w}_N^{\top}
  $$

- If the currently tracked attribute **varies** from frame to frame ( e.g. expression ), we solve the set of linear systems and proceed to the next pair of neighboring frames.
- If the attribute is **constant** across all frames ( e.g. identity ), we accumulate the mentioned linear systems from each pair of frames and solve them together as one combined system.

### 5.2. Initialization

- specify a small number of feature points which are then used to position the face geometry
- correspondences: user-provided or automatically detected

## 8. Conclusion

- estimate a highly detailed face model from an incomplete set of face scans
- **multilinear model**
- **separability**: different attributes, such as identity and expression, can be manipulated independently
