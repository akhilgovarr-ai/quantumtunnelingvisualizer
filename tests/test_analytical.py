import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'solver'))

from analytical import transmission_coefficient_rectangular

def test_T_zero_for_high_barrier():
    """Очень высокий барьер → T ≈ 0."""
    T = transmission_coefficient_rectangular(E=5.0, V0=100.0, a=1.0)
    assert T < 1e-10, f"T = {T}"

def test_T_one_for_no_barrier():
    """Нулевой барьер → T = 1."""
    T = transmission_coefficient_rectangular(E=5.0, V0=0.0, a=1.0)
    assert abs(T - 1.0) < 1e-10, f"T = {T}"

def test_T_monotonic_with_energy():
    """T растёт с энергией."""
    T1 = transmission_coefficient_rectangular(E=3.0, V0=10.0, a=1.0)
    T2 = transmission_coefficient_rectangular(E=8.0, V0=10.0, a=1.0)
    assert T2 > T1, f"T(E=8) = {T2} должно быть больше T(E=3) = {T1}"