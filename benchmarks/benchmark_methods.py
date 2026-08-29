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

results = []

for N in [256, 512, 1024, 2048, 4096]:
    x = np.linspace(x_min, x_max, N)
    dx = x[1] - x[0]
    
    V = rectangular_barrier(x, barrier_start, barrier_width, V0)
    psi0 = gaussian_wavepacket(x, x0, k0, sigma)
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)
    
    # Crank-Nicolson
    t_start = time.perf_counter()
    psi_cn = run_crank_nicolson(psi0, V, x, dt, n_steps)
    t_cn = time.perf_counter() - t_start
    
    T_cn, R_cn = compute_TR(psi_cn, x, barrier_start, barrier_width)
    norm_cn = compute_norm(psi_cn, x)
    error_cn = abs(T_cn - T_analytical)
    
    # Split-Step Fourier
    t_start = time.perf_counter()
    psi_ssf = run_split_step_fourier(psi0, V, x, dt, n_steps)
    t_ssf = time.perf_counter() - t_start
    
    T_ssf, R_ssf = compute_TR(psi_ssf, x, barrier_start, barrier_width)
    norm_ssf = compute_norm(psi_ssf, x)
    error_ssf = abs(T_ssf - T_analytical)
    
    results.append({
        'N': N,
        'CN_time_s': round(t_cn, 4),
        'SSF_time_s': round(t_ssf, 4),
        'CN_error': round(error_cn, 6),
        'SSF_error': round(error_ssf, 6),
        'CN_norm_error': abs(norm_cn - 1.0),
        'SSF_norm_error': abs(norm_ssf - 1.0)
    })
    
    print(f"N = {N:5d}") 
    print(f"  CN:  time = {t_cn:.4f}s, error = {error_cn:.6f}")
    print(f"  SSF: time = {t_ssf:.4f}s, error = {error_ssf:.6f}")
    print(f"  Speedup (SSF/CN): {t_cn/t_ssf:.2f}x")
    print()

# Сохранение CSV
os.makedirs('results/raw', exist_ok=True)
with open('results/raw/benchmark_methods.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Результаты сохранены: results/raw/benchmark_methods.csv")

# --- Таблица для статьи ---
print("\n" + "="*80)
print("TABLE: Benchmark Results")
print("="*80)
print(f"{'N':<6} {'CN time (s)':<12} {'SSF time (s)':<12} {'CN error':<10} {'SSF error':<10}")
print("-"*50)
for r in results:
    print(f"{r['N']:<6} {r['CN_time_s']:<12} {r['SSF_time_s']:<12} {r['CN_error']:<10} {r['SSF_error']:<10}")

# --- График ---
import matplotlib.pyplot as plt

N_values = [r['N'] for r in results]
cn_times = [r['CN_time_s'] for r in results]
ssf_times = [r['SSF_time_s'] for r in results]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(N_values, cn_times, 'o-', label='Crank-Nicolson', color='tab:blue')
ax1.plot(N_values, ssf_times, 's-', label='Split-Step Fourier', color='tab:green')
ax1.set_xlabel('N (grid size)')
ax1.set_ylabel('Runtime (s)')
ax1.set_title('Computational Performance')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.semilogy(N_values, [r['CN_error'] for r in results], 'o-', label='CN error', color='tab:blue')
ax2.semilogy(N_values, [r['SSF_error'] for r in results], 's-', label='SSF error', color='tab:green')
ax2.set_xlabel('N (grid size)')
ax2.set_ylabel('Error (log scale)')
ax2.set_title('Accuracy')
ax2.legend()
ax2.grid(True, alpha=0.3)

fig.tight_layout()
plt.savefig('figures/benchmark_methods.png', dpi=150)
plt.show()
print("График сохранён: figures/benchmark_methods.png")