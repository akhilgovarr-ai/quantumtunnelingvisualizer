import numpy as np
import matplotlib.pyplot as plt

# --- Параметры сетки (пространство x) ---
x_min = -20.0
x_max = 20.0
N = 1000
x = np.linspace(x_min, x_max, N)
dx = x[1] - x[0]

# --- Параметры начального волнового пакета ---
x0 = -10.0
sigma = 1.0
k0 = 5.0

# --- Параметры барьера ---
V0 = 15.0
barrier_start = 0.0
barrier_width = 1.0

V = np.zeros_like(x)
V[(x >= barrier_start) & (x <= barrier_start + barrier_width)] = V0

# --- Собираем гауссов волновой пакет ---
psi0 = np.exp(-(x - x0)**2 / (4 * sigma**2)) * np.exp(1j * k0 * x)

# --- Нормировка ---
norm = np.sqrt(np.sum(np.abs(psi0)**2) * dx)
psi0 = psi0 / norm

# --- Проверка нормировки ---
check_norm = np.sum(np.abs(psi0)**2) * dx
print(f"Норма пакета: {check_norm:.6f}")

# --- Параметры временной эволюции ---
dt = 0.01
n_steps = 2000

# --- Волновые числа k для FFT ---
# np.fft.fftfreq даёт частоты в специальном порядке, подходящем для FFT/IFFT
k = 2 * np.pi * np.fft.fftfreq(N, d=dx)

print(f"Диапазон k: от {k.min():.2f} до {k.max():.2f}")
print(f"Количество точек k: {len(k)}")

# --- График: пакет и барьер вместе (проверка, что стартовые условия совпадают с CN) ---
fig, ax1 = plt.subplots(figsize=(8, 4))

ax1.plot(x, np.abs(psi0)**2, color="tab:blue", label=r"$|\psi(x,0)|^2$")
ax1.set_xlabel("x")
ax1.set_ylabel(r"$|\psi(x,0)|^2$", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

ax2 = ax1.twinx()
ax2.plot(x, V, color="tab:red", linestyle="--", label="V(x)")
ax2.set_ylabel("V(x)", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")

plt.title("SSF: начальный волновой пакет и барьер (та же настройка, что и CN)")
fig.tight_layout()
plt.savefig("figures/ssf_initial_setup.png", dpi=150)
plt.show()