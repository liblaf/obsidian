---
date: 2025-12-29T16:40:43+08:00
modified: 2025-12-29T17:14:40+08:00
title: Derivatives of Polar-Decomposition-Based Energy Density
---

$$
\require{physics}
$$

## 1. Problem Setup and Notation

We are given the energy density function:

$$
\Psi(\vb{F}) = \norm{\vb{F} \vb{A} - \vb{R}}_F^2 
$$

**Definitions:**
- $\vb{F} \in \mathbb{R}^{3 \times 3}$: Deformation gradient (variable).
- $\vb{A} \in \mathbb{R}^{3 \times 3}$: Activation matrix (constant, symmetric).
- $\vb{G} = \vb{F}\vb{A}$: The activated deformation gradient.
- Polar Decomposition of $\vb{G} = \vb{R} \vb{S}$ where $\vb{R}$ is rotation ($\vb{R}^T\vb{R}=\vb{I}$) and $\vb{S}$ is symmetric positive semi-definite.
- Singular Value Decomposition (SVD) of $\vb{G}$:
$$
\vb{G} = \vb{U} \vb{\Sigma} \vb{V}^T
$$
$$
\vb{R} = \vb{U} \vb{V}^T, \quad \vb{S} = \vb{V} \vb{\Sigma} \vb{V}^T
$$

## 2. Proof: Differential of Singular Values

**Proposition:** For a matrix $\vb{G}$ with SVD $\vb{U} \vb{\Sigma} \vb{V}^T$, the differential of the singular values $\dd{\sigma_i}$ corresponds to the diagonal elements of the rotated differential matrix $\vb{U}^T \dd{\vb{G}} \vb{V}$.

**Proof:**

1. Differentiate the SVD definition $\vb{G} = \vb{U} \vb{\Sigma} \vb{V}^T$:
$$
\dd{\vb{G}} = \dd{\vb{U}} \vb{\Sigma} \vb{V}^T + \vb{U} \dd{\vb{\Sigma}} \vb{V}^T + \vb{U} \vb{\Sigma} \dd{\vb{V}}^T
$$
2. Transform the equation into the eigen-basis by pre-multiplying by $\vb{U}^T$ and post-multiplying by $\vb{V}$:
$$
\vb{U}^T \dd{\vb{G}} \vb{V} = (\vb{U}^T \dd{\vb{U}}) \vb{\Sigma} (\vb{V}^T \vb{V}) + (\vb{U}^T \vb{U}) \dd{\vb{\Sigma}} (\vb{V}^T \vb{V}) + (\vb{U}^T \vb{U}) \vb{\Sigma} (\dd{\vb{V}}^T \vb{V})
$$
3. Simplify using orthogonality $\vb{U}^T\vb{U} = \vb{I}$:
$$
\vb{U}^T \dd{\vb{G}} \vb{V} = (\vb{U}^T \dd{\vb{U}}) \vb{\Sigma} + \dd{\vb{\Sigma}} + \vb{\Sigma} (\dd{\vb{V}}^T \vb{V})
$$
4. **Skew-Symmetry Property:**
Since $\vb{U}^T \vb{U} = \vb{I}$, differentiating yields $\dd{\vb{U}}^T \vb{U} + \vb{U}^T \dd{\vb{U}} = 0$, implying $\vb{U}^T \dd{\vb{U}} = -(\vb{U}^T \dd{\vb{U}})^T$. Thus, $\vb{U}^T \dd{\vb{U}}$ is skew-symmetric, and its diagonal elements are **zero**. The same applies to $\dd{\vb{V}}^T \vb{V}$.
5. Examine the diagonal entries (index $ii$): Let $\vb{M} = \vb{U}^T d\vb{G} \vb{V}$.
$$
M_{ii} = [(\vb{U}^T \dd{\vb{U}}) \vb{\Sigma}]_{ii} + [\dd{\vb{\Sigma}}]_{ii} + [\vb{\Sigma} (\dd{\vb{V}}^T \vb{V})]_{ii}
$$
Since diagonal matrices commute with the diagonal operation and skew-symmetric matrices have zero diagonals:
$$
M_{ii} = 0 + \dd{\sigma_i} + 0
$$

**Conclusion:**
$$
\dd{\sigma_i} = (\vb{U}^T \dd{\vb{G}} \vb{V})_{ii}
$$

_(Note: If differentiating with respect to input $\vb{F}$, then $\dd{\vb{G}} = \dd{\vb{F}} \vb{A}$)._

## 3. Computation of $\dd{\vb{R}}$ given $\dd{\vb{F}}$

The computation of the differential of the rotation matrix $\dd{\vb{R}}$ relies on solving a Sylvester equation derived from the polar decomposition constraint.

### 3.1. Differentiating the Polar Decomposition

We start with the relationship $\vb{G} = \vb{R} \vb{S}$. Differentiating both sides yields:
$$
\dd{\vb{G}} = \dd{\vb{R}} \vb{S} + \vb{R} \dd{\vb{S}} 
$$

Multiplying by $\vb{R}^T$ on the left:
$$
\vb{R}^T \dd{\vb{G}} = (\vb{R}^T \dd{\vb{R}}) \vb{S} + \dd{\vb{S}} 
$$

We define the angular velocity matrix in the body frame as $\vb{\Omega} = \vb{R}^T \dd{\vb{R}}$. Since $\vb{R}$ is orthogonal ($\vb{R}^T\vb{R} = \vb{I}$), $\vb{\Omega}$ is **skew-symmetric** ($\vb{\Omega}^T = -\vb{\Omega}$).
$$
\vb{R}^T \dd{\vb{G}} = \vb{\Omega} \vb{S} + \dd{\vb{S}} 
$$

### 3.2. Projecting into the Eigen-Basis

Solving for $\vb{\Omega}$ directly is difficult because it is coupled with $\vb{S}$. We simplify the equation by projecting it into the eigen-basis of $\vb{S}$ (which is the basis $\vb{V}$ from the SVD).

Pre-multiply by $\vb{V}^T$ and post-multiply by $\vb{V}$:
$$
\vb{V}^T (\vb{R}^T \dd{\vb{G}}) \vb{V} = \vb{V}^T (\vb{\Omega} \vb{S}) \vb{V} + \vb{V}^T \dd{\vb{S}} \vb{V} 
$$

Let us define the transformed matrices:
1. **Projected Differential:** Using $\vb{R} = \vb{U}\vb{V}^T$, the LHS becomes:
$$
\vb{M} \equiv \vb{V}^T \vb{V} \vb{U}^T \dd{\vb{G}} \vb{V} = \vb{U}^T \dd{\vb{G}} \vb{V}
$$
2. **Rotated Angular Velocity:** $\tilde{\vb{\Omega}} \equiv \vb{V}^T \vb{\Omega} \vb{V}$. Since $\vb{\Omega}$ is skew-symmetric, $\tilde{\vb{\Omega}}$ remains skew-symmetric.
3. **Symmetric Term:** $\vb{D} \equiv \vb{V}^T \dd{\vb{S}} \vb{V}$. Since $\vb{S}$ is symmetric, $\dd{\vb{S}}$ and consequently $\vb{D}$ are symmetric.

Substituting $\vb{S} = \vb{V} \vb{\Sigma} \vb{V}^T$ into the equation:
$$
\vb{M} = (\vb{V}^T \vb{\Omega} \vb{V}) (\vb{V}^T \vb{S} \vb{V}) + \vb{D}
$$
$$
\vb{M} = \tilde{\vb{\Omega}} \vb{\Sigma} + \vb{D}
$$

### 3.3. Solving the System

We now have the equation $\vb{M} = \tilde{\vb{\Omega}} \vb{\Sigma} + \vb{D}$ expressed in components:
$$
M_{ij} = \sum_k \tilde{\Omega}_{ik} \Sigma_{kj} + D_{ij}
$$
Since $\vb{\Sigma}$ is diagonal ($\Sigma_{kj} = \delta_{kj} \sigma_j$):
$$
M_{ij} = \tilde{\Omega}_{ij} \sigma_j + D_{ij} \quad \text{(Equation 1)}
$$
We need to eliminate $D_{ij}$. We look at the transposed component $M_{ji}$:
$$
M_{ji} = \tilde{\Omega}_{ji} \sigma_i + D_{ji}
$$
Using the properties that $\tilde{\vb{\Omega}}$ is skew-symmetric ($\tilde{\Omega}_{ji} = -\tilde{\Omega}_{ij}$) and $\vb{D}$ is symmetric ($D_{ji} = D_{ij}$):
$$
M_{ji} = -\tilde{\Omega}_{ij} \sigma_i + D_{ij} \quad \text{(Equation 2)}
$$
Subtracting (Equation 2) from (Equation 1) eliminates $D_{ij}$:
$$
M_{ij} - M_{ji} = \tilde{\Omega}_{ij} \sigma_j - (-\tilde{\Omega}_{ij} \sigma_i)
$$
$$
M_{ij} - M_{ji} = \tilde{\Omega}_{ij} (\sigma_i + \sigma_j)
$$
Thus, the off-diagonal elements are:
$$
\tilde{\Omega}_{ij} = \frac{M_{ij} - M_{ji}}{\sigma_i + \sigma_j}
$$
For diagonal elements, $\tilde{\Omega}_{ii} = 0$ by definition of skew-symmetry.

### 3.4. Reconstructing $\dd{\vb{R}}$

We found $\tilde{\vb{\Omega}}$, which represents the rotation change in the basis $\vb{V}$. We must transform this back to the global frame to find $\dd{\vb{R}}$.

From the definition $\tilde{\vb{\Omega}} = \vb{V}^T \vb{\Omega} \vb{V}$, we invert to get $\vb{\Omega} = \vb{V} \tilde{\vb{\Omega}} \vb{V}^T$.
From $\vb{\Omega} = \vb{R}^T \dd{\vb{R}}$, we have $\dd{\vb{R}} = \vb{R} \vb{\Omega}$.

Substitute $\vb{R} = \vb{U}\vb{V}^T$:
$$
 \dd{\vb{R}} = (\vb{U}\vb{V}^T) (\vb{V} \tilde{\vb{\Omega}} \vb{V}^T) = \vb{U} (\vb{V}^T \vb{V}) \tilde{\vb{\Omega}} \vb{V}^T
$$
$$
 \dd{\vb{R}} = \vb{U} \tilde{\vb{\Omega}} \vb{V}^T
$$
**Summary Algorithm:**
1. Compute $\dd{\vb{G}} = \dd{\vb{F}} \vb{A}$.
2. Compute projection $\vb{M} = \vb{U}^T \dd{\vb{G}} \vb{V}$.
3. Compute skew-symmetric matrix $\tilde{\vb{\Omega}}$:
$$
\tilde{\Omega}_{ij} = \begin{cases}
  \frac{M_{ij} - M_{ji}}{\sigma_i + \sigma_j} & i \neq j \\
  0                                           & i = j
\end{cases}
$$
4. Compute $\dd{\vb{R}} = \vb{U} \tilde{\vb{\Omega}} \vb{V}^T$.

## 4. First Derivative: Gradient $\pdv{\Psi}{\vb{F}}$

We compute the First Piola-Kirchhoff stress tensor $\vb{P}(\vb{F}) = \pdv{\Psi}{\vb{F}}$.

1. **Simplify Energy Density:**
$$
\Psi = \tr((\vb{G} - \vb{R})^T (\vb{G} - \vb{R})) = \tr(\vb{G}^T \vb{G}) - 2\tr(\vb{R}^T \vb{G}) + \tr(\vb{I})
$$
2. **Differentiate with respect to $\vb{G}$:**
$$
\dd{\Psi} = 2 \tr(\vb{G}^T \dd{\vb{G}}) - 2 \dd(\tr(\vb{R}^T \vb{G}))
$$
Using the property that $\tr(\dd{\vb{R}}^T \vb{G}) = \tr(\dd{\vb{R}}^T \vb{R} \vb{S}) = 0$ (trace of skew-symmetric $\times$ symmetric is 0):
$$
\dd{\Psi} = 2 \tr(\vb{G}^T \dd{\vb{G}}) - 2 \tr(\vb{R}^T \dd{\vb{G}}) = 2\tr((\vb{G} - \vb{R})^T \dd{\vb{G}})
$$
Thus,
$$
\pdv{\Psi}{\vb{G}} = 2(\vb{G} - \vb{R})
$$
3. **Chain Rule to $\vb{F}$:**
Since $\vb{G} = \vb{F}\vb{A}$, we have $\dd{\vb{G}} = \dd{\vb{F}} \vb{A}$.
$$
\dd{\Psi} = \tr(2 (\vb{G} - \vb{R})^T \dd{\vb{F}} \vb{A}) = \tr(\vb{A} 2 (\vb{G} - \vb{R})^T \dd{\vb{F}})
$$
$$
\dd{\Psi} = \tr((2 (\vb{G} - \vb{R}) \vb{A}^T)^T \dd{\vb{F}})
$$
4. **Final Result:**
Using $\vb{G} = \vb{F} \vb{A}$ and symmetric $\vb{A}$:
$$
\vb{P}(\vb{F}) = \pdv{\Psi}{\vb{F}} = 2 (\vb{F} \vb{A} - \vb{R}) \vb{A}
$$

## 5. Second Derivative: Hessian-Vector Product

Given a perturbation direction $d\vb{F}$, we compute the differential of the gradient $d\vb{P} = \mathcal{H} : d\vb{F}$.

1. **Differentiate $\vb{P}$:**
$$
\vb{P} = 2 \vb{F} \vb{A}^2 - 2 \vb{R} \vb{A}
$$
$$
\dd{\vb{P}} = 2 \dd{\vb{F}} \vb{A}^2 - 2 \dd{\vb{R}} \vb{A}
$$
2. **Computation Steps:** Given input $\dd{\vb{F}}$:
    1. Compute $\dd{\vb{G}} = \dd{\vb{F}} \vb{A}$.
    2. Compute $\vb{M} = \vb{U}^T \dd{\vb{G}} \vb{V}$.
    3. Form $\tilde{\vb{\Omega}}$ where $\tilde{\Omega}_{ij} = \frac{M_{ij} - M_{ji}}{\sigma_i + \sigma_j}$.
    4. Compute $\dd{\vb{R}} = \vb{U} \tilde{\vb{\Omega}} \vb{V}^T$.
    5. Compute result:
$$
\dd{\vb{P}} = 2 (\dd{\vb{F}} \vb{A} - \dd{\vb{R}}) \vb{A}
$$

## 6. Hessian in Tensor Form

The Hessian $\mathcal{H}$ is a rank-4 tensor where $\mathcal{H}_{ijkl} = \frac{\partial P_{ij}}{\partial F_{kl}}$.

From the vector product $\dd{\vb{P}} = 2 \dd{\vb{F}} \vb{A}^2 - 2 \dd{\vb{R}} \vb{A}$:
1. **First Term ($2 \dd{\vb{F}} \vb{A}^2$):**
$$
(2 \dd{\vb{F}} \vb{A}^2)_{ij} = 2 \sum_p \dd{F_{ip}} (\vb{A}^2)_{pj}
$$
In tensor index form: $2 \delta_{ik} (\vb{A}^2)_{lj}$.
2. **Second Term ($-2 \dd{\vb{R}} \vb{A}$):**
This requires the derivative of rotation $\pdv{R_{im}}{F_{kl}}$.
$$
(-2 \dd{\vb{R}} \vb{A})_{ij} = -2 \sum_m \dd{R_{im}} A_{mj}
$$
3. **Explicit Tensor Expression:**
Combining these, the Hessian tensor is:
$$
\mathcal{H}_{ijkl} = 2 \left( \delta_{ik} (\vb{A}^2)_{lj} - \sum_m \pdv{R_{im}}{F_{kl}} A_{mj} \right)
$$
To evaluate $\pdv{R_{im}}{F_{kl}}$ explicitly without $d\vb{F}$, we expand the update rule for $\tilde{\Omega}$:
    
$$
 \pdv{R_{im}}{F_{kl}} = \sum_{a,b} U_{ia} \left( \frac{\partial \tilde{\Omega}_{ab}}{\partial F_{kl}} \right) V_{mb}
$$
where the term inside the parenthesis is derived from projecting the single-entry matrix basis $\vb{E}_{kl}$ through the $\vb{M}$-projection and $\sigma$-scaling described in Section 3.
