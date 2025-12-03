import xarray as xr
import numpy as np
import glob
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
import os

# -----------------------------
# Charger tous les fichiers
# -----------------------------
data_folder = 'Tropical_data'
input_pattern = os.path.join(data_folder, 'tropical_days_per_year_*.nc')
input_files = sorted(glob.glob(input_pattern))

datasets = [xr.open_dataset(f) for f in input_files]
combined = xr.concat(datasets, dim='year')

# Convertir tropical_days en nombre de jours
tropical_days_in_days = combined['tropical_days'] / np.timedelta64(1, 'D')

# Coordonnées
x = combined['x'].values.astype(float)
y = combined['y'].values.astype(float)
if np.issubdtype(combined['year'].dtype, np.datetime64):
    years = combined['year'].dt.year.values
else:
    years = combined['year'].values

# -----------------------------
# Créer la figure pour animation
# -----------------------------
fig, ax = plt.subplots(figsize=(8,6))
mesh = ax.pcolormesh(x, y, tropical_days_in_days[0, :, :], shading='auto', cmap='Reds')
cbar = plt.colorbar(mesh, ax=ax)
cbar.set_label('Nuits tropicales')
title = ax.set_title(f'Nuits tropicales - Année {years[0]}')
ax.set_xlabel('x')
ax.set_ylabel('y')

# Définir limites couleurs pour stabilité visuelle
vmin = np.nanmin(tropical_days_in_days.values)
vmax = np.nanmax(tropical_days_in_days.values)
mesh.set_clim(vmin, vmax)

# -----------------------------
# Fonction d’animation pour afficher toutes les années
# -----------------------------
def update(frame):
    mesh.set_array(tropical_days_in_days[frame, :, :].values.ravel())
    title.set_text(f'Nuits tropicales - Année {years[frame]}')
    return mesh, title

# -----------------------------
# Créer l’animation
# -----------------------------
anim = FuncAnimation(fig, update, frames=len(years), blit=False)

# -----------------------------
# Sauvegarder directement la vidéo
# -----------------------------
output_video = 'tropical_animations/tropical_days_evolution.mp4'
writer = FFMpegWriter(fps=8)
anim.save(output_video, writer=writer)
print(f"Vidéo créée : {output_video}")

# -----------------------------
# Sauvegarder directement un GIF
# -----------------------------
output_gif = 'tropical_animations/tropical_days_evolution.gif'
gif_writer = PillowWriter(fps=8)
anim.save(output_gif, writer=gif_writer)
print(f"GIF créé : {output_gif}")

# -----------------------------
# Définir les intervalles
# -----------------------------
intervals = [
    (1990, 2000),
    (2000, 2020),
    (2020, 2040),
    (2040, 2060),
    (2060, 2080),
    (2080, 2100)
]

mean_slices = []
interval_labels = []

for start, end in intervals:
    mask = (years >= start) & (years < end)
    mean_slice = tropical_days_in_days[mask, :, :].mean(dim='year')
    mean_slices.append(mean_slice)
    interval_labels.append(f"{start}-{end}")

mean_slices = xr.concat(mean_slices, dim='interval')


fig, ax = plt.subplots(figsize=(8,6))
mesh = ax.pcolormesh(x, y, mean_slices[0, :, :], shading='auto', cmap='Reds')
cbar = plt.colorbar(mesh, ax=ax)
cbar.set_label('Nuits tropicales')
title = ax.set_title(f'Nuits tropicales - Intervalle {interval_labels[0]}')
ax.set_xlabel('x')
ax.set_ylabel('y')

# Définir limites couleurs pour stabilité visuelle
vmin = np.nanmin(mean_slices.values)
vmax = np.nanmax(mean_slices.values)
mesh.set_clim(vmin, vmax)

# -----------------------------
# Fonction d’animation pour afficher par intervalles
# -----------------------------
def update_intervals(frame):
    mesh.set_array(mean_slices[frame, :, :].values.ravel())
    title.set_text(f'Nuits tropicales - Intervalle {interval_labels[frame]}')
    return mesh, title

# -----------------------------
# Créer l’animation
# -----------------------------
anim = FuncAnimation(fig, update_intervals, frames=len(mean_slices), blit=False)

# -----------------------------
# Sauvegarder directement la vidéo
# -----------------------------
output_video = 'tropical_animations/tropical_days_intervals.mp4'
writer = FFMpegWriter(fps=1)  # plus lent pour visualiser chaque intervalle
anim.save(output_video, writer=writer)
print(f"Vidéo créée : {output_video}")

# -----------------------------
# Sauvegarder directement un GIF
# -----------------------------
output_gif = 'tropical_animations/tropical_days_intervals.gif'
gif_writer = PillowWriter(fps=1)
anim.save(output_gif, writer=gif_writer)
print(f"GIF créé : {output_gif}")