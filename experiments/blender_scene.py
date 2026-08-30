"""
Premium Blender scene for quantum tunneling visualization.
"""

import bpy
import numpy as np
import json
import os
import math

# --- Очистка ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

# --- Загрузка данных ---
json_path = r"C:\Users\ahilg\Desktop\quantumtunnelingvisualizer\results\blender\wavefunction_frames.json"
with open(json_path, 'r') as f:
    data = json.load(f)

x = np.array(data['x'])
frames = data['frames']
n_frames = len(frames)

# --- Параметры ---
barrier_height = 0.35
wave_scale = 18.0
barrier_start = data['barrier_start']
barrier_width = data['barrier_width']

# --- Барьер (стеклянный) ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(barrier_start + barrier_width/2, 0, barrier_height/2),
    scale=(barrier_width, 3.5, barrier_height)
)
barrier = bpy.context.active_object
barrier.name = "Barrier"

mat_barrier = bpy.data.materials.new(name="BarrierGlass")
mat_barrier.use_nodes = True
nodes = mat_barrier.node_tree.nodes
principled = nodes["Principled BSDF"]
principled.inputs[0].default_value = (1.0, 0.2, 0.2, 1.0)
principled.inputs[21].default_value = 0.4  # Alpha
principled.inputs[19].default_value = 0.1  # Roughness
principled.inputs[14].default_value = 1.45  # IOR
barrier.data.materials.append(mat_barrier)

# --- Волновая поверхность ---
prob = np.array(frames[0]['probability'])
verts = []
faces = []

for i, xi in enumerate(x):
    y = prob[i] * wave_scale
    verts.append((xi, 0, 0))
    verts.append((xi, y, 0))

for i in range(len(x) - 1):
    v0 = i * 2
    v1 = i * 2 + 1
    v2 = (i + 1) * 2 + 1
    v3 = (i + 1) * 2
    faces.append((v0, v1, v2, v3))

mesh = bpy.data.meshes.new("WaveMesh")
mesh.from_pydata(verts, [], faces)
mesh.update()

obj = bpy.data.objects.new("WaveFunction", mesh)
bpy.context.collection.objects.link(obj)

# Неоновый материал волны
mat_wave = bpy.data.materials.new(name="WaveNeon")
mat_wave.use_nodes = True
nodes = mat_wave.node_tree.nodes
principled = nodes["Principled BSDF"]
principled.inputs[0].default_value = (0.0, 0.7, 1.0, 1.0)
principled.inputs[21].default_value = 0.6
principled.inputs[26].default_value = 3.0  # Сильное свечение
obj.data.materials.append(mat_wave)

# --- Сетка-пол ---
bpy.ops.mesh.primitive_grid_add(
    x_subdivisions=40,
    y_subdivisions=20,
    size=40,
    location=(0, 0, -0.01)
)
floor = bpy.context.active_object
floor.name = "Floor"

mat_floor = bpy.data.materials.new(name="FloorMat")
mat_floor.use_nodes = True
nodes = mat_floor.node_tree.nodes
principled = nodes["Principled BSDF"]
principled.inputs[0].default_value = (0.05, 0.05, 0.08, 1.0)
principled.inputs[7].default_value = 0.5  # Metallic
principled.inputs[9].default_value = 0.3  # Roughness
floor.data.materials.append(mat_floor)

# --- Частицы (точки на сетке) ---
bpy.ops.mesh.primitive_ico_sphere_add(
    subdivisions=2,
    radius=0.06,
    location=(0, 0, 0)
)
particle = bpy.context.active_object

mat_particle = bpy.data.materials.new(name="ParticleMat")
mat_particle.use_nodes = True
nodes = mat_particle.node_tree.nodes
principled = nodes["Principled BSDF"]
principled.inputs[0].default_value = (0.0, 1.0, 0.8, 1.0)
principled.inputs[26].default_value = 5.0
particle.data.materials.append(mat_particle)

# --- Камера ---
bpy.ops.object.camera_add(location=(0, -10, 4))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(72), 0, 0)
bpy.context.scene.camera = camera
camera.data.dof.use_dof = True
camera.data.dof.focus_distance = 10
camera.data.dof.aperture_fstop = 2.8

# --- Освещение ---
bpy.ops.object.light_add(type='SUN', location=(5, -5, 8))
sun = bpy.context.active_object
sun.data.energy = 2.0
sun.data.color = (0.9, 0.95, 1.0)

bpy.ops.object.light_add(type='POINT', location=(0, -2, 4))
point1 = bpy.context.active_object
point1.data.energy = 100.0
point1.data.color = (0.0, 0.6, 1.0)

bpy.ops.object.light_add(type='POINT', location=(0, 3, 2))
point2 = bpy.context.active_object
point2.data.energy = 50.0
point2.data.color = (1.0, 0.3, 0.3)

# --- Мир ---
world = bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.01, 0.03, 1.0)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.5

# --- Рендер ---
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 64
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.film_transparent = True

print("Premium scene created!")
print(f"Objects: barrier, wave, floor, particles, camera, lights, volume")