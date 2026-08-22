import numpy as np
import sys
import os
import csv
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'solver'))

from wavepacket import gaussian_wavepacket
from potentials import rectangular_barrier
from crank_nicolson import run_crank_nicolson
from split_step_fourier import run_split_step_fourier
from observables import compute_TR, compute_norm
from analytical import transmission_coefficient_rectangular

# Параметры
x_min, x_max = -30.0, 30.0
x0, sigma, k0 = -15.0, 3.0, 5.0
V0, barrier_start, barrier_width = 15.0, 0.0, 1.0
dt = 0.01
n_steps = 400

E_packet = k0**2 / 2
T_analytical = transmission_coefficient_rectangular(E_packet, V0, barrier_width)

print(f"E_packet = {E_packet}")
print(f"T_analytical = {T_analytical:.6f}")
print()

# Таблица результатов
results = []

for N in [250, 500, 1000, 2000, 4000]:
    x = np.linspace(x_min, x_max, N)
    dx = x[1] - x[0]
    
    V = rectangular_barrier(x, barrier_start, barrier_width, V0)
    psi0 = gaussian_wavepacket(x, x0, k0, sigma)
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)
    
    # Crank-Nicolson
    t_start = time.time()
    psi_cn = run_crank_nicolson(psi0, V, x, dt, n_steps)
    t_cn = time.time() - t_start
    
    T_cn, R_cn = compute_TR(psi_cn, x, barrier_start, barrier_width)
    norm_cn = compute_norm(psi_cn, x)
    error_cn = abs(T_cn - T_analytical)
    
    # Split-Step Fourier
    t_start = time.time()
    psi_ssf = run_split_step_fourier(psi0, V, x, dt, n_steps)
    t_ssf = time.time() - t_start
    
    T_ssf, R_ssf = compute_TR(psi_ssf, x, barrier_start, barrier_width)
    norm_ssf = compute_norm(psi_ssf, x)
    error_ssf = abs(T_ssf - T_analytical)
    
    results.append({
        'N': N,
        'dx': dx,
        'T_CN': T_cn,
        'T_SSF': T_ssf,
        'error_CN': error_cn,
        'error_SSF': error_ssf,
        'norm_CN': norm_cn,
        'norm_SSF': norm_ssf,
        'runtime_CN': t_cn,
        'runtime_SSF': t_ssf
    })
    
    print(f"N = {N:4d}  dx = {dx:.4e}")
    print(f"  CN:  T = {T_cn:.6f}, error = {error_cn:.6f}, norm = {norm_cn:.8f}, runtime = {t_cn:.3f}s")
    print(f"  SSF: T = {T_ssf:.6f}, error = {error_ssf:.6f}, norm = {norm_ssf:.8f}, runtime = {t_ssf:.3f}s")
    print()

# Сохранение CSV
os.makedirs('results/raw', exist_ok=True)
with open('results/raw/convergence_study.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Результаты сохранены: results/raw/convergence_study.csv")

# --- График сходимости ---
import matplotlib.pyplot as plt

dx_values = [r['dx'] for r in results]
error_cn = [r['error_CN'] for r in results]
error_ssf = [r['error_SSF'] for r in results]

fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(dx_values, error_cn, 'o-', label='Crank-Nicolson', color='tab:blue')
ax.loglog(dx_values, error_ssf, 's-', label='Split-Step Fourier', color='tab:green')
ax.loglog(dx_values, [dx**2 for dx in dx_values], '--', label=r'$\sim \Delta x^2$', color='gray')
ax.set_xlabel(r'$\Delta x$')
ax.set_ylabel(r'$|T_{num} - T_{analytical}|$')
ax.set_title('Convergence Study: Rectangular Barrier')
ax.legend()
ax.grid(True, which='both', alpha=0.3)

fig.tight_layout()
os.makedirs('figures', exist_ok=True)
plt.savefig('figures/convergence_study.png', dpi=150)
plt.show()
print("График сохранён: figures/convergence_study.png")