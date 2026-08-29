import numpy as np
from observables import compute_norm, compute_TR, compute_mean_position

def print_scientific_summary(psi_cn, psi_ssf, x, V, barrier_start, barrier_width, dt, n_steps, k0):
    """
    Выводит полное научное резюме симуляции.

    Parameters
    ----------
    psi_cn, psi_ssf : np.ndarray
        Волновые функции после эволюции (CN и SSF).
    x : np.ndarray
        Пространственная сетка.
    V : np.ndarray
        Потенциал.
    barrier_start, barrier_width : float
        Параметры барьера.
    dt, n_steps : float, int
        Параметры времени.
    k0 : float
        Начальный волновой вектор.
    """
    dx = x[1] - x[0]
    E_packet = k0**2 / 2
    V0 = V.max()

    print("=" * 60)
    print("SCIENTIFIC OUTPUT")
    print("=" * 60)

    # Основные параметры
    print(f"\nParameters:")
    print(f"  Grid: N = {len(x)}, dx = {dx:.4e}")
    print(f"  Time: dt = {dt:.4e}, n_steps = {n_steps}, t_final = {n_steps*dt:.2f}")
    print(f"  Packet energy: E = {E_packet:.4f}")
    print(f"  Barrier: V0 = {V0:.4f}, width = {barrier_width:.4f}")

    # Нормы
    norm_cn = compute_norm(psi_cn, x)
    norm_ssf = compute_norm(psi_ssf, x)
    print(f"\nNorm Conservation:")
    print(f"  CN:  {norm_cn:.8f} (error: {abs(norm_cn - 1.0):.2e})")
    print(f"  SSF: {norm_ssf:.8f} (error: {abs(norm_ssf - 1.0):.2e})")

    # T и R
    T_cn, R_cn = compute_TR(psi_cn, x, barrier_start, barrier_width)
    T_ssf, R_ssf = compute_TR(psi_ssf, x, barrier_start, barrier_width)

    print(f"\nTransmission and Reflection:")
    print(f"  CN:  T = {T_cn:.6f}, R = {R_cn:.6f}, R+T = {R_cn + T_cn:.6f}")
    print(f"  SSF: T = {T_ssf:.6f}, R = {R_ssf:.6f}, R+T = {R_ssf + T_ssf:.6f}")

    # Разница методов
    print(f"\nMethod Comparison:")
    print(f"  |T_CN - T_SSF| = {abs(T_cn - T_ssf):.6f}")
    print(f"  |R_CN - R_SSF| = {abs(R_cn - R_ssf):.6f}")
    diff_max = np.max(np.abs(np.abs(psi_cn)**2 - np.abs(psi_ssf)**2))
    print(f"  max |ψ_CN|² - |ψ_SSF|² = {diff_max:.2e}")

    # Средние значения
    x_mean_cn = compute_mean_position(psi_cn, x)
    x_mean_ssf = compute_mean_position(psi_ssf, x)
    print(f"\nMean Position:")
    print(f"  CN:  <x> = {x_mean_cn:.4f}")
    print(f"  SSF: <x> = {x_mean_ssf:.4f}")

    print("=" * 60)