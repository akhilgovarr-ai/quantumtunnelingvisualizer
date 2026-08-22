import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

def run_crank_nicolson(psi_start, V, x, dt, n_steps):
    """
    Crank-Nicolson method for the 1D time-dependent Schrödinger equation.

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

    # Hamiltonian (dimensionless units: hbar = 1, m = 1)
    main_diag = V + 1.0 / dx**2
    off_diag = -0.5 / dx**2 * np.ones(N - 1)
    H = diags([off_diag, main_diag, off_diag], offsets=[-1, 0, 1], format="csc")

    # Crank-Nicolson matrices
    I = diags([np.ones(N)], offsets=[0], format="csc")
    A = I + 1j * dt / 2 * H
    B = I - 1j * dt / 2 * H

    psi = psi_start.copy()
    for _ in range(n_steps):
        psi = spsolve(A, B @ psi)

    return psi