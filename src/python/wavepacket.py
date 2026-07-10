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

# --- Собираем гауссов волновой пакет ---
psi0 = np.exp(-(x - x0)**2 / (4 * sigma**2)) * np.exp(1j * k0 * x)

# --- Нормировка: делаем так, чтобы интеграл |psi|^2 dx = 1 ---
norm = np.sqrt(np.sum(np.abs(psi0)**2) * dx)
psi0 = psi0 / norm

# --- Проверка нормировки ---
check_norm = np.sum(np.abs(psi0)**2) * dx
print(f"Норма пакета: {check_norm:.6f}")  # должно быть очень близко к 1.0

# --- График ---
plt.figure(figsize=(8, 4))
plt.plot(x, np.abs(psi0)**2, label=r"$|\psi(x,0)|^2$")
plt.xlabel("x")
plt.ylabel("плотность вероятности")
plt.title("Начальный гауссов волновой пакет")
plt.legend()
plt.grid(True)
plt.savefig("figures/initial_wavepacket.png", dpi=150)
plt.show()