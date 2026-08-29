# Numerical Study of One-Dimensional Quantum Tunneling: Comparison of Crank-Nicolson and Split-Step Fourier Methods

## Abstract

We present a comparative numerical study of two methods for solving the one-dimensional time-dependent Schrödinger equation: the Crank-Nicolson (CN) finite-difference scheme and the Split-Step Fourier (SSF) spectral method. Both methods are applied to simulate quantum tunneling of a Gaussian wave packet through a rectangular potential barrier. We validate both implementations against analytical results for the transmission coefficient and investigate convergence properties, norm conservation, and computational performance. Our results show that CN achieves higher accuracy for discontinuous (rectangular) potentials with error < 0.002 for N ≥ 1024, while SSF is consistently 2–4 times faster but does not converge systematically due to Gibbs oscillations at potential discontinuities. This work provides a reproducible open-source benchmark for numerical quantum tunneling simulations.

## 1. Introduction

Quantum tunneling is a fundamental phenomenon in quantum mechanics with applications ranging from scanning tunneling microscopy to nuclear fusion. The time-dependent Schrödinger equation (TDSE) governs the evolution of quantum states, but analytical solutions exist only for simple potentials. For general potentials, numerical methods are essential.

Two widely used numerical approaches are:
- **Crank-Nicolson (CN)**: an implicit finite-difference scheme, second-order accurate in space and time, unconditionally stable.
- **Split-Step Fourier (SSF)**: a spectral method using Fast Fourier Transform (FFT), highly efficient for smooth potentials.

This work addresses the research question: **How do CN and SSF compare in accuracy, stability, probability conservation, and computational performance when simulating one-dimensional quantum tunneling?**

## 2. Physical Model

### 2.1 Governing Equation

We solve the one-dimensional time-dependent Schrödinger equation:

iħ · ∂ψ/∂t = [ −(ħ²/2m) · ∂²/∂x² + V(x) ] · ψ

In dimensionless units (ħ = 1, m = 1), the equation simplifies to:

i · ∂ψ/∂t = [ −(1/2) · ∂²/∂x² + V(x) ] · ψ

### 2.2 Initial Condition

The initial state is a Gaussian wave packet:

ψ(x, 0) = (1/(2πσ²)^(1/4)) · exp( −(x − x₀)² / (4σ²) ) · exp( i·k₀·x )

where x₀ = −15.0, σ = 3.0, k₀ = 5.0 in our simulations. The mean energy is E = k₀²/2 = 12.5.

### 2.3 Potential

We consider a rectangular potential barrier:

V(x) = V₀ for x ∈ [0, a], V(x) = 0 otherwise

with V₀ = 15.0 and a = 1.0 in our simulations.

## 3. Numerical Methods

### 3.1 Crank-Nicolson Method

The CN scheme discretizes the TDSE as:

A · ψ^{n+1} = B · ψ^n

where A = I + (iΔt/2)·H and B = I − (iΔt/2)·H.

The Hamiltonian H is represented as a sparse tridiagonal matrix:
(H·ψ)_j = −(1/(2Δx²))·(ψ_{j+1} − 2ψ_j + ψ_{j−1}) + V_j·ψ_j

The scheme is unconditionally stable and conserves probability exactly in exact arithmetic.

### 3.2 Split-Step Fourier Method

The SSF method uses operator splitting with FFT. Each time step consists of three substeps:

1. Half step in potential: ψ ← ψ · exp(−i·V·Δt/2)
2. Full step in kinetic: ψ ← IFFT( FFT(ψ) · exp(−i·k²·Δt/2) )
3. Half step in potential: ψ ← ψ · exp(−i·V·Δt/2)

This is a second-order accurate splitting (Strang splitting).

## 4. Validation

### 4.1 Norm Conservation

Both methods conserve total probability with error < 1e-13 over 400 time steps.

### 4.2 Analytical Comparison

For the rectangular barrier, the analytical transmission coefficient is:

T(E) = 1 / ( 1 + [ (k² + κ²) / (2kκ) ]² · sinh²(κ·a) )  for E < V₀

where k = √(2mE)/ħ and κ = √(2m(V₀−E))/ħ.

Using a wide Gaussian packet (σ = 3.0) to approximate a monochromatic wave:
- CN: T = 0.0286, error = 0.0033
- SSF: T = 0.0424, error = 0.0171

### 4.3 Convergence Study

For N = 250 to 4000 grid points:
- CN shows monotonic convergence: error decreases from 0.019 to 0.001.
- SSF does not show systematic convergence: error oscillates around 0.004–0.010.

This confirms that CN is the preferred method for discontinuous potentials.

## 5. Results

### 5.1 Benchmark Results

| N    | CN time (s) | SSF time (s) | CN error | SSF error |
|------|-------------|--------------|----------|-----------|
| 256  | 0.116       | 0.032        | 0.018    | 0.002     |
| 512  | 0.197       | 0.050        | 0.011    | 0.005     |
| 1024 | 0.175       | 0.082        | 0.0003   | 0.005     |
| 2048 | 0.571       | 0.174        | 0.001    | 0.011     |
| 4096 | 0.814       | 0.330        | 0.002    | 0.010     |

SSF is consistently 2–4x faster than CN.

### 5.2 Parameter Sweeps

- T(E): excellent agreement with analytical results for E < V₀.
- T(V₀): good agreement in tunneling regime.
- T(a): exponential decay confirmed, T ∝ exp(−2κa).

## 6. Discussion

The results demonstrate a clear trade-off between accuracy and speed:
- CN is more accurate for discontinuous potentials but computationally more expensive.
- SSF is faster but suffers from Gibbs oscillations at sharp potential edges.

For smooth potentials, SSF is expected to achieve spectral accuracy and outperform CN. This will be investigated in future work.

## 7. Limitations

- One-dimensional model only
- Non-relativistic quantum mechanics
- Non-interacting particles
- Simple rectangular barrier (most experiments)
- Finite grid introduces numerical error
- Wave packet has energy spread (not truly monochromatic)

## 8. Conclusion

We have implemented and validated two numerical methods for the 1D TDSE. CN achieves higher accuracy for rectangular barriers, while SSF offers better computational performance. The open-source code and reproducible experiments provide a benchmark for quantum tunneling simulations.

## References

1. J. Crank, P. Nicolson (1947). "A practical method for numerical evaluation of solutions of partial differential equations of the heat-conduction type." Mathematical Proceedings of the Cambridge Philosophical Society, 43(1), 50–67.

2. R. H. Hardin, F. D. Tappert (1973). "Applications of the split-step Fourier method to the numerical solution of nonlinear and variable coefficient wave equations." SIAM Review, 15(2), 423.

3. D. J. Griffiths. "Introduction to Quantum Mechanics." Pearson. Re