---
category:
  - Course Notes
date: 2023-04-14T08:00:00+08:00
modified: 2025-09-20T23:07:39+08:00
tags:
  - Quantum_Mechanics
title: "Chap 1: 波函数与 Schrodinger 方程"
---

## 1.1 波函数的统计诠释

### 1.1.1 实物粒子的波动性

$$
\lambda = h / p \qc
\nu = E / h
$$

### 1.1.2 波粒二象性的分析

在非相对论情况下, 自由粒子能量 $E = p^2 / 2 m$, 利用 de Broglie 关系, 可得

$$
\omega = \hbar k^2 / 2 m \qc
k = 2 \pi / \lambda
$$

所以波包的群速度为

$$
v_g = \dv*{\omega}{k} = \hbar k / m = p / m = v
$$

即经典粒子的速度.

### 1.1.3 概率波, 多粒子体系的波函数

### 1.1.4 动量分布概率

$$
\psi(\vb*{r}) = \frac{1}{\pqty{2 \pi \hbar}^{\frac{3}{2}}} \int \varphi(\vb*{p}) e^{i \vb*{p} \vdot \vb*{r} / \hbar} \dd[3]{p}
$$

$$
\varphi(\vb*{p}) = \frac{1}{\pqty{2 \pi \hbar}^{\frac{3}{2}}} \int \psi(\vb*{r}) e^{- i \vb*{p} \vdot \vb*{r} / \hbar} \dd[3]{r}
$$

### 1.1.5 不确定性原理与不确定度关系

$$
\Delta{x} \vdot \Delta{p} \geqslant \frac{\hbar}{2}
$$

### 1.1.6 力学量的平均值与算符的引进

$$
\begin{align*}
  \hat{\vb*{p}} & = - i \hbar \grad                            & \qq{(动量算符)}      \\
  \hat{T}       & = - \frac{h^2}{2 m} \grad^2                  & \qq{(动能算符)}      \\
  \vb*{l}       & = \vb*{r} \cp \hat{\vb*{p}}                  & \qq{(角动量算符)}    \\
  \hat{H}       & = - \frac{\hbar^2}{2 m} \grad^2 + V(\vb*{r}) & \qq{(Hamilton 算符)}
\end{align*}
$$

一般来说, 粒子的力学量 $A$ 的平均值可如下求出

$$
\overline{A} = \int \psi^*(\vb*{r}) \hat{A} \psi(\vb*{r}) \dd[3]{r} = \pqty{\psi, \hat{A} \psi}
$$

$\hat{A}$ 是与力学量 $A$ 对应的算符. 如波函数未归一化, 则

$$
\overline{A} = \pqty{\psi, \hat{A} \psi} / \pqty{\psi, \psi}
$$

### 1.1.7 统计诠释对波函数提出的要求

1. $\psi(\vb*{r})$ 取有限值
2. 一个真实的波函数需要满足归一化条件 (平方可积)
3. $\abs{\psi(\vb*{r})}^2$ 单值
4. 波函数 $\psi(\vb*{r})$ 及其各阶微商的连续性

## 1.2 Schrodinger 方程

### 1.2.1 Schrodinger 方程的引进

先讨论 **自由** 粒子.

$$
\omega = E / \hbar \qc
\vb*{k} = \vb*{p} / \hbar
$$

$$
\begin{equation} \label{eq:8}
  i \hbar \pdv{t} \psi(\vb*{r}, t) = \bqty{- \frac{h^2}{2 m} \grad^2 + V(\vb*{r})} \psi(\vb*{r}, t)
\end{equation}
$$

### 1.2.2 Schrodinger 方程的讨论

#### 1. 定域的概率守恒

$$
\begin{align*}
  \rho(\vb*{r}, t)    & = \psi^*(\vb*{r}, t) \psi(\vb*{r}, t)                                        \\
  \vb*{j}(\vb*{r}, t) & = - \frac{i \hbar}{2 m} \pqty{\psi^* \grad \psi - \psi \grad \psi^*}         \\
                      & = \frac{1}{2 m} \pqty{\psi^* \hat{\vb*{p}} \psi - \psi \hat{\vb*{p}} \psi^*}
\end{align*}
$$

$\rho$ 表示概率密度, $\vb*{j}$ 表示概率流密度.

$$
\pdv{t} \rho + \div \vb*{j} = 0
$$

#### 2. 初值问题, 传播子

由于 Schrodinger 方程 **只含波函数 $\psi(\vb*{r}, t)$ 对时间的一次微商, 只要在初始时刻 $(t = 0)$ 体系的状态 $\psi(\vb*{r}, 0)$ 给定, 则以后任何时刻 $t$ 的状态 $\psi(\vb*{r}, t)$ 原则上就完全确定** 了.

取初始时刻为 $t'$, 则

$$
\begin{equation} \label{eq:21}
  \psi(\vb*{r}, t) = \int \dd[3]{r'} G(\vb*{r}, t; \vb*{r}', t') \psi(\vb*{r}', t') \quad (t \geqslant t')
\end{equation}
$$

式中

$$
G(\vb*{r}, t; \vb*{r}', t') = \bqty{\frac{m}{2 \pi i \hbar (t - t')}}^{\frac{3}{2}} \exp\bqty{i \frac{m}{2 \hbar} \frac{(\vb*{r} - \vb*{r}')^2}{(t - t')}}
$$

$$
\lim_{t \to t'} G(\vb*{r}, t; \vb*{r}', t') = \var(\vb*{r} - \vb*{r}')
$$

$G(\vb*{r}, t; \vb*{r}', t')$ 的物理意义如下: 设初始时刻 $t'$ 粒子处于空间 $\vb*{r}_0'$ 点, $\psi(\vb*{r}', t') = \var(\vb*{r}' - \vb*{r}_0')$, 按式 $\eqref{eq:21}$

$$
\psi(\vb*{r}, t)
= \int \dd[3]{r}' G(\vb*{r}, t; \vb*{r}', t') \var(\vb*{r}' - \vb*{r}_0')
= G(\vb*{r}, t; \vb*{r}', t')
$$

式 $\eqref{eq:21}$ 表示: 在 **$t$ 时刻于空间 $\vb*{r}$ 点找到粒子的概率波幅 $\psi(\vb*{r}, t)$ 是 $t' (\leqslant t)$ 时刻粒子在空间中各 $\vb*{r}'$ 点的概率波幅传播到 $\vb*{r}$ 点后的相干叠加**.

### 1.2.3 能量本征方程

假设 **势能 $V$ 不显含 $t$** (经典力学中, 在这种势场中的粒子的机械能是守恒量). 此时, Schrodinger 方程 $\eqref{eq:8}$ 可以用分离变数法求其特解.

特解可表示为

$$
\psi(\vb*{r}, t) = \psi_E(\vb*{r}) e^{- i E t / \hbar}
$$

其中 $\psi_E(\vb*{r})$ 满足下列方程:

$$
\bqty{- \frac{\hbar^2}{2 m} \grad^2 + V(\vb*{r})} \psi_E(\vb*{r}) = E \psi_E(\vb*{r})
$$

Schrodinger 方程更普遍的表示是

$$
\begin{equation} \label{eq:31}
  i \hbar \pdv{t} \psi = \hat{H} \psi
\end{equation}
$$

$\hat{H}$ 是体系的 Hamilton 算符. 当 $\hat{H}$ **不显含 $t$ 时**, 体系的能量是守恒量, 方程 $\eqref{eq:31}$ 可以分离变量. 此时, 不含时 Schrodinger 方程, 即能量本征方程, 为

$$
\hat{H} \psi = E \psi
$$

### 1.2.4 定态与非定态

$$
\begin{equation} \label{eq:34}
  \psi(\vb*{r}, t) = \psi_E(\vb*{r}) e^{- i E t / \hbar}
\end{equation}
$$

形式如式 $\eqref{eq:34}$ 的波函数所描述的态, 成为 **定态**. 处于定态下的粒子具有如下特征:

1. 粒子在空间的 **概率密度 $\rho(\vb*{r}) = \abs{\psi_E(\vb*{r})}^2$** 以及 **概率流密度 $\vb*{j}$** 显然 **不随时间改变**.
2. **任何 (不显含 $t$ 的) 力学量的平均值不随时间改变**. 因为在定态 $\eqref{eq:34}$ 下, 不显含 $t$ 的力学量 $A$ 的平均值
   $$
   \begin{equation*}
     \begin{split}
       \overline{A}
        & = \int \psi^*(\vb*{r}, t) \hat{A} \psi(\vb*{r}, t) \dd[3]{r} \\
        & = \int \psi_E^*(\vb*{r}) \hat{A} \psi_E(\vb*{r}) \dd[3]{r}
     \end{split}
   \end{equation*}
   
$$
3. **任何 (不显含 $t$ 的) 力学量的测值概率分布也不随时间改变**.

若体系的初态不是能量本征态, 而是若干个能量本征态的叠加 (设 $E$ 取离散值)

$$
\psi(\vb*{r}, 0) = \sum_E C_E \psi_E(\vb*{r})
$$

式中的叠加系数 $C_E$ 为

$$
C_E = \int \dd[3]{r} \psi_E^_(\vb_{r}) \psi(\vb*{r}, 0)
$$

由于初态 $\psi(\vb*{r}, 0)$ 唯一确定. 不难证明

$$
\begin{equation} \label{eq:37}
  \psi(\vb*{r}, t) = \sum_E C_E \psi_E(\vb*{r}) e^{- i E t / \hbar}
\end{equation}
$$

在式 $\eqref{eq:37}$ 所示状态下, 粒子的能量平均值为

$$
\overline{H} = \sum_E \abs{C_E}^2 E
$$

所以, $\abs{C_E}^2$ 可以理解为在式 $\eqref{eq:37}$ 所示状态下测得粒子能量为 $E$ 值的概率. 这种由若干个能量不同的本征态的叠加所形成的态, 称为 **非定态**.

### 1.2.5 多粒子体系的 Schrodinger 方程

## 1.3 量子态叠加原理

### 1.3.1 量子态及其表象

我们称 $\psi(\vb*{r})$ 是粒子态在 **坐标表象** 中的表示, 而 $\varphi(\vb*{p})$ 则是同一个状态在 **动量表象** 中的表示.

### 1.3.2 量子态叠加原理, 测量与波函数坍缩
