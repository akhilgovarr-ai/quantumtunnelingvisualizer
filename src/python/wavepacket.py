import numpy as np
import matplotlib.pyplot as plt

# --- Параметры сетки (пространство x) ---
x_min = -20.0       # левая граница расчётной области
x_max = 20.0        # правая граница
N = 1000            # количество точек сетки
x = np.linspace(x_min, x_max, N)
dx = x[1] - x[0]    # шаг сетки

# --- Параметры начального волнового пакета ---
x0 = -10.0          # начальный центр пакета (слева, чтобы двигался к барьеру справа)
sigma = 1.0         # ширина пакета
k0 = 5.0            # начальный "импульс" (задаёт скорость движения пакета)

# --- Параметры барьера ---
V0 = 15.0        # высота барьера (чем больше, тем сильнее отражение)
barrier_start = 0.0    # где начинается барьер
barrier_width = 1.0    # ширина барьера

# --- Строим потенциал V(x): 0 везде, кроме области барьера ---
V = np.zeros_like(x)
V[(x >= barrier_start) & (x <= barrier_start + barrier_width)] = V0
# --- Собираем гауссов волновой пакет ---
psi0 = np.exp(-(x - x0)**2 / (4 * sigma**2)) * np.exp(1j * k0 * x)

# --- Нормировка: делаем так, чтобы интеграл |psi|^2 dx = 1 ---
norm = np.sqrt(np.sum(np.abs(psi0)**2) * dx)
psi0 = psi0 / norm

# --- Проверка нормировки ---
check_norm = np.sum(np.abs(psi0)**2) * dx
print(f"Норма пакета: {check_norm:.6f}")  # должно быть очень близко к 1.0

# --- График: пакет и барьер вместе ---
fig, ax1 = plt.subplots(figsize=(8, 4))

ax1.plot(x, np.abs(psi0)**2, color="tab:blue", label=r"$|\psi(x,0)|^2$")
ax1.set_xlabel("x")
ax1.set_ylabel(r"$|\psi(x,0)|^2$", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

ax2 = ax1.twinx()
ax2.plot(x, V, color="tab:red", linestyle="--", label="V(x)")
ax2.set_ylabel("V(x)", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")

plt.title("Начальный волновой пакет и потенциальный барьер")
fig.tight_layout()
plt.savefig("figures/wavepacket_and_barrier.png", dpi=150)
plt.show()
