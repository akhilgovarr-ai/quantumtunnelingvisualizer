import numpy as np
import sys
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'solver'))

from wavepacket import gaussian_wavepacket
from potentials import rectangular_barrier
from crank_nicolson import run_crank_nicolson
from split_step_fourier import run_split_step_fourier
from observables import compute_TR, compute_norm
from analytical import transmission_coefficient_rectangular

os.makedirs('figures', exist_ok=True)

# --- Параметры ---
x_min, x_max = -30.0, 30.0
N = 1000
x = np.linspace(x_min, x_max, N)
dx = x[1] - x[0]

x0, sigma, k0 = -15.0, 3.0, 5.0
V0, barrier_start, barrier_width = 15.0, 0.0, 1.0
dt = 0.01
n_steps = 400

V = rectangular_barrier(x, barrier_start, barrier_width, V0)
psi0 = gaussian_wavepacket(x, x0, k0, sigma)
psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)

# --- Симуляция обоими методами ---
print("Running simulations...")
psi_cn = run_crank_nicolson(psi0, V, x, dt, n_steps)
psi_ssf = run_split_step_fourier(psi0, V, x, dt, n_steps)

# --- Figure 1: Initial state + barrier ---
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, np.abs(psi0)**2, 'b-', label=r'$|\psi(x,0)|^2$')
ax2 = ax.twinx()
ax2.plot(x, V, 'r--', label='V(x)')
ax.set_xlabel('x')
ax.set_ylabel(r'$|\psi|^2$', color='b')
ax2.set_ylabel('V(x)', color='r')
ax.set_title('Initial Gaussian Wave Packet and Rectangular Barrier')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
fig.tight_layout()
plt.savefig('figures/fig1_initial_state.png', dpi=150)
plt.close()
print("Figure 1 saved")

# --- Figure 2: Evolution (final state) ---
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, np.abs(psi_cn)**2, 'b-', label='CN final state')
ax.plot(x, np.abs(psi_ssf)**2, 'g--', label='SSF final state')
ax2 = ax.twinx()
ax2.plot(x, V, 'r:', alpha=0.5)
ax.set_xlabel('x')
ax.set_ylabel(r'$|\psi|^2$')
ax2.set_ylabel('V(x)', color='r')
ax.set_title(f'Wave Function After Scattering (t={n_steps*dt:.1f})')
ax.legend(loc='upper left')
fig.tight_layout()
plt.savefig('figures/fig2_final_state.png', dpi=150)
plt.close()
print("Figure 2 saved")

# --- Figure 3: T(E) curve ---
E_values = np.linspace(2, 25, 50)
T_an = [transmission_coefficient_rectangular(E, V0, barrier_width) for E in E_values]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(E_values, T_an, 'r-', label='Analytical T(E)')
ax.axvline(x=V0, color='gray', linestyle=':', label=f'V0 = {V0}')
ax.set_xlabel('E')
ax.set_ylabel('T')
ax.set_title('Analytical Transmission Coefficient vs Energy')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
plt.savefig('figures/fig3_transmission_vs_energy.png', dpi=150)
plt.close()
print("Figure 3 saved")

# --- Figure 4: Convergence ---
N_list = [250, 500, 1000, 2000, 4000]
errors_cn = []
errors_ssf = []

E_packet = k0**2 / 2
T_an = transmission_coefficient_rectangular(E_packet, V0, barrier_width)

for N_test in N_list:
    x_test = np.linspace(x_min, x_max, N_test)
    dx_test = x_test[1] - x_test[0]
    V_test = rectangular_barrier(x_test, barrier_start, barrier_width, V0)
    psi0_test = gaussian_wavepacket(x_test, x0, k0, sigma)
    psi0_test = psi0_test / np.sqrt(np.sum(np.abs(psi0_test)**2) * dx_test)
    
    psi_cn_test = run_crank_nicolson(psi0_test, V_test, x_test, dt, n_steps)
    T_cn_test, _ = compute_TR(psi_cn_test, x_test, barrier_start, barrier_width)
    errors_cn.append(abs(T_cn_test - T_an))
    
    psi_ssf_test = run_split_step_fourier(psi0_test, V_test, x_test, dt, n_steps)
    T_ssf_test, _ = compute_TR(psi_ssf_test, x_test, barrier_start, barrier_width)
    errors_ssf.append(abs(T_ssf_test - T_an))

dx_list = [(x_max - x_min) / N_val for N_val in N_list]

fig, ax = plt.subplots(figsize=(8, 4))
ax.loglog(dx_list, errors_cn, 'o-', label='CN error', color='tab:blue')
ax.loglog(dx_list, errors_ssf, 's-', label='SSF error', color='tab:green')
ax.loglog(dx_list, [d**2 for d in dx_list], '--', label=r'$\sim \Delta x^2$', color='gray')
ax.set_xlabel(r'$\Delta x$')
ax.set_ylabel('Error')
ax.set_title('Convergence Study')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
plt.savefig('figures/fig4_convergence.png', dpi=150)
plt.close()
print("Figure 4 saved")

print("\nAll figures generated successfully!")