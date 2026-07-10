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
# --- Параметры временной эволюции ---
dt = 0.01        # маленький шаг по времени
hbar = 1.0       # безразмерные единицы
m = 1.0

# --- Собираем гамильтониан H в виде трёх диагоналей ---
# H действует так: (H*psi)_j = -0.5/dx^2 * (psi[j+1] - 2*psi[j] + psi[j-1]) + V[j]*psi[j]
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

N_points = len(x)
main_diag = V + 1.0 / dx**2          # главная диагональ H
off_diag = -0.5 / dx**2 * np.ones(N_points - 1)   # соседние диагонали H

H = diags([off_diag, main_diag, off_diag], offsets=[-1, 0, 1], format="csc")

# --- Собираем матрицы A и B схемы Кранка-Николсон ---
I = diags([np.ones(N_points)], offsets=[0], format="csc")
A = I + 1j * dt / 2 * H
B = I - 1j * dt / 2 * H

# --- Цикл эволюции по времени ---
n_steps = 2000     # сколько шагов сделать всего
psi = psi0.copy()  # текущее состояние, будет обновляться на каждом шаге

norm_history = []  # сюда будем складывать норму на каждом шаге — для проверки

for step in range(n_steps):
    psi = spsolve(A, B @ psi)
    current_norm = np.sum(np.abs(psi)**2) * dx
    norm_history.append(current_norm)

print(f"Норма в начале: {norm_history[0]:.6f}")
print(f"Норма в конце ({n_steps} шагов): {norm_history[-1]:.6f}")
print(f"Максимальное отклонение нормы: {max(abs(n - 1.0) for n in norm_history):.2e}")

# --- Разделяем финальную волновую функцию на "прошло" и "отразилось" ---
transmitted = np.sum(np.abs(psi[x > barrier_start + barrier_width])**2) * dx
reflected = np.sum(np.abs(psi[x < barrier_start])**2) * dx

print(f"Вероятность прохождения (туннелирование): {transmitted:.4f}")
print(f"Вероятность отражения: {reflected:.4f}")

# --- График: начальное и финальное состояние + барьер ---
fig, ax1 = plt.subplots(figsize=(9, 4.5))

ax1.plot(x, np.abs(psi0)**2, color="tab:blue", alpha=0.5, linestyle=":", label=r"$|\psi(x,0)|^2$ (начало)")
ax1.plot(x, np.abs(psi)**2, color="tab:blue", label=rf"$|\psi(x,t={n_steps*dt:.1f})|^2$ (конец)")
ax1.set_xlabel("x")
ax1.set_ylabel(r"$|\psi(x,t)|^2$", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax1.legend(loc="upper left")

ax2 = ax1.twinx()
ax2.plot(x, V, color="tab:red", linestyle="--", label="V(x)")
ax2.set_ylabel("V(x)", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")

plt.title(f"Туннелирование через барьер (T={transmitted:.3f}, R={reflected:.3f})")
fig.tight_layout()
plt.savefig("figures/tunneling_result.png", dpi=150)
plt.show()
