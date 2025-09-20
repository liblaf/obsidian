---
category:
- Reading Notes
- Research
date: '2023-04-06T00:00:00+08:00'
tags:
- Face_Model
title: 'SCULPTOR: Skeleton-Consistent Face Creation Using a Learned Parametric Generator'
---

| Model                |     Parametric     |       Skull        |        Face        | Anatomically Consistent |       Shape        |        Pose        |     Expression     |     Appearance     |       Trait        |
| -------------------- | :----------------: | :----------------: | :----------------: | :---------------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: |
| [Madsen et al. 2018] | :white_check_mark: | :white_check_mark: | :white_check_mark: |   :white_check_mark:    | :white_check_mark: |        :x:         |        :x:         |        :x:         |        :x:         |
| [Gruber et al. 2020] | :white_check_mark: | :white_check_mark: | :white_check_mark: |           :x:           | :white_check_mark: |        :x:         |        :x:         |        :x:         |        :x:         |
| [Ichim et al. 2017]  |        :x:         | :white_check_mark: | :white_check_mark: |           :x:           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |
| [Li et al. 2020]     |        :x:         |        :x:         | :white_check_mark: |           :x:           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |
| [Li et al. 2017]     | :white_check_mark: |        :x:         | :white_check_mark: |           :x:           | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |        :x:         |
| SCULPTOR (Ours)      | :white_check_mark: | :white_check_mark: | :white_check_mark: |   :white_check_mark:    | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |

## 4. Building LUCY

### 4.1. Data Acquisition and Original Usage

- 72 individual subject head CT image pairs (pre and post-surgery)
  - image spatial resolution $\pu{0.48 \times 0.48 \times 1 mm^3}$
- multi-view face appearance scans

### 4.2. Data Labeling

- raw CT data -- specialists segment with thresholding method and morphological operations --> separated **mandible**, **maxilla** volume and the **facial outer surface**
- apply ICT[^1] to align **multi-view scans** to the facial soft tissues captured in **CT**
- 29 skeleton and 15 face surface **semantic landmarks** for model registration

[^1]: P.J. Besl and Neil D. McKay. 1992. A method for registration of 3-D shapes. IEEE Transactions on Pattern Analysis and Machine Intelligence 14, 2 (1992), 239–256. https://doi.org/10.1109/34.121791

## 5. SCULPTOR Model

### 5.1. Model Formulation

- $\mathcal{G}$ --- geometry for both skeleton and face
- $\mathcal{A}$ --- face appearance
- $\theta$ --- pose parameters (PCA coefficient vector of pose space)
- $\beta$ --- shape parameters
- $\gamma$ --- trait parameters
- $\phi$ --- expression parameters
- $\alpha$ --- appearance parameters
- $LBS(\cdot)$ --- Linear Blend Skinning (LBS) function
- $\mathcal{W}$ --- **learned** skinning weight ( for LBS )
- $\vb{T}_p$ --- person-specific head mesh with variation over the general template $\overline{\vb{T}}$
- $\overline{\vb{T}}$ --- general head template (outer surface + mandible + maxilla)
- $J_p$ --- anatomical joint location for jaws
- $\mathcal{J}$ --- a sparse matrix that computes joint location from personalized skull vertices with shape $B_S$ and trait $B_D$ components (defined by experienced surgeons)
- $B_*$ --- component

$$
\mathcal{M}(\theta, \beta, \gamma, \phi, \alpha) = \Bqty{\mathcal{G}(\theta, \beta, \gamma, \alpha), \mathcal{A}(\alpha)}
$$

$$
\mathcal{G}(\theta, \beta, \gamma, \alpha) = LBS(\mathcal{W}, J_p(\beta, \gamma), \vb{T}_p(\beta, \gamma, \theta, \phi))
$$

$$
J_p(\beta, \gamma) = \mathcal{J}(\overline{\vb{T}} + B_S(\beta; \mathcal{S}) + B_D(\gamma; \mathcal{D}))
$$

$$
\vb{T}_p(\beta, \gamma, \theta, \phi) = \overline{\vb{T}} + B_S(\beta; \mathcal{S}) + B_D(\gamma; \mathcal{D}) + B_P(\theta; \mathcal{P}) + B_E(\phi, \mathcal{E})
$$

$$
\overline{\vb{T}} = \Bqty{\overline{\vb{T}}_{mdb}, \overline{\vb{T}}_{mxl}, \overline{\vb{T}}_f}
$$

$$
B_D(\gamma; \mathcal{D}) = \mathcal{D} \gamma
$$

### 5.2. Registration

#### Registration on skull

1. skull template $\overline{\vb{T}}_S = \Bqty{\overline{\vb{T}}_{mdb}, \overline{\vb{T}}_{mxl}}$ and CT skull $\vb{C}_S$ are roughly aligned using **Procrustes rigid alignment on landmark correspondences**

2.

3.

4. use embedded deformation to recover skull details

   1. sample control nodes $x \in \mathcal{N}$ on the template surface with interval $\sigma$

   2. $$
      v' = \sum_{x \in \mathcal{N}} w(x, v) M v
      $$

      - $M$ --- transformation of node $x$
      - $w(\cdot)$ --- influence weight of node $x$ on $v$ (Radial Basis Function[^2])
      - $CD(\cdot)$ --- Chamfer Distance[^3] between two meshes
      - $CD_n(\cdot)$ --- computes the angle between the corresponding vertex normal, adds a normal penalty

      $$
      E_{rskull} = E_d + \lambda_l E_{lmk} + \lambda_r E_{reg}
      $$

      $$
      E_d = \lambda_d CD(\overline{\vb{T}}_S', \vb{C}_S) + (1 - \lambda_d) CD_n(\overline{\vb{T}}_s', \vb{C}_S)
      $$

5.

[^2]: Taehyun Rhee, J.P. Lewis, Ulrich Neumann, and Krishna Nayak. 2007. Soft-Tissue Deformation for In Vivo Volume Animation. In 15th Pacific Conference on Computer Graphics and Applications (PG'07). 435–438. https://doi.org/10.1109/PG.2007.46

#### Registration on face

$$
E_{rface} = E_d(\overline{\vb{T}}_f, \vb{C}_f) + \lambda_l E_{lmk} + \lambda_{lap} E_{lap}
$$

### 5.3. Parameter Learning

- train model parameters --- $\Bqty{\overline{\vb{T}}, \mathcal{S}, \mathcal{D}, \mathcal{W}, \mathcal{P}}$

#### Learning on LUCY

- train $\Bqty{\overline{\vb{T}}, \mathcal{S}, \mathcal{D}}$
- we compute $\mathcal{D}$ by performing PCA on the vertex offset of pre- and post-surgery data by $d_i = \vb{T}_{post}^i - \vb{T}_{pre}^i$ to model the trait component.

#### Learning on FaceScape

- train $\Bqty{\mathcal{W}, \mathcal{P}}$

#### Optimization Summary

- **alternatively** optimize the parameters on two different datasets

## Notes
