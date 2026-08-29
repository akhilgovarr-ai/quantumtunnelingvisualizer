import numpy as np
import sys
import os
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'solver'))

from wavepacket import gaussian_wavepacket
from potentials import rectangular_barrier
from crank_nicolson import run_crank_nicolson
from observables import compute_TR
from analytical import transmission_coefficient_rectangular

import matplotlib.pyplot as plt

# --- Общие параметры ---
x_min, x_max = -30.0, 30.0
N = 1000
x = np.linspace(x_min, x_max, N)
dx = x[1] - x[0]

x0, sigma = -15.0, 3.0
dt = 0.01
n_steps = 400

# ==========================================
# Experiment A: T(E) — меняем энергию пакета
# ==========================================
print("="*60)
print("Experiment A: T(E) — transmission vs energy")
print("="*60)

barrier_width = 1.0
V0 = 15.0
E_values = np.linspace(2.0, 25.0, 24)
T_num_list = []
T_analytical_list = []

for E in E_values:
    k0 = np.sqrt(2 * E)  # E = k^2 / 2
    psi0 = gaussian_wavepacket(x, x0, k0, sigma)
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)
    
    V = rectangular_barrier(x, 0.0, barrier_width, V0)
    psi = run_crank_nicolson(psi0, V, x, dt, n_steps)
    T_num, _ = compute_TR(psi, x, 0.0, barrier_width)
    
    T_an = transmission_coefficient_rectangular(E, V0, barrier_width)
    
    T_num_list.append(T_num)
    T_analytical_list.append(T_an)
    print(f"E = {E:5.1f}  T_num = {T_num:.6f}  T_an = {T_an:.6f}")

# Сохранение CSV
os.makedirs('results/raw', exist_ok=True)
with open('results/raw/sweep_energy.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['E', 'T_numerical', 'T_analytical'])
    for i in range(len(E_values)):
        writer.writerow([E_values[i], T_num_list[i], T_analytical_list[i]])

# График T(E)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(E_values, T_num_list, 'o-', label='Numerical (CN)', color='tab:blue')
ax.plot(E_values, T_analytical_list, '--', label='Analytical', color='tab:red')
ax.axvline(x=V0, color='gray', linestyle=':', label=f'V0 = {V0}')
ax.set_xlabel('E (packet energy)')
ax.set_ylabel('T (transmission)')
ax.set_title('Transmission vs Energy')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
plt.savefig('figures/sweep_energy.png', dpi=150)
plt.show()
print("Figure saved : figures/sweep_energy.png")
print()

# ==========================================
# Experiment B: T(V0) — меняем высоту барьера
# ==========================================
print("="*60)
print("Experiment B: T(V0) — transmission vs barrier height")
print("="*60)

E_fixed = 12.5
k0 = np.sqrt(2 * E_fixed)
V0_values = np.linspace(0.5, 25.0, 25)
T_num_list = []
T_analytical_list = []

for V0_val in V0_values:
    psi0 = gaussian_wavepacket(x, x0, k0, sigma)
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)
    
    V = rectangular_barrier(x, 0.0, barrier_width, V0_val)
    psi = run_crank_nicolson(psi0, V, x, dt, n_steps)
    T_num, _ = compute_TR(psi, x, 0.0, barrier_width)
    
    T_an = transmission_coefficient_rectangular(E_fixed, V0_val, barrier_width)
    
    T_num_list.append(T_num)
    T_analytical_list.append(T_an)
    print(f"V0 = {V0_val:5.1f}  T_num = {T_num:.6f}  T_an = {T_an:.6f}")

with open('results/raw/sweep_barrier_height.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['V0', 'T_numerical', 'T_analytical'])
    for i in range(len(V0_values)):
        writer.writerow([V0_values[i], T_num_list[i], T_analytical_list[i]])

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(V0_values, T_num_list, 'o-', label='Numerical (CN)', color='tab:blue')
ax.plot(V0_values, T_analytical_list, '--', label='Analytical', color='tab:red')
ax.axvline(x=E_fixed, color='gray', linestyle=':', label=f'E = {E_fixed}')
ax.set_xlabel('V0 (barrier height)')
ax.set_ylabel('T (transmission)')
ax.set_title('Transmission vs Barrier Height')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
plt.savefig('figures/sweep_barrier_height.png', dpi=150)
plt.show()
print("Figure saved: figures/sweep_barrier_height.png")
print()

# ==========================================
# Experiment C: T(a) — меняем ширину барьера
# ==========================================
print("="*60)
print("Experiment C: T(a) — transmission vs barrier width")
print("="*60)

E_fixed = 12.5
k0 = np.sqrt(2 * E_fixed)
V0 = 15.0
a_values = np.linspace(0.2, 3.0, 15)
T_num_list = []
T_analytical_list = []

for a in a_values:
    psi0 = gaussian_wavepacket(x, x0, k0, sigma)
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dx)
    
    V = rectangular_barrier(x, 0.0, a, V0)
    psi = run_crank_nicolson(psi0, V, x, dt, n_steps)
    T_num, _ = compute_TR(psi, x, 0.0, a)
    
    T_an = transmission_coefficient_rectangular(E_fixed, V0, a)
    
    T_num_list.append(T_num)
    T_analytical_list.append(T_an)
    print(f"a = {a:5.2f}  T_num = {T_num:.6f}  T_an = {T_an:.6f}")

with open('results/raw/sweep_barrier_width.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['a', 'T_numerical', 'T_analytical'])
    for i in range(len(a_values)):
        writer.writerow([a_values[i], T_num_list[i], T_analytical_list[i]])

fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogy(a_values, T_num_list, 'o-', label='Numerical (CN)', color='tab:blue')
ax.semilogy(a_values, T_analytical_list, '--', label='Analytical', color='tab:red')
ax.set_xlabel('a (barrier width)')
ax.set_ylabel('T (transmission, log scale)')
ax.set_title('Transmission vs Barrier Width (log scale)')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
plt.savefig('figures/sweep_barrier_width.png', dpi=150)
plt.show()
print("Figure saved: figures/sweep_barrier_width.png")