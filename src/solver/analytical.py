import numpy as np

def transmission_coefficient_rectangular(E, V0, a, m=1.0, hbar=1.0):
    """
    Аналитический коэффициент прохождения для прямоугольного барьера.

    Parameters
    ----------
    E : float
        Энергия частицы.
    V0 : float
        Высота барьера.
    a : float
        Ширина барьера.
    m : float
        Масса (безразмерная, по умолчанию 1.0).
    hbar : float
        Постоянная Планка (безразмерная, по умолчанию 1.0).

    Returns
    -------
    float
        T — коэффициент прохождения (0 ≤ T ≤ 1).
    """
    if E < 0:
        raise ValueError("Энергия должна быть неотрицательной")
    if V0 < 0:
        raise ValueError("Высота барьера должна быть неотрицательной")

    if E == V0:
        # Предельный случай
        return 1.0 / (1.0 + m * V0 * a**2 / (2 * hbar**2))

    if E < V0:
        # Туннелирование
        kappa = np.sqrt(2 * m * (V0 - E)) / hbar
        k = np.sqrt(2 * m * E) / hbar
        factor = (kappa**2 + k**2) / (2 * k * kappa)
        return 1.0 / (1.0 + factor**2 * np.sinh(kappa * a)**2)

    else:
        # Надбарьерное прохождение
        k = np.sqrt(2 * m * E) / hbar
        q = np.sqrt(2 * m * (E - V0)) / hbar
        factor = (k**2 - q**2) / (2 * k * q)
        return 1.0 / (1.0 + factor**2 * np.sin(q * a)**2)