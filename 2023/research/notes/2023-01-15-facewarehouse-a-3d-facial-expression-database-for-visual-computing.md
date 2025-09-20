---
category:
  - Reading Notes
  - Research
date: "2023-01-15T00:00:00+08:00"
tags:
  - Face_Model
title: "FaceWarehouse: a 3D Facial Expression Database for Visual Computing"
---

- <https://ieeexplore.ieee.org/abstract/document/6654137/>
- [[PDF] kunzhou.net](http://kunzhou.net/2012/facewarehouse-tr.pdf)

## TL;DR

- **Building**
  - **Input** --- ( depth maps + color images ) $\cp$ expression $\cp$ identity
  - **Morphable Model** --> meshes
  - **Active Shape Model ( ASM )** --- Expression meshes --> individual-specific blendshape
  - **Multilinear Model**

## Abstract

> We present FaceWarehouse, a database of 3D facial expressions for visual computing applications. We use Kinect, an off-the-shelf RGBD camera, to capture 150 individuals aged 7--80 from various ethnic backgrounds. For each person, we captured the RGBD data of her different expressions, including the neutral expression and 19 other expressions such as mouth-opening, smile, kiss, etc. For every RGBD raw data record, a set of facial feature points on the color image such as eye corners, mouth contour and the nose tip are automatically localized, and manually adjusted if better accuracy is required. We then **deform a template facial mesh to fit the depth data** as closely as possible while matching the feature points on the color image to their corresponding points on the mesh. Starting from these fitted face meshes, we **construct a set of individual-specific expression blendshapes** for each person. These meshes with consistent topology are assembled as a rank-three tensor to build a **bilinear face model** with two attributes, identity and expression. Compared with previous 3D facial databases, for every person in our database, there is a much richer matching collection of expressions, enabling depiction of most human facial actions. We demonstrate the potential of FaceWarehouse for visual computing with four applications: facial image manipulation, face component transfer, real-time performance-based facial image animation, and facial animation retargeting from video to image.

## 3. FaceWarehouse

### 3.1. Data capture

- 2D images + depth maps

### 3.2. Expression mesh and individual-specific blendshape generation

Active Shape Model ( ASM ) --> feature points on color image --> $m_i$ internal feature points + $m_c$ contour feature points

#### Neutral expression

- Blanz and Vetter's morphable model + mesh deformation algorithm

$$
V = \overline{F} + \sum_{i = 1}^l \alpha_i F_i
$$

- $\overline{F}$ --- average face
- $F_i$ --- the $i$-th PCA vector

energy to be minimized for **feature point** matching:

$$
E_{fea}
= \sum_{j = 1}^{m_i} \norm{\vb{v}_{i_j} - \vb{c}_j}^2
  + \sum_{k = 1}^{m_c} \norm{\vb{M}_{proj} \vb{v}_{c_k} - \vb{s}_k}^2
$$

- $c_j$ --- 3D position of the $j$-th feature point
- $\vb{v}_{i_j}$ --- corresponding vertex on the mesh $V$
- $\vb{s}_k$ --- 2D feature point on the color image
- $\vb{v}_{c_k}$ --- corresponding 3D feature vertex on the mesh $V$
- $\vb{M}_{proj}$ --- projection matrix of the camera

energy term for matching the **depth map**:

$$
E_{pos} = \sum_{j = 1}^{n_d} \norm{\vb{v}_{d_j} - \vb{p}_j}^2
$$

- $\vb{v}_{d_j}$ --- a mesh vertex
- $\vb{p}_j$ --- closest point to $\vb{v}_{d_j}$ in the depth map
- $n_d$ --- the number of the mesh vertices

**Tikhonov regularization** energy term:

based on the estimated probability distribution of a shape defined by $\alpha_i$

$$
p\pqty{\alpha} \sim \exp\bqty{- \frac{1}{2} \sum \pqty{\alpha_i / \sigma_i}^2}
$$

- $\sigma_i^2$ --- eigenvalues of the face covariance matrix from PCA

$$
E_{coef} = \frac{1}{2} \alpha^T \Lambda \alpha
$$

- $\Lambda = diag\pqty{1 / \sigma_1^2, 1 / \sigma_2^2, \dots, 1 / \sigma_L^2}$

**total energy**:

$$
E_1 = \omega_1 E_{fea} + \omega_2 E_{pos} + \omega_3 E_{coef}
$$

**Laplacian energy** as the regularization term:

$$
E_{lap} = \sum_{i = 1}^n \norm{L \vb{v}_i - \frac{\delta_i}{\abs{L \vb{v}_i}} L \vb{v}_i}^2
$$

- $L$ --- discrete Laplacian operator
- $\delta_i$ --- magnitude of the original Laplacian coordinate before deformation
- $n$ --- vertex number of the mesh

**mesh deformation energy**:

$$
E_2 = \omega_1' E_{fea} + \omega_2' E_{pos} + \omega_3' E_{lap}
$$

#### Other expressions

- **deformation transfer algorithm**: the deformation from face mesh $S_0$ to $S_i$ mimics the deformation from the guide model $G_0$ to $G_i$
- **mesh deformation algorithm**

#### Individual-specific expression blendshapes

**example-based facial rigging algorithm**

- $\vb{B} = \Bqty{B_0, B_1, \dots, B_{46}}$ --- a neutral face + 46 FACS blendshapes
- $H = B_0 + \sum_{i = 1}^{46} \alpha_i \pqty{B_i - B_0}$ --- an expression
- $\vb{A} = \Bqty{A_0, A_1, \dots, A_{46}}$ --- generic blendshape model

minimize

- difference between each expression mesh $S_j$ and the linear combination of $B_i$ with the known weights for expression $j$
- the difference between the relative deformation from $B_0$ to $B_i$ and that from $A_0$ to $A_i$

### 3.3. ~~Blinear~~ Bilinear face model

assemble the dataset into a rank-three ( 3-mode ) **data tensor $T$** ( 11K vertices $\times$ 150 identities $\times$ 47 expressions )

**$N$-mode SVD** process:

$$
T \cp_2 \vb{U}_{id}^T \cp_3 \vb{U}_{exp}^T = C
$$

- $T$ --- data tensor
- $C$ --- core tensor
- $\vb{U}_{id}, \vb{U}_{exp}$ orthonormal transform matrices, which contain the left singular vectors of the 2nd mode ( identity ) space and 3rd mode ( expression ) space

approximate:

$$
T \simeq C_r \cp_2 \check{\vb{U}}_{id} \cp_3 \check{\vb{U}}_{exp}
$$

- $C_r$ --- reduced core tensor produces by keeping the top-left corner of the original core tensor
- $\check{\vb{U}}_{id}, \check{\vb{U}}_{exp}$ --- truncated matrices from $\vb{U}_{id}$ and $\vb{U}_{exp}$ by removing the trailing columns

$$
V = C_r \cp_2 \vb{w}_{id}^T \cp_3 \vb{w}_{exp}^T
$$

- $C_r$ --- bilinear face model for FaceWarehouse
- $\vb{w}_{id}, \vb{w}_{exp}$ --- column vectors of identity

## 4. Applications

### 4.1. Facial image manipulation

1. learn a linear regression model that **maps a set of user-specified facial attributes to the identity attribute** in the bilinear face model
2. compute the **identity and expression weights** in bilinear face model for the input image
3. **reconstruct a new 3D face mesh** based on these weights

#### Facial feature analysis

**algorithm of multi-variate linear regression** to map attributes to the identity attribute in bilinear face model

- $\vb{w}_{id}$ --- identity weights ( a $k$-D vector )
- $\Bqty{f_1, f_2, \dots, f_l}$ --- $l$ user-specified attributes
- $\vb{M}_{fea}$ --- a $k \times \pqty{l + 1}$ matrix mapping user-specified attributes to the identity weights

$$
M_{fea} \bqty{f_1, \dots, f_l, 1}^T = \vb{w}_{id}
$$

assemble the vectors

- $\vb{W}_{id}$ --- ( $k \times 150$ )
- $\vb{F}$ --- ( $\pqty{l + 1} \times 150$ )
- $\vb{F}^+ = \vb{F}^T \pqty{\vb{F} \vb{F}}^{-1}$ --- left pseudoinverse of $\vb{F}$

$$
\vb{M}_{fea} = \vb{W}_{id} \vb{F}^+
$$

#### Fitting 3D face mesh into image

$$
\vb{p}_k = s \vb{R} \vb{v}_k + \vb{t}
$$

- $\vb{v}_k$ --- scaling factor
- $\vb{R}$ --- 3D rotation matrix
- $\vb{t}$ --- translation vector
- $\vb{v}_k$ --- mesh vertex position
- $\vb{p}_k$ --- projected point position on the image

matching error:

$$
E_k = \frac{1}{2} \norm{s \vb{R} \pqty{C_r \cp_2 \vb{w}_{id}^T \cp_3 \vb{w}_{exp}^T}^{\pqty{k}} + \vb{t} - \vb{s}^{\pqty{k}}}^2
$$

- $\vb{s}^{\pqty{k}}$ --- feature point positions on the image

### 4.2. Face component transfer

As the two input images represent the same person, their identity weights $\vb{w}_{id}^T$ should be the same.

- unified identity weights $\vb{w}_{id}^T$
- expression weights ( $\vb{w}_{exp-1}^T$ and $\vb{w}_{exp-2}^T$ )

$$
E_k^{joint} = \frac{1}{2} \sum_{j = 1}^2 \norm{s_j \vb{R}_j \pqty{C_r \cp_2 \vb{w}_{id}^T \cp_3 \vb{w}_{id}^T}^{\pqty{k}} + \vb{t}_j - \vb{s}_j^{\pqty{k}}}^2
$$

1. use the method described in the last section to compute an **initial estimation** of the identity and expression weights
2. fix $\vb{w}_{exp-1}$ and $\vb{w}_{exp-2}$ and compute $\vb{w}_{id}^T$ by minimizing $E_k^{joint}$
3. $\vb{w}_{exp-1}$ and $\vb{w}_{exp-2}$ are solved separately with $\vb{w}_{id}^T$ fixed
4. step 2, 3 are **performed iteratively** until the fitting results converge

- **2D expression flow**: warp the target face to match the desired expression
- **2D alignment flow**: warp the reference face to an appropriate size and position for transferring
- select a crop region from the warped reference image and blend it to the warped target image

### 4.3. Real-time performance-based facial image animation

construct the expression blendshapes for the person of ientity $\vb{w}_{id}$

$$
B_i = C_r \cp_2 \vb{w}_{id} \cp_3 \pqty{\check{\vb{U}}_{exp} \vb{d}_i}
$$

- $\check{\vb{U}}_{exp}$ --- truncated transform matrix for the expression mode
- $\vb{d}_i$ --- the expression weight vector with value 1 for the $i$-th element and 0 for other elements

generate new expressions

$$
V = B_0 + \sum_{i = 1}^{46} \beta_i \pqty{B_i - B_0}
$$

- real-time performance-based facial animation system to **capture the dynamic expressions** of an arbitrary user
- track the **rigid transformation** of the user's head and the **facial expressions** expressed in the format of blendshapes coefficients $\beta_i$
- hair, teeth

### 4.4 Facial animation retargeting from video to image

- **estimate face identity and expression of the image** using the algorithm described in Section IV-A
- **fit a unified face identity for all frames** using a simple extension of the joint fitting algorithm described in Section IV-B
- **construct expression blendshapes** using the method described in Section IV-C
