# Methodology

## Governing Equation

The system is modeled by the one-dimensional time-dependent Schrödinger equation:

i·ħ·(∂ψ/∂t) = [ −(ħ²/2m)·(∂²/∂x²) + V(x) ]·ψ

where:
- ψ(x, t) is the complex wavefunction describing the particle's quantum state
- V(x) is the potential energy as a function of position
- m is the particle's mass
- ħ is the reduced Planck constant

## Units

The simulation is performed in dimensionless units where:
- ħ = 1
- m = 1

Physical parameters (energy, barrier width) are scaled to these units through characteristic scales.

## Initial Condition: Gaussian Wave Packet

The initial state is a normalized Gaussian wave packet:

ψ(x, 0) = (1 / (2π·σ²)^(1/4)) · exp( −(x − x₀)² / (4σ²) ) · exp( i·k₀·x )

where:
- x₀ is the initial mean position of the packet
- k₀ is the initial mean wavenumber, related to the mean momentum p₀ = ħ·k₀
- σ is the initial spatial width of the packet

The mean energy of the packet is E = k₀²/2 (in dimensionless units).

## Potential: Rectangular Barrier

The potential is a finite rectangular barrier:

V(x) = V₀ for x in [x_b, x_b + a], and V(x) = 0 elsewhere

where:
- V₀ is the barrier height
- a is the barrier width
- x_b is the position of the barrier's left edge

## Spatial and Temporal Discretization

- Δx is the spacing between adjacent points on the spatial grid
- Δt is the time step used to advance the simulation
- The spatial domain is truncated to a finite interval [x_min, x_max], discretized into N points

## Numerical Methods

### Crank-Nicolson

The Crank-Nicolson scheme is an implicit finite-difference method, second-order accurate in both space and time. It solves:

A·ψ^{n+1} = B·ψ^n

where A = I + (i·Δt/2)·H and B = I − (i·Δt/2)·H.

The Hamiltonian H is discretized as:
(H·ψ)_j = −(1/(2Δx²))·(ψ_{j+1} − 2ψ_j + ψ_{j−1}) + V_j·ψ_j

### Split-Step Fourier

The Split-Step Fourier method uses operator splitting with FFT. Each time step consists of:
1. Half step in potential: ψ ← ψ·exp(−i·V·Δt/2)
2. Full step in kinetic (momentum space): ψ ← IFFT(FFT(ψ)·exp(−i·k²·Δt/2))
3. Half step in potential: ψ ← ψ·exp(−i·V·Δt/2)

## Validation

### Norm Conservation

Both methods conserve total probability with error < 1e-10 over 400 time steps.

### Analytical Comparison

For a rectangular barrier, the analytical transmission coefficient T(E) is computed and compared with numerical results. Using a wide Gaussian packet (σ = 3.0) to approximate a monochromatic wave:

- Crank-Nicolson: T = 0.0286, error = 0.0033
- Split-Step Fourier: T = 0.0424, error = 0.0171

CN is more accurate for discontinuous (rectangular) potentials because SSF (spectral method) suffers from Gibbs oscillations at sharp discontinuities.

## Boundary Conditions

Currently: reflecting boundaries (finite box). Wave reaching the domain edge will reflect back. For quantitative studies, the domain should be large enough that the wave packet does not reach the boundary during the simulation time.

## Convergence Study

A convergence study was performed for N = 250, 500, 1000, 2000, 4000 grid points.

For the rectangular barrier:
- **Crank-Nicolson** shows monotonic convergence: error decreases from 0.0193 to 0.0009 as N increases.
- **Split-Step Fourier** does not show systematic convergence: error oscillates around 0.004-0.010 due to Gibbs oscillations at the discontinuous potential.

This confirms that CN is the preferred method for discontinuous (rectangular) potentials.