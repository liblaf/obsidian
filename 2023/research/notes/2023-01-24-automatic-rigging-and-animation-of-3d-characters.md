---
category:
- Reading Notes
- Research
date: '2023-01-24T00:00:00+08:00'
modified: 2025-09-20 21:47:26+08:00
tags:
- Body_Model
title: Automatic Rigging and Animation of 3D Characters
---

## TL;DR

- **Pinocchio**
  - **Input** --- a static character mesh + a generic skeleton
  - **Output** --- adapt skeleton to character and attach it to surface
- **Skeleton Embedding**
  - **Discretization**
    - **Distance Field**
    - **Approximate Medial Surface**
    - **Sphere Packing**
    - **Graph Construction**
  - **Reduced Skeleton**
  - **Discrete Penalty Function**
  - **Embedding Refinement**
- **Skin Attachment** --- attach skeleton to surface

## 3. Skeleton Embedding

### 3.1. Discretization

#### Distance Field

- constructs a kd-tree to evaluate the exact signed **distance to the surface from an arbitrary point**

#### Approximate Medial Surface ==?==

> Pinocchio therefore traverses the octree and for each cell, **looks at a grid ( of spacing $\tau$ ) of points on each face of the cell**. It then **computes the gradient vectors for the cells adjacent to each grid point** --- if the angle between two of them is $\pu{120\degree}$ or greater, it adds the point to the medial surface sample. We impose the $\pu{120\degree}$ condition because we do not want the "noisy" parts of the medial surface --- we want the points where skeleton joints are likely to lie. For the same reason, Pinocchio filters out the sampled points that are too close to the character surface ( within $2 \tau$ ).

#### Sphere Packing

- **sort** the medial surface points **by** their **distance to the surface** ( farthest first )
- if a point is **outside** all previously added spheres
  - add the sphere centered at that point whose radius is the distance to the surface

In other words,

- **largest** spheres are added **first**
- **no sphere contains the center of another sphere**

#### Graph Construction

- **add an edge** between two sphere centers **if the spheres intersect**
- add edges between spheres that do not intersect if that edge is **well inside the surface** and if that edge is **"essential"**

Precise condition

- the **distance** from any point of the edge to the surface must be **at least half of the radius of the smaller sphere**
- the closest sphere centers to the midpoint of the edge must be the edge endpoints

==?== How to construct a rooted tree on $s$ joints

### 3.2. Reduced Skeleton

- all **bone chains are merged** ( all degree-two joints, such as knees, eliminated )

> It can **compute the intermediate joints** by **taking the shortest path** between the endpoints and **splitting it in accordance with the proportions of the unreduced skeleton**.

### 3.3. Discrete Penalty Function

- design penalties **independently**
- **learn a proper weighting** for a global penalty that combines each term

#### The Setup

$$
f(\vb{v}) = \sum_{i = 1}^k \gamma_i b_i(\vb{v})
$$

- $f$ --- penalty function
- $k$ --- number of "basic" penalty functions
- $\Gamma = \pqty{\gamma_1, \dots, \gamma_k}$ --- weights
- $\vb{b}(\vb{v}) = \pqty{b_1(\vb{v}), \dots, b_k(\vb{v})}$ --- feature vector to each example embedding $\vb{v}$
- $\vb{p}_1, \dots, \vb{p}_m$ --- $k$-dimensional feature vectors of **good embeddings**
- $\vb{q}_1, \dots, \vb{q}_m$ --- feature vectors of **bad embeddings**

#### Maximum Margin

> ==?== we want $\Gamma$ to distinguish between the best "bad" embedding and the best "good" embedding

maximize the optimization margin ( subject to $\norm{\Gamma} = 1$ ):

$$
\min_{i = 1}^n \Gamma^T \vb{q}_i - \min_{i = 1}^m \Gamma^T \vb{p}_i
$$

#### Learning Procedure

### 3.4. Discrete Embedding

**branch-and-bound method**

### 3.5. Embedding Refinement

minimize continuous penalty function $g =$ sum of penalty functions over the bones + an asymmetry penalty

$$
g\pqty{q_1, \dots, q_s} = \alpha_A g^A \pqty{q_1, \dots, q_s} + \sum_{i = 2}^s g_i\pqty{q_i, q_{p_S}(i)}
$$

- $p_S$ --- parent function for the unreduced skeleton ( analogous to $p_R$ )
- $g_i = \alpha_S g_i^S + \alpha_L g_i^L + \alpha_O g_i^O$ --- penalizes bones that do not fit inside the surface nicely
  - too short
  - oriented differently from the given skeleton

## 4. Skin Attachment

**Linear Blend Skinning ( LBS )** gives the position of the transformed vertex $j$ as

$$
\sum_i w_j^i \vb{T}^i(\vb{v}_j)
$$

- $\vb{v}_j$ --- position of vertex $j$
- $\vb{T}^i$ --- transformation of the $i$^th^ bone
- $w_j^i$ --- weight of the $i$^th^ bone for vertex $j$

> ==?== Suppose we treat the character volume as an **insulated heat-conducting body** and force the **temperature of bone $i$ to be 1** while keeping the **temperature of all of the other bones at 0**. Then we can **take the equilibrium temperature at each vertex on the surface as the weight of bone $i$** at that vertex.

$$
- \Delta{\vb{w}^i} + \vb{H} \vb{w}^i = \vb{H} \vb{p}^i
$$

- $\Delta$ --- discrete surface Laplacian
- $\vb{p}^i$ --- a vector with $p_j^i = 1$ if the nearest bone to vertex $j$ is $i$ and $p_j^i =  0$ otherwise
- $\vb{H} = c / d(j)^2$ --- the diagonal matrix with $H_{jj}$ being the **heat contribution weight of the nearest bone**
- $d(j)$ --- the distance from vertex $j$ to the nearest bone
