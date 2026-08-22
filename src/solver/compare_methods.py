import numpy as np
import matplotlib.pyplot as plt

from wavepacket import gaussian_wavepacket
from potentials import rectangular_barrier
from crank_nicolson import run_crank_nicolson
from split_step_fourier import run_split_step_fourier

# Единицы измерения:
# Вся симуляция выполняется в безразмерных единицах, где
# hbar = 1, m = 1.
# Физические параметры (энергия, ширина барьера) масштабируются
# при переходе к реальным системам через характерные масштабы.

# --- Общие параметры ---
x_min, x_max, N = -20.0, 20.0, 1000
x = np.linspace(x_min, x_max, N)
dx = x[1] - x[0]

x0, sigma, k0 = -10.0, 1.0, 5.0
V0, barrier_start, barrier_width = 15.0, 0.0, 1.0

# Потенциал и начальное состояние
V = rectangular_barrier(x, barrier_start, barrier_width, V0)
psi0 = gaussian_wavepacket(x, x0, k0, sigma)

# Нормировка (функция gaussian_wavepacket уже нормирована аналитически,
# но численная нормировка на сетке — обязательная проверка)
norm = np.sqrt(np.sum(np.abs(psi0)**2) * dx)
psi0 = psi0 / norm

dt = 0.01
n_steps = 400

# --- Запуск обоих методов ---
print("Считаю Crank-Nicolson...")
psi_cn = run_crank_nicolson(psi0, V, x, dt, n_steps)

print("Считаю Split-Step Fourier...")
psi_ssf = run_split_step_fourier(psi0, V, x, dt, n_steps)

# --- Вычисление T и R ---
from observables import compute_TR, compute_norm

T_cn, R_cn = compute_TR(psi_cn, x, barrier_start, barrier_width)
T_ssf, R_ssf = compute_TR(psi_ssf, x, barrier_start, barrier_width)

# Проверка сохранения нормы
norm_cn = compute_norm(psi_cn, x)
norm_ssf = compute_norm(psi_ssf, x)
print(f"\nНорма CN:  {norm_cn:.6f}")
print(f"Норма SSF: {norm_ssf:.6f}")
print(f"\nCrank-Nicolson:      T = {T_cn:.4f}, R = {R_cn:.4f}")
print(f"Split-Step Fourier:  T = {T_ssf:.4f}, R = {R_ssf:.4f}")
print(f"Разница по T: {abs(T_cn - T_ssf):.4f}")
print(f"Разница по R: {abs(R_cn - R_ssf):.4f}")

# --- Разница между волновыми функциями ---
diff = np.abs(np.abs(psi_cn)**2 - np.abs(psi_ssf)**2)
print(f"Максимальная разница |ψ|² в точке: {diff.max():.2e}")

# --- График ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

ax1.plot(x, np.abs(psi_cn)**2, color="tab:blue", label="Crank-Nicolson")
ax1.plot(x, np.abs(psi_ssf)**2, color="tab:green", linestyle="--", label="Split-Step Fourier")
ax1_v = ax1.twinx()
ax1_v.plot(x, V, color="tab:red", linestyle=":", alpha=0.7)
ax1_v.set_ylabel("V(x)", color="tab:red")
ax1.set_ylabel(r"$|\psi(x,t)|^2$")
ax1.set_title(f"Сравнение методов (t={n_steps*dt:.1f})")
ax1.legend(loc="upper left")

ax2.plot(x, diff, color="black")
ax2.set_xlabel("x")
ax2.set_ylabel("|разница|")
ax2.set_title("Абсолютная разница между методами в каждой точке")

fig.tight_layout()
plt.savefig("figures/methods_comparison.png", dpi=150)
plt.show()

print(f"\nE_packet = {k0**2 / 2:.4f}")
print(f"V0 = {V0:.4f}")
print(f"dx = {dx:.3e}")
print(f"dt = {dt:.3e}")