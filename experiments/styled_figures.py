import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# ---------- Настройка стиля ----------
plt.rcParams.update({
    'figure.facecolor': '#0a0a12',
    'axes.facecolor': '#12121e',
    'axes.edgecolor': '#1e1e2e',
    'axes.labelcolor': '#e8e8f0',
    'text.color': '#e8e8f0',
    'xtick.color': '#9999aa',
    'ytick.color': '#9999aa',
    'grid.color': '#1e1e2e',
    'grid.alpha': 0.5,
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
})

# Цвета
CYAN = '#00d4ff'
GREEN = '#00ff88'
RED = '#ff6b6b'
GRAY = '#9999aa'

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'solver'))

from wavepacket import gaussian_wavepacket
from potentials import rectangular_barrier
from crank_nicolson import run_crank_nicolson
from split_step_fourier import run_split_step_fourier
from observables import compute_TR
from analytical import transmission_coefficient_rectangular

os.makedirs('figures/styled', exist_ok=True)

# ==========================================
# Figure 1: Premium T(E) curve
# ==========================================
E_values = np.linspace(1, 25, 200)
V0, a = 15.0, 1.0
T_values = [transmission_coefficient_rectangular(E, V0, a) for E in E_values]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(E_values, T_values, color=CYAN, linewidth=3, label='Analytical T(E)')
ax.axvline(x=V0, color=RED, linestyle='--', linewidth=1.5, alpha=0.8, label=f'V₀ = {V0}')
ax.fill_between(E_values, T_values, alpha=0.1, color=CYAN)

# Область туннелирования
ax.fill_between(E_values[E_values < V0], T_values[:len(E_values[E_values < V0])], 
                 alpha=0.08, color=GREEN, label='Tunneling regime')
ax.fill_between(E_values[E_values > V0], T_values[len(E_values[E_values < V0]):], 
                 alpha=0.08, color=RED, label='Above barrier')

ax.set_xlabel('E (energy)', fontsize=13)
ax.set_ylabel('T (transmission)', fontsize=13)
ax.set_title('Transmission Coefficient vs Energy', fontsize=15, fontweight='bold', pad=15)
ax.legend(facecolor='#12121e', edgecolor='#1e1e2e', labelcolor='#e8e8f0')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 26)
ax.set_ylim(0, 1.05)

fig.tight_layout()
plt.savefig('figures/styled/transmission_vs_energy.png', dpi=200, bbox_inches='tight')
plt.close()
print("Styled Figure 1 saved")

# ==========================================
# Figure 2: Premium benchmark comparison
# ==========================================
N_values = [256, 512, 1024, 2048, 4096]
cn_times = [0.116, 0.197, 0.175, 0.571, 0.814]
ssf_times = [0.032, 0.050, 0.082, 0.174, 0.330]
cn_errors = [0.018, 0.011, 0.0003, 0.001, 0.002]
ssf_errors = [0.002, 0.005, 0.005, 0.011, 0.010]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.plot(N_values, cn_times, 'o-', color=CYAN, linewidth=2.5, markersize=8, label='Crank-Nicolson')
ax1.plot(N_values, ssf_times, 's-', color=GREEN, linewidth=2.5, markersize=8, label='Split-Step Fourier')
ax1.set_xlabel('N (grid size)', fontsize=12)
ax1.set_ylabel('Runtime (s)', fontsize=12)
ax1.set_title('Computational Performance', fontsize=13, fontweight='bold')
ax1.legend(facecolor='#12121e', edgecolor='#1e1e2e')
ax1.grid(True, alpha=0.3)

ax2.semilogy(N_values, cn_errors, 'o-', color=CYAN, linewidth=2.5, markersize=8, label='CN error')
ax2.semilogy(N_values, ssf_errors, 's-', color=RED, linewidth=2.5, markersize=8, label='SSF error')
ax2.set_xlabel('N (grid size)', fontsize=12)
ax2.set_ylabel('Error (log scale)', fontsize=12)
ax2.set_title('Accuracy Comparison', fontsize=13, fontweight='bold')
ax2.legend(facecolor='#12121e', edgecolor='#1e1e2e')
ax2.grid(True, alpha=0.3)

fig.tight_layout()
plt.savefig('figures/styled/benchmark_comparison.png', dpi=200, bbox_inches='tight')
plt.close()
print("Styled Figure 2 saved")

# ==========================================
# Figure 3: Premium wave packet + barrier
# ==========================================
x = np.linspace(-25, 25, 1200)
dx = x[1] - x[0]
V = rectangular_barrier(x, 0.0, 1.0, 15.0)
psi0 = gaussian_wavepacket(x, -12.0, 6.0, 2.5)
psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)

fig, ax = plt.subplots(figsize=(12, 6))

# Барьер
ax.fill_between(x, 0, V / V.max() * 0.25, color=RED, alpha=0.3, label='V(x) / V₀')

# Волновой пакет
ax.plot(x, np.abs(psi0)**2, color=CYAN, linewidth=2.5, label=r'$|\psi(x,0)|^2$')
ax.fill_between(x, 0, np.abs(psi0)**2, color=CYAN, alpha=0.2)

ax.set_xlabel('x (position)', fontsize=13)
ax.set_ylabel('Probability density', fontsize=13)
ax.set_title('Initial Gaussian Wave Packet and Potential Barrier', fontsize=15, fontweight='bold', pad=15)
ax.legend(facecolor='#12121e', edgecolor='#1e1e2e')
ax.grid(True, alpha=0.3)
ax.set_xlim(-20, 15)
ax.set_ylim(0, 0.3)

fig.tight_layout()
plt.savefig('figures/styled/wave_packet_barrier.png', dpi=200, bbox_inches='tight')
plt.close()
print("Styled Figure 3 saved")

print("\nAll styled figures saved to figures/styled/")