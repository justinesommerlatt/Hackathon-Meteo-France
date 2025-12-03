import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter

# -----------------------------
# Lecture des fichiers CSV
# -----------------------------
df = pd.read_csv("ligne_crete_cols.csv", sep=";")
df = df[df['Altitude_Sommet'].notna()]

# Conversion en nombres
cols_num = ['Altitude_Sommet', 'Altitude_Préfécture',
            'Altitude_basse_station de ski', 'Altitude_haute_station de ski']
for col in cols_num:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remplacer les noms manquants
df['Nom_station de ski'] = df['Nom_station de ski'].fillna('')
x = np.arange(len(df))

# -----------------------------
# Lecture des isothermes
# -----------------------------
# Iso
iso_df = pd.read_csv("isotherme_0_averaged_stats.csv", index_col=0)
iso_df.columns = iso_df.columns.str.strip()
isothermes = {}
for periode, row in iso_df.iterrows():
    isothermes[periode] = {
        "Isotherme 0° pour l'année la plus froide sur la période": row["min_elevation"],
        "Isotherme 0° moyen sur la période": row["mean_elevation"],
        "Isotherme 0° pour l'année la plus chaude sur la période": row["max_elevation"],
    }
colors_iso = {
    "Isotherme 0° pour l'année la plus froide sur la période": "#2EA8FF",
    "Isotherme 0° moyen sur la période": "#8ACEFF",
    "Isotherme 0° pour l'année la plus chaude sur la période": "#B3DFFF"
}

# Tropic
tropic_df = pd.read_csv("tropical_averaged_stats.csv", index_col=0)
tropic_df.columns = tropic_df.columns.str.strip()
tropic_isothermes = {}
for periode, row in tropic_df.iterrows():
    tropic_isothermes[periode] = {
        "Tropic 0° pour l'année la plus froide sur la période": row["min_elevation"],
        "Tropic 0° moyen sur la période": row["mean_elevation"],
        "Altitude maximale du seuil 20°": row["max_elevation"],
    }
colors_tropic = {
    "Tropic 0° pour l'année la plus froide sur la période": "#FF9F2E",
    "Tropic 0° moyen sur la période": "#FFC37A",
    "Altitude maximale du seuil 20°": "#D10000"
}

# -----------------------------
# Tracé par période
# -----------------------------
for periode, stats in isothermes.items():
    plt.figure(figsize=(30, 12))

    # Fond gris pour la crête
    plt.fill_between(x, df['Altitude_Sommet'], color='#C2C2C2', alpha=0.5)

    # Crête
    plt.plot(x, df['Altitude_Sommet'], color='grey', marker='', label='Sommet', linewidth=2)

    # Noms des sommets
    for xi, yi, nom in zip(x, df['Altitude_Sommet'], df['Nom_Sommet']):
        plt.text(xi, yi + 80, nom, ha='center', va='bottom', fontsize=9)

    # Préfectures
    plt.scatter(x, df['Altitude_Préfécture'], color='darkgrey', marker='x', s=100, label='Préfecture')
    for xi, yi, nom in zip(x, df['Altitude_Préfécture'], df['Nom_prefecture']):
        plt.text(xi, yi + 80, nom, ha='center', va='bottom', fontsize=8)

    # Stations de ski
    mask_stations = df['Nom_station de ski'] != ''
    for xi, yb, yh in zip(x[mask_stations], df.loc[mask_stations, 'Altitude_basse_station de ski'],
                          df.loc[mask_stations, 'Altitude_haute_station de ski']):
        plt.plot([xi, xi], [yb, yh], color='#BDF4FF', linestyle='-', linewidth=8)
    # Légende unique pour les stations
    plt.plot([], [], color='#BDF4FF', linestyle='-', linewidth=8, label='Espace couvert par le domaine skiable')

    # Lignes isothermes
    for key in [
        "Isotherme 0° pour l'année la plus froide sur la période",
        "Isotherme 0° moyen sur la période",
        "Isotherme 0° pour l'année la plus chaude sur la période"
    ]:
        linestyle = '--' if key != "Isotherme 0° moyen sur la période" else '-'
        plt.axhline(y=stats[key], color=colors_iso[key], linestyle=linestyle, linewidth=4,
                    label=f'{key} {periode}')

    # Lignes tropic

    # Seuil 20° maximum uniquement
    tropic_stats = tropic_isothermes[periode]
    plt.axhline(
        y=tropic_stats["Altitude maximale du seuil 20°"],
        color=colors_tropic["Altitude maximale du seuil 20°"],
        linestyle='--',  # trait plein
        linewidth=4,
        label=f'Altitude maximale du seuil 20° sur la période {periode}'
    )

    # Départements
    plt.xticks(x, df['Département'], rotation=45, ha='right')
    plt.ylabel("Altitude (m)")
    plt.title(f"Profil de crêtes avec altitudes de l'isotherme 0°C et tropic ({periode})")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # Sauvegarder l'image
    output_path = f"crete_animations/profile_0C_{periode.replace('-', '_')}v2.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

# -----------------------------
# Animation
# -----------------------------
image_folder = "crete_animations"
images = [
    os.path.join(image_folder, f"profile_0C_{periode.replace('-', '_')}v2.png")
    for periode in isothermes.keys()
]

fig, ax = plt.subplots(figsize=(30, 12))
img_display = ax.imshow(mpimg.imread(images[0]))
ax.axis('off')

def update(frame):
    img_display.set_data(mpimg.imread(images[frame]))
    return img_display

anim = FuncAnimation(fig, update, frames=len(images), blit=False)

# Vidéo
output_video = os.path.join(image_folder, "crete_animationv2.mp4")
writer = FFMpegWriter(fps=1)
anim.save(output_video, writer=writer)
print(f"Vidéo créée : {output_video}")

# GIF
output_gif = os.path.join(image_folder, "crete_animationv2.gif")
gif_writer = PillowWriter(fps=1)
anim.save(output_gif, writer=gif_writer)
print(f"GIF créé : {output_gif}")
