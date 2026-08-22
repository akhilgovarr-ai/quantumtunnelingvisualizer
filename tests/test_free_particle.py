import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'solver'))

from wavepacket import gaussian_wavepacket
from potentials import rectangular_barrier
from crank_nicolson import run_crank_nicolson
from split_step_fourier import run_split_step_fourier
from observables import compute_mean_position

def test_free_particle_moves_right_cn():
    """Свободная частица (V=0) движется вправо для CN."""
    x = np.linspace(-20, 20, 1000)
    V = np.zeros_like(x)
    psi0 = gaussian_wavepacket(x, -10.0, 5.0, 1.0)
    
    dx = x[1] - x[0]
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)
    
    psi = run_crank_nicolson(psi0, V, x, dt=0.01, n_steps=200)
    
    x_start = compute_mean_position(psi0, x)
    x_end = compute_mean_position(psi, x)
    
    assert x_end > x_start, f"Пакет не движется вправо: {x_start:.2f} → {x_end:.2f}"

def test_free_particle_moves_right_ssf():
    """Свободная частица (V=0) движется вправо для SSF."""
    x = np.linspace(-20, 20, 1000)
    V = np.zeros_like(x)
    psi0 = gaussian_wavepacket(x, -10.0, 5.0, 1.0)
    
    dx = x[1] - x[0]
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)
    
    psi = run_split_step_fourier(psi0, V, x, dt=0.01, n_steps=200)
    
    x_start = compute_mean_position(psi0, x)
    x_end = compute_mean_position(psi, x)
    
    assert x_end > x_start, f"Пакет не движется вправо: {x_start:.2f} → {x_end:.2f}"