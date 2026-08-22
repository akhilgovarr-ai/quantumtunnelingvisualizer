import numpy as np

def rectangular_barrier(x, barrier_start, barrier_width, V0):
    """
    Rectangular potential barrier.

    Parameters
    ----------
    x : ndarray
        Spatial grid.
    barrier_start : float
        Left edge position of the barrier.
    barrier_width : float
        Width of the barrier.
    V0 : float
        Barrier height.

    Returns
    -------
    ndarray
        Potential V(x): equal to V0 inside the barrier region, 0 elsewhere.
    """
    V = np.zeros_like(x)
    V[(x >= barrier_start) & (x <= barrier_start + barrier_width)] = V0
    return V