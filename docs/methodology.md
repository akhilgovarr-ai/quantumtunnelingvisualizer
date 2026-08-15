# Methodology

## Governing Equation

The system is modeled by the one-dimensional time-dependent Schrödinger equation:

i·ℏ·(∂ψ/∂t) = [ −(ℏ²/2m)·(∂²/∂x²) + V(x) ]·ψ

where:
- ψ(x, t) is the complex wavefunction describing the particle's quantum state
- V(x) is the potential energy as a function of position
- m is the particle's mass
- ℏ is the reduced Planck constant

## Initial Condition: Gaussian Wave Packet

The initial state is a normalized Gaussian wave packet:

ψ(x, 0) = (1 / (2π·σ²)^(1/4)) · exp( −(x − x₀)² / (4σ²) ) · exp( i·k₀·x )

where:
- x₀ is the initial mean position of the packet
- k₀ is the initial mean wavenumber, related to the mean momentum p₀ = ℏ·k₀
- σ is the initial spatial width of the packet

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

## Boundary Conditions

[to fill in after Stage 20: state whether boundaries are reflecting, periodic, or absorbing, based on what the current implementation actually does]