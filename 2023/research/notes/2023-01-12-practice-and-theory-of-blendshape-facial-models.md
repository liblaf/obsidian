---
category:
- Reading Notes
- Research
date: '2023-01-12T00:00:00+08:00'
tags:
- Face_Model
title: Practice and Theory of Blendshape Facial Models
---

[[PDF] scribblethink.org](http://www.scribblethink.org/Work/Pdfs/blendshapes_MAIN.pdf)

## TL;DR

- focus on **expression**
- interpretable
- **Blendshapes** --- $\vb{f} = \vb{b}_0 + \vb{B} \vb{w}$

## Introduction

blendshapes: simple, expressive, interpretable

advantages of blendshapes:

- Blendshapes are a **semantic parameterization**.
- To some extent blendshapes force the animator to stat "on model", that is, arbitary deformations are not possible.

## 1. Terminology

- **blendshape targets / morph targets**: individual basis vectors
- **sliders**: weights of blendshape targets
- **morphable model**: linear facial model, focus on identity, underlying basis is orthogonal

## 3. Algebra and Algorithms

- $n$ --- # of blendshapes
- $p$ --- # of vertices
- $\vb{b}_k$ --- By "unrolling" the numbers composing each blendshape into a long vector $\vb{b}_k$ in some order that is arbitary ( such as xxxyyyzzz, or alternately xyzxyzxyz )
- $\vb{f}$ --- resulting face, in the form of a $(m = 3 p) \times 1$ vector
- $\vb{B}$ --- a $(m = 3 p) \times n$ matrix whose column vectors, $\vb{b}_k$, are the individual blendshapes
- $\vb{w}$ --- weights ( a $n \times 1$ vector )

**blendshape model** is expressed as

$$
\vb{f} = \sum_{k = 0}^n w_k \vb{b}_k = \vb{B} \vb{w}
$$

### 3.1. Delta blendshape formulation

$$
\vb{f}
= \vb{b}_0 + \sum_{k = 1}^n w_k \pqty{\vb{b}_k - \vb{b}_0}
= \vb{b}_0 + \vb{B} \vb{w}
$$

- $\vb{b}_0$ --- neutral shape

### 3.2. Intermediate shapes

allow targets to be situated at intermediate weight values

### 3.3. Combination blendshapes

$$
\begin{equation*}
  \begin{split}
    \vb{f} & = \vb{f}_0 + \vb{b}_1 w_1 + \vb{b}_2 w_2 + \vb{b}_3 w_3 + \dots          \\
           & \qquad \; + \: \vb{b}_{1, 5} w_1 w_5 + \vb{b}_{2, 13} w_2 w_{13} + \dots \\
           & \qquad \; + \: \vb{b}_{2, 3, 10} w_2 w_3 w_{10} + \dots
  \end{split}
\end{equation*}
$$

- A term $\vb{b}_{1, 5} w_1 w_5$ is a bilinear "correction" shape.
- The combination blendshape scheme is not ideal from an interpolation point of view.

### 3.4. Hybrid rigs

In a bendshape model the jaw and neck are sometimes handled by alternate approaches.

## 4. Constructing Blendshapes

## 5. Animation and Interaction Techniques

### 5.1. Keyframe animation

### 5.2. Performance-driven animation

### 5.3. Expression cloning

### 5.4. Partially-automated animation

### 5.5 Direct manipulation

#### 5.5.1 Direct manipulation of PCA models

#### 5.5.2 Direct manipulation of blendshapes

### 5.6. Further interaction techniques

## 6. Facial Animation as an Interpolation Problem

### 6.1. Linear interpolation

### 6.2. Blendshapes as a high dimensional interpolation problem

### 6.3. Blendshapes as a tangent space

$$
f\pqty{\vb{w}}
= f\pqty{0} + \pdv{\vb{f}}{\vb{w}} \vdot \vb{w}
= \vb{b}_0 + \vb{B} \vb{w}
$$

## 7. The Blendshape Parameterization

### 7.1. Lack of orthogonality

### 7.2. Blendshape models are not unique

### 7.3. Equivalence of whole-face and delta blendshape formulations

### 7.4. Global versus local control

### 7.5. Convex combination of shapes

$$
\begin{align*}
  \sum_{k = 1}^n w_k & = 1                                \\
  w_k                & \geqslant 0, &  & \text{for all $k$}
\end{align*}
$$

### 7.6. Semantic parameterization

### 7.7. PCA is not interpretable

### 7.8. Conversion between blendshape and PCA representations

- $\vb{U}, \vb{c}$ --- PCA eigenvectors and coefficients
- $\vb{f}_0, \vb{e}_0$ --- neutral face and mean face

$$
\vb{B} \vb{w} + \vb{f}_0 = \vb{U} \vb{c} + \vb{e}_0
$$

$$
\begin{gather*}
  \vb{w} = \pqty{\vb{B}^T \vb{B}}^{-1} \vb{B}^T \pqty{\vb{U} \vb{c} + \vb{e}_0 - \vb{f}_0} \\
  \vb{c} = \pqty{\vb{U}^T \vb{U}}^{-1} \vb{U}^T \pqty{\vb{B} \vb{w} + \vb{f}_0 - \vb{e}_0}
\end{gather*}
$$

### 7.9. Probability of a blendshape expression

- $\vb{f}$ --- vector representing the face
- $\vb{u}_i$ --- eigenvector
- $\lambda_i$ --- eigenvalue

$$
\begin{equation*}
  \begin{split}
    \mathbb{E}\bqty{c_i^2}
     & = \mathbb{E}\bqty{\vb{u}_i^T \vb{f} \vb{f}^T \vb{u}_i}                              \\
     & = \vb{u}_i^T \mathbb{E}\bqty{\vb{f} \vb{f}^T} \vb{u}_i = \vb{u}_i^T \vb{C} \vb{u}_i \\
     & = \vb{u}_i^T \lambda_i \vb{u}_i                                                     \\
     & = \lambda_i \qq{because $\norm{\vb{u}_i} = 1$}
  \end{split}
\end{equation*}
$$

$$
P\pqty{\vb{c}} = \exp(\sum_i \frac{c_i^2}{\lambda_i}) = \exp(- \vb{c}^T \Lambda^{-1} \vb{c})
$$

### 7.10. Compressing blendshapes

## 8. Further Applications

### 8.1. Model transfer

### 8.2. Blendshape refinement

### 8.3. Discovery of blendshapes

### 8.4. Alternatives and related techniques
