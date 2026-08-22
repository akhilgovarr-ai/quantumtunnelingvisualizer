import numpy as np
import sys
import os

# Добавляем путь к солверам
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'solver'))

from wavepacket import gaussian_wavepacket
from potentials import rectangular_barrier
from crank_nicolson import run_crank_nicolson
from split_step_fourier import run_split_step_fourier
from observables import compute_norm

def test_norm_conservation_cn():
    """Проверка сохранения нормы для Crank-Nicolson."""
    x = np.linspace(-20, 20, 1000)
    V = rectangular_barrier(x, 0.0, 1.0, 15.0)
    psi0 = gaussian_wavepacket(x, -10.0, 5.0, 1.0)
    
    # Нормировка
    dx = x[1] - x[0]
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)
    
    psi = run_crank_nicolson(psi0, V, x, dt=0.01, n_steps=400)
    
    norm_start = compute_norm(psi0, x)
    norm_end = compute_norm(psi, x)
    
    assert abs(norm_start - 1.0) < 1e-10, f"Начальная норма: {norm_start}"
    assert abs(norm_end - 1.0) < 1e-8, f"Конечная норма CN: {norm_end}"

def test_norm_conservation_ssf():
    """Проверка сохранения нормы для Split-Step Fourier."""
    x = np.linspace(-20, 20, 1000)
    V = rectangular_barrier(x, 0.0, 1.0, 15.0)
    psi0 = gaussian_wavepacket(x, -10.0, 5.0, 1.0)
    
    # Нормировка
    dx = x[1] - x[0]
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)
    
    psi = run_split_step_fourier(psi0, V, x, dt=0.01, n_steps=400)
    
    norm_start = compute_norm(psi0, x)
    norm_end = compute_norm(psi, x)
    
    assert abs(norm_start - 1.0) < 1e-10, f"Начальная норма: {norm_start}"
    assert abs(norm_end - 1.0) < 1e-8, f"Конечная норма SSF: {norm_end}"