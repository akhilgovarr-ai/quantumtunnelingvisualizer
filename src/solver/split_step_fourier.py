import numpy as np

def run_split_step_fourier(psi_start, V, x, dt, n_steps):
    """
    Split-Step Fourier method for the 1D time-dependent Schrödinger equation.

    Parameters
    ----------
    psi_start : np.ndarray (complex)
        Initial wavefunction ψ(x, 0).
    V : np.ndarray
        Potential V(x) on the spatial grid.
    x : np.ndarray
        Spatial grid.
    dt : float
        Time step.
    n_steps : int
        Number of time steps.

    Returns
    -------
    np.ndarray (complex)
        Wavefunction after n_steps.
    """
    dx = x[1] - x[0]
    N = len(x)
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)

    psi = psi_start.copy()
    for _ in range(n_steps):
        # Half step in potential
        psi = psi * np.exp(-1j * V * dt / 2)
        # Full step in kinetic (momentum space)
        psi_k = np.fft.fft(psi)
        psi_k = psi_k * np.exp(-1j * k**2 * dt / 2)
        psi = np.fft.ifft(psi_k)
        # Half step in potential
        psi = psi * np.exp(-1j * V * dt / 2)

    return psi