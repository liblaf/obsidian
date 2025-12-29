---
date: 2025-12-29T16:40:43+08:00
modified: 2025-12-29T16:49:07+08:00
title: Derivatives of Polar-Decomposition-Based Energy Density
---

## 1. Problem Setup and Notation

We are given the energy density function:

$$
\require{physics}
\Psi(\mathbf{F}) = \norm{\mathbf{F} \mathbf{A} - \mathbf{R}}_F^2 
$$

**Definitions:**
- $\mathbf{F} \in \mathbb{R}^{3 \times 3}$: Deformation gradient (variable).
- $\mathbf{A} \in \mathbb{R}^{3 \times 3}$: Activation matrix (constant, symmetric).
- $\mathbf{G} = \mathbf{F}\mathbf{A}$: The activated deformation gradient.
- Polar Decomposition of $\mathbf{G} = \mathbf{R} \mathbf{S}$ where $\mathbf{R}$ is rotation ($\mathbf{R}^T\mathbf{R}=\mathbf{I}$) and $\mathbf{S}$ is symmetric positive semi-definite.
- Singular Value Decomposition (SVD) of $\mathbf{G}$:
$$
\mathbf{G} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T
$$
$$
\mathbf{R} = \mathbf{U} \mathbf{V}^T, \quad \mathbf{S} = \mathbf{V} \mathbf{\Sigma} \mathbf{V}^T
$$

---

## 2. Proof: Differential of Singular Values

**Proposition:** For a matrix $\mathbf{G}$ with SVD $\mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$, the differential of the singular values $\require{physics} \dd{\sigma_i}$ corresponds to the diagonal elements of the rotated differential matrix $\mathbf{U}^T d\mathbf{G} \mathbf{V}$.

**Proof:**
1. Differentiate the SVD definition $\mathbf{G} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$:
    
$$
 d\mathbf{G} = d\mathbf{U} \mathbf{\Sigma} \mathbf{V}^T + \mathbf{U} d\mathbf{\Sigma} \mathbf{V}^T + \mathbf{U} \mathbf{\Sigma} d\mathbf{V}^T
$$
2. Transform the equation into the eigen-basis by pre-multiplying by $\mathbf{U}^T$ and post-multiplying by $\mathbf{V}$:

$$
 \mathbf{U}^T d\mathbf{G} \mathbf{V} = (\mathbf{U}^T d\mathbf{U}) \mathbf{\Sigma} (\mathbf{V}^T \mathbf{V}) + (\mathbf{U}^T \mathbf{U}) d\mathbf{\Sigma} (\mathbf{V}^T \mathbf{V}) + (\mathbf{U}^T \mathbf{U}) \mathbf{\Sigma} (d\mathbf{V}^T \mathbf{V})
$$
3. Simplify using orthogonality $\mathbf{U}^T\mathbf{U} = \mathbf{I}$:

$$
 \mathbf{U}^T d\mathbf{G} \mathbf{V} = (\mathbf{U}^T d\mathbf{U}) \mathbf{\Sigma} + d\mathbf{\Sigma} + \mathbf{\Sigma} (d\mathbf{V}^T \mathbf{V})
$$
4. **Skew-Symmetry Property:**
    Since $\mathbf{U}^T \mathbf{U} = \mathbf{I}$, differentiating yields $d\mathbf{U}^T \mathbf{U} + \mathbf{U}^T d\mathbf{U} = 0$, implying $\mathbf{U}^T d\mathbf{U} = -(\mathbf{U}^T d\mathbf{U})^T$. Thus, $\mathbf{U}^T d\mathbf{U}$ is skew-symmetric, and its diagonal elements are zero. The same applies to $d\mathbf{V}^T \mathbf{V}$.

1. Examine the diagonal entries (index $ii$):
    Let $\mathbf{M} = \mathbf{U}^T d\mathbf{G} \mathbf{V}$.
    
$$
 M_{ii} = [(\mathbf{U}^T d\mathbf{U}) \mathbf{\Sigma}]_{ii} + [d\mathbf{\Sigma}]_{ii} + [\mathbf{\Sigma} (d\mathbf{V}^T \mathbf{V})]_{ii}
$$
    Since diagonal matrices commute with the diagonal operation and skew-symmetric matrices have zero diagonals:
    
$$
 M_{ii} = 0 + d\sigma_i + 0
$$
**Conclusion:**
$$
 d\sigma_i = (\mathbf{U}^T d\mathbf{G} \mathbf{V})_{ii}
$$
_(Note: If differentiating with respect to input $\mathbf{F}$, then $d\mathbf{G} = d\mathbf{F}\mathbf{A}$)_.

---

## 3. Computation of $d\mathbf{R}$ given $d\mathbf{F}$

To compute the Hessian, we need the differential of the rotation $d\mathbf{R}$ resulting from a perturbation $d\mathbf{F}$.

**Algorithm:**

1. **Compute differential of G:**
    
$$
 d\mathbf{G} = d\mathbf{F} \mathbf{A}
$$
1. **Project into SVD basis:**
    
$$
 \mathbf{M} = \mathbf{U}^T d\mathbf{G} \mathbf{V}
$$
2. **Solve for Rotation parameters in Eigen-space:**
    Let $d\mathbf{R} = \mathbf{U} \tilde{\mathbf{\Omega}} \mathbf{V}^T$, where $\tilde{\mathbf{\Omega}}$ is a skew-symmetric matrix.
    The entries of $\tilde{\mathbf{\Omega}}$ are derived from the off-diagonal entries of $\mathbf{M}$ via the Sylvester equation associated with polar decomposition:
$$
 \tilde{\Omega}_{ij} = \frac{M_{ij} - M_{ji}}{\sigma_i + \sigma_j}
$$
    *Note: For $i=j$, $\tilde{\Omega}_{ii} = 0$.*

1. **reconstruct $d\mathbf{R}$:**
    
$$
 d\mathbf{R} = \mathbf{U} \tilde{\mathbf{\Omega}} \mathbf{V}^T
$$

---

## 4. First Derivative: Gradient $\pdv{\Psi}{\mathbf{F}}$

We compute the First Piola-Kirchhoff stress tensor $\mathbf{P}(\mathbf{F}) = \pdv{\Psi}{\mathbf{F}}$.

1. **Simplify Energy Density:**
    
$$
 \Psi = \tr((\mathbf{G} - \mathbf{R})^T (\mathbf{G} - \mathbf{R})) = \tr(\mathbf{G}^T \mathbf{G}) - 2\tr(\mathbf{R}^T \mathbf{G}) + \tr(\mathbf{I})
$$
1. **Differentiate with respect to $\mathbf{G}$:**
$$
 d\Psi = 2\tr(\mathbf{G}^T d\mathbf{G}) - 2 d(\tr(\mathbf{R}^T \mathbf{G}))
$$
    Using the property that $\tr(d\mathbf{R}^T \mathbf{G}) = \tr(d\mathbf{R}^T \mathbf{R} \mathbf{S}) = 0$ (trace of skew-symmetric $\times$ symmetric is 0):
    
$$
 d\Psi = 2\tr(\mathbf{G}^T d\mathbf{G}) - 2\tr(\mathbf{R}^T d\mathbf{G}) = 2\tr((\mathbf{G} - \mathbf{R})^T d\mathbf{G})
$$
    Thus, $\pdv{\Psi}{\mathbf{G}} = 2(\mathbf{G} - \mathbf{R})$.

2. **Chain Rule to $\mathbf{F}$:**
    Since $\mathbf{G} = \mathbf{F}\mathbf{A}$, we have $d\mathbf{G} = d\mathbf{F}\mathbf{A}$.
    
$$
 d\Psi = \tr\left( 2(\mathbf{G}-\mathbf{R})^T d\mathbf{F} \mathbf{A} \right) = \tr\left( \mathbf{A} 2(\mathbf{G}-\mathbf{R})^T d\mathbf{F} \right)
$$

$$
 d\Psi = \tr\left( \left( 2(\mathbf{G}-\mathbf{R})\mathbf{A}^T \right)^T d\mathbf{F} \right)
$$
1. **Final Result:**
    Using $\mathbf{G} = \mathbf{F}\mathbf{A}$ and symmetric $\mathbf{A}$:
    
$$
 \mathbf{P}(\mathbf{F}) = \pdv{\Psi}{\mathbf{F}} = 2(\mathbf{F}\mathbf{A} - \mathbf{R})\mathbf{A}
$$

---

## 5. Second Derivative: Hessian-Vector Product

Given a perturbation direction $d\mathbf{F}$, we compute the differential of the gradient $d\mathbf{P} = \mathcal{H} : d\mathbf{F}$.

1. **Differentiate $\mathbf{P}$:**
    
$$
 \mathbf{P} = 2\mathbf{F}\mathbf{A}^2 - 2\mathbf{R}\mathbf{A}
$$
$$
 d\mathbf{P} = 2 d\mathbf{F} \mathbf{A}^2 - 2 d\mathbf{R} \mathbf{A}
$$
2. **Computation Steps:**
    Given input $d\mathbf{F}$:
    1. Compute $d\mathbf{G} = d\mathbf{F} \mathbf{A}$.
    2. Compute $\mathbf{M} = \mathbf{U}^T d\mathbf{G} \mathbf{V}$.
    3. Form $\tilde{\mathbf{\Omega}}$ where $\tilde{\Omega}_{ij} = \frac{M_{ij} - M_{ji}}{\sigma_i + \sigma_j}$.
    4. Compute $d\mathbf{R} = \mathbf{U} \tilde{\mathbf{\Omega}} \mathbf{V}^T$.
    5. Compute result:

$$
 d\mathbf{P} = 2 (d\mathbf{F} \mathbf{A} - d\mathbf{R}) \mathbf{A}
$$

---

## 6. Hessian in Tensor Form

The Hessian $\mathcal{H}$ is a rank-4 tensor where $\mathcal{H}_{ijkl} = \frac{\partial P_{ij}}{\partial F_{kl}}$.

From the vector product $d\mathbf{P} = 2 d\mathbf{F} \mathbf{A}^2 - 2 d\mathbf{R} \mathbf{A}$:

1. **First Term ($2 d\mathbf{F} \mathbf{A}^2$):**
    
$$
 (2 d\mathbf{F} \mathbf{A}^2)_{ij} = 2 \sum_p dF_{ip} (\mathbf{A}^2)_{pj}
$$
    In tensor index form: $2 \delta_{ik} (\mathbf{A}^2)_{lj}$.

1. **Second Term ($-2 d\mathbf{R} \mathbf{A}$):**
    This requires the derivative of rotation $\pdv{R_{im}}{F_{kl}}$.
    
$$
 (-2 d\mathbf{R} \mathbf{A})_{ij} = -2 \sum_m dR_{im} A_{mj}
$$
2. **Explicit Tensor Expression:**
    Combining these, the Hessian tensor is:
$$
 \mathcal{H}_{ijkl} = 2 \left( \delta_{ik} (\mathbf{A}^2)_{lj} - \sum_m \pdv{R_{im}}{F_{kl}} A_{mj} \right)
$$
    To evaluate $\pdv{R_{im}}{F_{kl}}$ explicitly without $d\mathbf{F}$, we expand the update rule for $\tilde{\Omega}$:
    
$$
 \pdv{R_{im}}{F_{kl}} = \sum_{a,b} U_{ia} \left( \frac{\partial \tilde{\Omega}_{ab}}{\partial F_{kl}} \right) V_{mb}
$$
    where the term inside the parenthesis is derived from projecting the single-entry matrix basis $\mathbf{E}_{kl}$ through the $\mathbf{M}$-projection and $\sigma$-scaling described in Section 3.
