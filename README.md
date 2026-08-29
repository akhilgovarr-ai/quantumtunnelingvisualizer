# Numerical Study of One-Dimensional Quantum Tunneling

[![Tests](https://github.com/akhilgovarr-ai/quantumtunnelingvisualizer/actions/workflows/test.yml/badge.svg)](https://github.com/akhilgovarr-ai/quantumtunnelingvisualizer/actions/workflows/test.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22164464.svg)](https://doi.org/10.5281/zenodo.22164464)

1D quantum tunneling simulator with two numerical methods:
**Crank–Nicolson** and **Split-Step Fourier**.

**Live demo:** https://akhilgovarr-ai.github.io/quantumtunnelingvisualizer/

## Research Question

How do the Crank–Nicolson and Split-Step Fourier methods compare in accuracy, stability, probability conservation and computational performance when simulating one-dimensional quantum tunneling?

**Comparison metrics:**
- Transmission coefficient (T)
- Reflection coefficient (R)
- Norm conservation
- Numerical error
- Convergence rate
- Computational time
- Dependence on Δx
- Dependence on Δt

**Physical model:**
- 1D time-dependent Schrödinger equation
- Initial state: Gaussian wave packet
- Potential: rectangular potential barrier

## Project Status

- [x] Crank–Nicolson solver implemented and validated
- [x] Split-Step Fourier solver implemented and validated
- [x] Analytical transmission coefficient for rectangular barrier
- [x] Norm conservation tests (error < 1e-13)
- [x] Convergence study (CN: ~Δx², SSF: Gibbs artifact)
- [x] Benchmark: SSF is 2–4x faster, CN more accurate for rectangular barrier
- [x] Parameter sweeps: T(E), T(V0), T(a)
- [x] Scientific output module
- [x] Research figures

## Physical Model

The system is modeled by the 1D time-dependent Schrödinger equation:

iħ·∂ψ/∂t = [ −(ħ²/2m)·∂²/∂x² + V(x) ]·ψ

**Units:** dimensionless (ħ = 1, m = 1)

**Initial state:** Gaussian wave packet
ψ(x, 0) = (1/(2πσ²)^(1/4)) · exp(−(x−x₀)²/(4σ²)) · exp(i·k₀·x)

**Potential:** rectangular barrier
V(x) = V₀ for x ∈ [x_b, x_b + a], V(x) = 0 otherwise

## Numerical Methods

### Crank–Nicolson
Implicit finite-difference scheme, second-order accurate in space and time.
Solves: A·ψ^{n+1} = B·ψ^n, where A = I + (iΔt/2)H, B = I − (iΔt/2)H.

### Split-Step Fourier
Operator splitting with FFT. Each step:
1. Half step in potential: ψ ← ψ·exp(−iVΔt/2)
2. Full step in kinetic (momentum space): ψ ← IFFT(FFT(ψ)·exp(−ik²Δt/2))
3. Half step in potential: ψ ← ψ·exp(−iVΔt/2)

## Validation

### Norm Conservation
Both methods conserve total probability with error < 1e-13 over 400 time steps.

### Analytical Comparison
For rectangular barrier, analytical T(E) is computed and compared with numerical results.

Using a wide Gaussian packet (σ = 3.0) to approximate monochromatic wave:
- Crank–Nicolson: T = 0.0286, error = 0.0033
- Split-Step Fourier: T = 0.0424, error = 0.0171

CN is more accurate for discontinuous (rectangular) potentials.

### Convergence Study
- CN: error decreases monotonically with N (convergence ~Δx²)
- SSF: error does not improve systematically due to Gibbs oscillations

### Benchmark Results
| N    | CN time (s) | SSF time (s) | CN error | SSF error |
|------|-------------|--------------|----------|-----------|
| 256  | 0.116       | 0.032        | 0.018    | 0.002     |
| 512  | 0.197       | 0.050        | 0.011    | 0.005     |
| 1024 | 0.175       | 0.082        | 0.0003   | 0.005     |
| 2048 | 0.571       | 0.174        | 0.001    | 0.011     |
| 4096 | 0.814       | 0.330        | 0.002    | 0.010     |

**Conclusion:** SSF is 2–4x faster, but CN is more accurate for rectangular barriers.

## Project Structure
quantum-tunneling/
├── src/solver/
│   ├── constants.py           # Physical constants
│   ├── potentials.py          # Potential functions
│   ├── wavepacket.py          # Gaussian wave packet
│   ├── crank_nicolson.py      # CN solver
│   ├── split_step_fourier.py  # SSF solver
│   ├── observables.py         # T, R, norm, mean position
│   ├── analytical.py          # Analytical T(E) formula
│   ├── scientific_output.py   # Structured scientific summary
│   ├── compare_methods.py     # Method comparison script
│   └── visualizer.py          # Animation script
├── tests/                     # 7 automated tests
├── experiments/               # Reproducible experiment scripts
├── results/raw/               # CSV data
├── figures/                   # Generated figures
└── docs/                      # Documentation

## Installation

```bash
git clone https://github.com/akhilgovarr-ai/quantumtunnelingvisualizer.git
cd quantumtunnelingvisualizer
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Usage

Run method comparison:

```bash
.\venv\Scripts\python.exe .\src\solver\compare_methods.py
```

Run animation:

```bash
.\venv\Scripts\python.exe .\src\solver\visualizer.py
```

Run tests:

```bash
.\venv\Scripts\python.exe -m pytest tests/ -v
```

Run experiments:

```bash
.\venv\Scripts\python.exe .\experiments\convergence_study.py
.\venv\Scripts\python.exe .\experiments\benchmark_methods.py
.\venv\Scripts\python.exe .\experiments\parameter_sweep.py
```

## Limitations

· Model is one-dimensional
· Non-relativistic quantum mechanics only
· Non-interacting particles
· Simple rectangular barrier (most experiments)
· Finite grid introduces numerical error
· Finite domain can cause boundary reflections
· Wave packet has energy spread (not truly monochromatic)

## References

· J. Crank, P. Nicolson (1947). "A practical method for numerical evaluation of solutions of partial differential equations of the heat-conduction type."
· R. H. Hardin, F. D. Tappert (1973). "Applications of the split-step Fourier method to the numerical solution of nonlinear and variable coefficient wave equations."
· D. J. Griffiths. "Introduction to Quantum Mechanics."

## License

MIT License — see LICENSE file.

```