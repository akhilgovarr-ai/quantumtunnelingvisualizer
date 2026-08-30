import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'solver'))

from wavepacket import gaussian_wavepacket
from potentials import rectangular_barrier
from crank_nicolson import run_crank_nicolson

# --- Параметры ---
x_min, x_max = -20.0, 20.0
N = 500
x = np.linspace(x_min, x_max, N)
dx = x[1] - x[0]

x0, sigma, k0 = -12.0, 2.0, 5.0
V0, barrier_start, barrier_width = 15.0, 0.0, 1.0

V = rectangular_barrier(x, barrier_start, barrier_width, V0)
psi = gaussian_wavepacket(x, x0, k0, sigma)
psi = psi / np.sqrt(np.sum(np.abs(psi)**2) * dx)

dt = 0.01
n_steps = 300
save_every = 10

# --- Симуляция с сохранением кадров ---
print("Running simulation...")
frames = []

for step in range(1, n_steps + 1):
    psi = run_crank_nicolson(psi, V, x, dt, 1)
    if step % save_every == 0:
        probability = np.abs(psi)**2
        frames.append({
            'x': x.tolist(),
            'probability': probability.tolist(),
            'time': step * dt
        })

print(f"Frames saved: {len(frames)}")

# --- Экспорт в JSON для Blender ---
import json

os.makedirs('results/blender', exist_ok=True)

data = {
    'x': x.tolist(),
    'V': V.tolist(),
    'barrier_start': barrier_start,
    'barrier_width': barrier_width,
    'V0': V0,
    'frames': frames
}

with open('results/blender/wavefunction_frames.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Exported: results/blender/wavefunction_frames.json")
print(f"File size: {os.path.getsize('results/blender/wavefunction_frames.json') / 1024:.1f} KB")