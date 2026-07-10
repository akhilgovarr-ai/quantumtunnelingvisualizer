import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

# --- Общие параметры (одинаковые для обоих методов) ---
x_min, x_max, N = -20.0, 20.0, 1000
x = np.linspace(x_min, x_max, N)
dx = x[1] - x[0]

x0, sigma, k0 = -10.0, 1.0, 5.0
V0, barrier_start, barrier_width = 15.0, 0.0, 1.0

V = np.zeros_like(x)
V[(x >= barrier_start) & (x <= barrier_start + barrier_width)] = V0

psi_start = np.exp(-(x - x0)**2 / (4 * sigma**2)) * np.exp(1j * k0 * x)
norm = np.sqrt(np.sum(np.abs(psi_start)**2) * dx)
psi_start = psi_start / norm

dt = 0.01
n_steps = 400

def run_crank_nicolson():
    main_diag = V + 1.0 / dx**2
    off_diag = -0.5 / dx**2 * np.ones(N - 1)
    H = diags([off_diag, main_diag, off_diag], offsets=[-1, 0, 1], format="csc")
    I = diags([np.ones(N)], offsets=[0], format="csc")
    A = I + 1j * dt / 2 * H
    B = I - 1j * dt / 2 * H

    psi = psi_start.copy()
    for _ in range(n_steps):
        psi = spsolve(A, B @ psi)
    return psi

def run_split_step_fourier():
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    psi = psi_start.copy()
    for _ in range(n_steps):
        psi = psi * np.exp(-1j * V * dt / 2)
        psi_k = np.fft.fft(psi)
        psi_k = psi_k * np.exp(-1j * k**2 * dt / 2)
        psi = np.fft.ifft(psi_k)
        psi = psi * np.exp(-1j * V * dt / 2)
    return psi

# --- Запускаем оба метода ---
print("Считаю Crank-Nicolson...")
psi_cn = run_crank_nicolson()

print("Считаю Split-Step Fourier...")
psi_ssf = run_split_step_fourier()

# --- Считаем T и R для каждого ---
def compute_TR(psi):
    T = np.sum(np.abs(psi[x > barrier_start + barrier_width])**2) * dx
    R = np.sum(np.abs(psi[x < barrier_start])**2) * dx
    return T, R

T_cn, R_cn = compute_TR(psi_cn)
T_ssf, R_ssf = compute_TR(psi_ssf)

print(f"\nCrank-Nicolson:      T = {T_cn:.4f}, R = {R_cn:.4f}")
print(f"Split-Step Fourier:  T = {T_ssf:.4f}, R = {R_ssf:.4f}")
print(f"Разница по T: {abs(T_cn - T_ssf):.4f}")
print(f"Разница по R: {abs(R_cn - R_ssf):.4f}")

# --- Разница между волновыми функциями в каждой точке ---
diff = np.abs(np.abs(psi_cn)**2 - np.abs(psi_ssf)**2)
print(f"Максимальная разница |ψ|² в точке: {diff.max():.2e}")

# --- График: оба метода рядом ---
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