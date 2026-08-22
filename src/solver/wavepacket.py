import numpy as np

def gaussian_wavepacket(x, x0, k0, sigma):
    """
    Normalized 1D Gaussian wave packet.

    Parameters
    ----------
    x : ndarray
        Spatial grid.
    x0 : float
        Initial mean position.
    k0 : float
        Initial mean wavenumber (mean momentum p0 = hbar * k0, with hbar = 1 in this mode).
    sigma : float
        Initial spatial width.

    Returns
    -------
    ndarray (complex)
        Normalized wavefunction psi(x, 0).
    """
    norm = (2 * np.pi * sigma**2) ** (-0.25)
    return norm * np.exp(-(x - x0)**2 / (4 * sigma**2)) * np.exp(1j * k0 * x)