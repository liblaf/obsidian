---
category:
- Reading Notes
- Research
date: '2023-02-14T00:00:00+08:00'
modified: 2025-09-20 21:47:50+08:00
tags:
- Face_Model
- Physics
title: 'Phace: Physics-based Face Modeling and Animation'
---

## 1. Introduction

### Contributions

- a novel muscle activation model that offers more flexibility than standard fiber-based models
- a physics-based simulation method that retains realism even with significant external forces or substantial modifications of the face geometry and tissue material properties
- an inverse modeling optimization to adapt the simulation template to a series of expression scans of a specific person.

### Overview

![Schematic workflow of our method.](https://cdn.liblaf.me/img/2023/2023-02-24T051425Z.png)

![Our template model consists of a volumetric representation of the tissue and bones (a), and a surface blendshape basis to represent the expression space (d). Muscles are embedded into a non-conforming tetrahedral mesh discretization (b). We explicitly model jaw kinematics with a 5 DoF joint (c) and utilize low-resolution geometry proxies for faster collision detection for the teeth region (e). Dynamic skin sliding is supported by introducing both sliding (green) and fixed (red) constraints for bone-tissue connections (f).](https://cdn.liblaf.me/img/2023/2023-02-24T051500Z.png)

## 3. Template Face Model

- generic face model --- an anatomical face template corresponding to an average human subject ( see Figure above )
  - polygonal representations of the **bones**, **skin**, and 33 facial **muscles**
  - generate a tetrahedral mesh discretizing the **soft tissue** ( two types ) of the face
    - **active** --- muscles
    - **passive** --- subcutaneous fat, connective tissue and the skin

### Jaw kinematics

- see Figure (c) above
- DoF ( degree of freedom ) = 5
- $\vb{b} \in \mathbb{R}^5$ --- kinematic parameters of the jaw bone

### Template blendshapes

- defined on the skin as a basis for parametrizing the space of facial expressions
- provide no information about the internal deformations

## 4. Forward Physics

### Passive tissue

$$
\begin{equation} \label{eq:1}
  E_{\text{pass}}(\vb{x}) = \sum_i \min_{\vb{R}_i \in SO(3)} W_i^{\text{pass}} \mu \norm{\vb{F}_i(\vb{x}) - \vb{R}_i}_F^2 + W_i^{\text{pass}} \lambda (\det(\vb{F}_i(x)) - 1)^2
\end{equation}
$$

- $E_{\text{pass}}(\vb{x})$ --- deformation energy
- ( params ) $\vb{x}$ --- a vector stacking all degrees of freedom of the soft tissue
- ( input ) $i$ --- index goes over all tets
- ( input ) $W_i^{\text{pass}} \geqslant 0$ --- volume of the $i$-th tetrahedron that is occupied by passive tissue, pre-computed during template construction with Monte-Carlo sampling
- first term --- commonly used co-rotated elasticity ( measure of deviation from rigid motion )
- second term --- resistance to changes of volume
- $\vb{F}_i(\vb{x})$ --- deformation gradient
- ( params ) $\vb{R}_i$ --- auxiliary rotation matrix used in co-rotated model
- $\mu, \lambda$ --- material parameters

### Active tissue

> Muscles can generate only internal forces. In other words, **an isolated muscle is not capable of translating or rotating by itself** (even though the muscle can of course be translated or rotated due to contact with the surrounding tissues).

- no translation --- translation invariance of the deformation gradient operator $\vb{F}_i(\vb{x})$
- no rotation --- activation to be a **symmetric** $3 \times 3$ matrix
  - $\vb{Q} \vb{\Lambda} \vb{Q}^T$ --- eigendecomposition
    - $\vb{Q} \in SO(3)$ --- orthonormal coordinate system
    - $\vb{\Lambda} \in \mathbb{R}^3$ --- diagonal, non-uniform scaling
  - $\vb{a}_i \in \mathbb{R}^6$ --- activation vector
  - $\mathcal{S}: \mathbb{R}^6 \to \mathbb{R}^{3 \times 3}$ --- linear operator to generate the corresponding symmetric matrix $\mathcal{S}(\vb{a}_i) \in \mathbb{R}^{3 \times 3}$

> Muscles are approximately incompressible, which means $\det(\mathcal{S}(\vb{a}_i)) = \det(\vb{Q} \vb{\Lambda} \vb{Q}^T) = \det(\vb{\Lambda})$ should be close to 1. However, to compensate for discretization errors, we do not enforce $\det(\mathcal{S}(\vb{a}_i)) = 1$ strictly, but only as a soft constraint, as discussed in Section 5.

$$
\begin{equation} \label{eq:2}
  E_{\text{act}}(\vb{x}, \vb{a}) = \sum_i \min_{\vb{R}_i \in SO(3)} W_i^{\text{act}} \mu \norm{\vb{F}_i(\vb{x}) - \vb{R}_i \mathcal{S}(\vb{a}_i)}^2 + W_i^{\text{act}} \lambda (\det(\vb{F}_i(\vb{x}) - \det(\mathcal{S}(\vb{a}_i))))^2
\end{equation}
$$

- $E_{\text{act}}(\vb{x}, \vb{a})$ --- deformation energy
- ( params ) $\vb{a}$ --- a vector stacking the 6-dimensional activation parameters for all active tets
- $i$ --- index goes over all tets
- ( input ) $W_i^{\text{act}} \geqslant 0$ --- volume of the $i$-th tet that corresponds to active tissue
- co-rotated term --- find the rotation $\vb{R}_i$ that **best aligns** the deformation gradient $\vb{F}_i(\vb{x})$ with $\mathcal{S}(\vb{a}_i)$
- second term --- encourage the volume ratio of the deformed tet ( i.e. $\det(\vb{F}_i(\vb{x}))$ ) to align with the volume ratio of the activation matrix $\det(\mathcal{S}(\vb{a}_i))$, which should be close to 1, i.e., **volume conserving**.

### Bone attachments

> To distinguish areas where soft tissue is **directly attached to the bones** from areas where soft tissue **slides over the bones**, we create two types of constraints:

- pin constraints --- Dirichlet boundary conditions
- sliding constrains --- point-on-plane constraints

$$
c(\vb{x}, \vb{b}) = 0
$$

- $\vb{b} \in \mathbb{R}^5$ --- kinematic parameters of the jaw bone

### Quasi-static solution

$$
\begin{equation} \label{eq:3}
  \begin{aligned}
     & \mathop{\text{minimize}}_x &  & E_{\text{pass}}(\vb{x}) + E_{\text{act}}(\vb{x}, \vb{a}) + E_{\text{grav}}(\vb{x}) \\
     & \text{subject to}          &  & c(\vb{x}, \vb{b}) = 0 \qc \vb{p}(\vb{x}) \geqslant 0,
  \end{aligned}
\end{equation}
$$

- $E_{\text{grav}}(\vb{x})$ --- gravitational potential ( $m g h$ )
- inequality constraints $\vb{p}(\vb{x})$ --- resolve penetrations ( collision response )

> When collision detection finds a surface vertex penetrating the volumetric face model ( see below for more details ), an inequality constraint is appended to $\vb{p}$. For each offending vertex we find its projection onto the surface and create a tangent plane at this point. The inequality constraint requires the vertex to be at the half-space opposite the volume.

### Collisions - implementation details

> Because the geometry of the teeth is quite detailed ( and we are not aspiring to simulate e.g. flossing where the detail would be necessary ), we start by creating **proxy collision shapes** for the upper and lower teeth ( see Figure 3-e ).

> detect collisions using AABB hierarchies

## 5. Inverse Physics

### Optimization formulation

$$
\begin{equation} \label{eq:4}
  \begin{aligned}
     & \min_{\vb{x}, \vb{a}, \vb{b}} &  & \norm{\vb{S} \vb{x} - \vb{T} \vb{t}}^2 + R_{\text{act}}(\vb{a}) + R_{\text{sparse}}(\vb{a})                                            \\
     & \text{subj. to}               &  & c(\vb{x}, \vb{b}) = 0 \qc \vb{p}(\vb{x}) \geqslant 0                                                                                   \\
     &                               &  & \grad_{\vb{x}}{E_{\text{pass}}(\vb{x})} + \grad_{\vb{x}}{E_{\text{act}}(\vb{x}, \vb{a})} + \grad_{\vb{x}}{E_{\text{grav}}(\vb{x})} = 0
  \end{aligned}
\end{equation}
$$

- $\vb{b}$ --- bone parameters
- $\vb{a}$ --- muscle activations
- $\vb{t}$ --- target vertex positions of the skin
- $\norm{\vb{S} \vb{x} - \vb{T} \vb{t}}^2$ --- how close state $\vb{x}$ is to the target $\vb{t}$
- matrix $\vb{S}$ --- selects the simulation nodes corresponding to the skin surface
- $\vb{S}, \vb{T}$ --- encode both position ( point-to-point ) and point-to-plane distance terms
- last vector equality --- sum of all forces ( gradient with respect to $\vb{x}$ ) is zero

### Regularization

$$
R_{\text{act}}(\vb{a}) = \sum_{i, m} f_{i, m} \norm{Q_i^T \begin{bmatrix}
                                                              \gamma_{m(i)}^{-1} & 0                    & 0                    \\
                                                              0                  & \sqrt{\gamma_{m(i)}} & 0                    \\
                                                              0                  & 0                    & \sqrt{\gamma_{m(i)}}
                                                            \end{bmatrix} Q_i - \mathcal{S}(\vb{a}_i)
}^2
$$

$$
R_{\text{sparse}}(\vb{a}) = \sum_m \sqrt{\sum_i f_{i, m} \norm{\vb{a}_i}^2}
$$

### Numerical solution

## 6. Phace Modeling and Animation

### Model Building

- input --- 3D scan of subject in neutral expression and about 5-10 additional premeditated facial expressions
- Each of the scans is approximately **aligned with the skin of our template model** (Section 3) using **rigid registration** (plus uniform scale).
- Then we apply non-rigid ICP to find **dense correspondences between the template skin and the target scan**, guided with a few manually chosen markers as shown in the inset.
  - $\vb{s}_{\text{neut}}$ --- registered neutral skin surface
  - $\vb{s}_k$ --- registered $k$-th expression skin surface
- **deform volumetric template model** such that its boundary ( skin ) **aligns** with $\vb{s}_{\text{neut}}$ ( with Anatomy Transfer )
- **solve** for **activations** $\vb{a}_j$ and **jaw bone parameters** $\vb{b}_j$ that correspond to each of the **blendshapes** $\vb{c}_j$ using the **Inverse Physics** optimization of Section 5

### Animation

- input --- per-frame blendshape weights $\vb{w} = \Bqty{w_1, \dots, w_{48}}$
- compute muscle activations as $\vb{a} = \vb{a}_{\text{neut}} + \sum_j \vb{w}_j (\vb{a}_j - \vb{a}_{\text{neut}})$
- compute the blended jaw kinematics parameters $\vb{b} = \sum_j w_j \vb{b}_j$

### Dynamics

augmenting the objective of Eq. $\eqref{eq:3}$ with the term:

$$
\frac{1}{2} \norm{\vb{x} - (\vb{x}_n + h \vb{v}_n)}_{\vb{M}}^2
$$

- $\vb{x}_n, \vb{v}_n$ --- positions and velocities in the previous frame
- $h > 0$ --- time step
- $\vb{M}$ --- mass matrix

### Plasticity

$$
\vb{F}_{\text{total}}(\vb{x}) = \vb{F}_{\text{elast}}(\vb{x}) \vb{F}_{\text{plast}}
$$

- $\vb{F}_{\text{total}}(\vb{x})$ --- total deformation gradient
