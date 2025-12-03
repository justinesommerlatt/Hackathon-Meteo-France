import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Lecture du fichier CSV
df = pd.read_csv("ligne_crete_cols.csv", sep=";")

# Garder uniquement les lignes avec un sommet
df = df[df['Altitude_Sommet'].notna()]

# Conversion des colonnes en nombres
df['Altitude_Sommet'] = pd.to_numeric(df['Altitude_Sommet'], errors='coerce')
df['Altitude_Préfécture'] = pd.to_numeric(df['Altitude_Préfécture'], errors='coerce')
df['Altitude_basse_station de ski'] = pd.to_numeric(df['Altitude_basse_station de ski'], errors='coerce')
df['Altitude_haute_station de ski'] = pd.to_numeric(df['Altitude_haute_station de ski'], errors='coerce')

# Remplacer les noms de stations manquants par chaîne vide
df['Nom_station de ski'] = df['Nom_station de ski'].fillna('')

# Conversion de x en array
x = np.arange(len(df))

# Isothermes 0°C pour les 4 périodes avec min, mean et max
#isothermes = {
    #"2020-2040": {"Isotherme 0° pour l'année la plus froide sur la période": 1347.0, "Isotherme 0° moyen sur la période": 2039.4, "Isotherme 0° pour l'année la plus chaude sur la période": 2617.0},
    #"2041-2060": {"Isotherme 0° pour l'année la plus froide sur la période": 1675.0, "Isotherme 0° moyen sur la période": 2231.5, "Isotherme 0° pour l'année la plus chaude sur la période": 2750.0},
    #"2061-2080": {"Isotherme 0° pour l'année la plus froide sur la période": 1742.0, "Isotherme 0° moyen sur la période": 2339.5, "Isotherme 0° pour l'année la plus chaude sur la période": 2793.0},
    #"2081-2100": {"Isotherme 0° pour l'année la plus froide sur la période": 2126.0, "Isotherme 0° moyen sur la période": 2565.5, "Isotherme 0° pour l'année la plus chaude sur la période": 2999.0}
#}

# NEW
iso_df = pd.read_csv("isotherme_0_averaged_stats.csv", index_col=0)

print(iso_df.columns)
print(iso_df.head())

# Nettoyage des colonnes
iso_df.columns = iso_df.columns.str.strip()

# Construction du dictionnaire au même format que ton ancien code
isothermes = {}

for periode, row in iso_df.iterrows():
    isothermes[periode] = {
        "Isotherme 0° pour l'année la plus froide sur la période": row["min_elevation"],
        "Isotherme 0° moyen sur la période": row["mean_elevation"],
        "Isotherme 0° pour l'année la plus chaude sur la période": row["max_elevation"],
    }


# END NEW
colors = {"Isotherme 0° pour l'année la plus froide sur la période": "#2EA8FF", "Isotherme 0° moyen sur la période": "#8ACEFF", "Isotherme 0° pour l'année la plus chaude sur la période": "#B3DFFF"}

for periode, stats in isothermes.items():
    plt.figure(figsize=(30, 12))

    plt.fill_between(x, df['Altitude_Sommet'], color='#C2C2C2', alpha=0.5)

    # Tracer la crête (sommets reliés par une ligne)
    plt.plot(x, df['Altitude_Sommet'], color='grey', marker='', label='Sommet', linewidth=2)

    # Ajouter le nom des sommets
    for xi, yi, nom in zip(x, df['Altitude_Sommet'], df['Nom_Sommet']):
        plt.text(xi, yi + 80, nom, ha='center', va='bottom', fontsize=9) #, rotation=90)

    # Points pour préfectures et nom
    plt.scatter(x, df['Altitude_Préfécture'], color='darkgrey', marker='x', s=100, label='Préfecture')
    for xi, yi, nom in zip(x, df['Altitude_Préfécture'], df['Nom_prefecture']):
        plt.text(xi, yi + 80, nom, ha='center', va='bottom', fontsize=8)

    # Points pour stations de ski et relier basse et haute
    mask_stations = df['Nom_station de ski'] != ''
    #plt.scatter(x[mask_stations], df.loc[mask_stations, 'Altitude_basse_station de ski'],
                #color='#BDF4FF', marker='', s=100, label='Basse station de ski')
    #plt.scatter(x[mask_stations], df.loc[mask_stations, 'Altitude_haute_station de ski'],
                #color='#BDF4FF', marker='', s=100, label='Haute station de ski')

    # Relier basse et haute pour chaque station
    for xi, yb, yh in zip(x[mask_stations], df.loc[mask_stations, 'Altitude_basse_station de ski'],
                          df.loc[mask_stations, 'Altitude_haute_station de ski']):
        plt.plot([xi, xi], [yb, yh], color='#BDF4FF', linestyle='-', linewidth=8)

    plt.plot([], [], color='#BDF4FF', linestyle='-', linewidth=8,
                 label='Espace couvert par le domaine skiable')

    # Lignes min, mean, max pour cette période
    for key in [
        "Isotherme 0° pour l'année la plus froide sur la période",
        "Isotherme 0° moyen sur la période",
        "Isotherme 0° pour l'année la plus chaude sur la période"
    ]:
        linestyle = '-' if key == "Isotherme 0° moyen sur la période" else '--'

        plt.axhline(
            y=stats[key],
            color=colors[key],
            linestyle=linestyle,
            linewidth=4,
            label=f'{key} {periode}'
        )

    # Noms des départements en abscisse
    plt.xticks(x, df['Département'], rotation=45, ha='right')

    plt.ylabel("Altitude (m)")
    plt.title(f"Profil de crêtes avec altitudes de l'isotherme 0°C ({periode})")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # Sauvegarder l'image
    plt.savefig(f"crete_animations/profile_0C_{periode.replace('-', '_')}.png", dpi=300)
    plt.close()

# -----------------------------
# Animation à partir des images générées
# -----------------------------
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
import os

# Dossier où les images ont été sauvegardées
image_folder = "crete_animations"
images = [
    os.path.join(image_folder, "profile_0C_1990_2020.png"),
    os.path.join(image_folder, "profile_0C_2021_2040.png"),
    os.path.join(image_folder, "profile_0C_2041_2060.png"),
    os.path.join(image_folder, "profile_0C_2061_2080.png"),
    os.path.join(image_folder, "profile_0C_2081_2100.png")
]

# Création de la figure pour l'animation
fig, ax = plt.subplots(figsize=(30, 12))
img_display = ax.imshow(mpimg.imread(images[0]))
ax.axis('off')  # cacher axes

# Fonction d’animation
def update(frame):
    img_display.set_data(mpimg.imread(images[frame]))
    periode_label = images[frame].split("_")[-1].replace(".png", "").replace("_", "-")
    return img_display

# Créer l’animation
anim = FuncAnimation(fig, update, frames=len(images), blit=False)

# Sauvegarder la vidéo
output_video = os.path.join(image_folder, "crete_animation.mp4")
writer = FFMpegWriter(fps=1)
anim.save(output_video, writer=writer)
print(f"Vidéo créée : {output_video}")

# Sauvegarder le GIF
output_gif = os.path.join(image_folder, "crete_animation.gif")
gif_writer = PillowWriter(fps=1)
anim.save(output_gif, writer=gif_writer)
print(f"GIF créé : {output_gif}")
