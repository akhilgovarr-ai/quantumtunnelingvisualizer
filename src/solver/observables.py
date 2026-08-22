import numpy as np

def compute_norm(psi, x):
    """
    Полная вероятность (норма волновой функции).

    Parameters
    ----------
    psi : np.ndarray (complex)
        Волновая функция.
    x : np.ndarray
        Пространственная сетка.

    Returns
    -------
    float
        N = ∫ |ψ(x)|² dx
    """
    dx = x[1] - x[0]
    return np.sum(np.abs(psi)**2) * dx

def compute_TR(psi, x, barrier_start, barrier_width):
    """
    Коэффициенты прохождения (T) и отражения (R).

    Parameters
    ----------
    psi : np.ndarray (complex)
        Волновая функция после рассеяния.
    x : np.ndarray
        Пространственная сетка.
    barrier_start : float
        Левая граница барьера.
    barrier_width : float
        Ширина барьера.

    Returns
    -------
    tuple (T, R)
        T — вероятность прохождения,
        R — вероятность отражения.
    """
    dx = x[1] - x[0]
    T = np.sum(np.abs(psi[x > barrier_start + barrier_width])**2) * dx
    R = np.sum(np.abs(psi[x < barrier_start])**2) * dx
    return T, R

def compute_mean_position(psi, x):
    """
    Среднее положение ⟨x⟩.

    Parameters
    ----------
    psi : np.ndarray (complex)
        Волновая функция.
    x : np.ndarray
        Пространственная сетка.

    Returns
    -------
    float
        ⟨x⟩ = ∫ x |ψ(x)|² dx
    """
    dx = x[1] - x[0]
    return np.sum(x * np.abs(psi)**2) * dx