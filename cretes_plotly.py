import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

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
    fig = go.Figure()

    # Remplissage sous la crête
    fig.add_trace(go.Scatter(
        x=x,
        y=df['Altitude_Sommet'],
        fill='tozeroy',
        fillcolor='#C2C2C2',
        line=dict(color='#C2C2C2', width=2),
        mode='lines+text',
        name='Sommet',
        text=df['Nom_Sommet'],
        textposition='top center'
    ))

    # Préfectures
    fig.add_trace(go.Scatter(
        x=x,
        y=df['Altitude_Préfécture'],
        mode='markers+text',
        marker=dict(symbol='x', color='darkgrey', size=10),
        name='Préfecture',
        text=df['Nom_prefecture'],
        textposition='top center'
    ))

    # Stations de ski
    mask_stations = df['Nom_station de ski'] != ''

    # Relier basse et haute
    added_legend = False  # flag pour ajouter la légende une seule fois

    for xi, yb, yh in zip(x[mask_stations], df.loc[mask_stations, 'Altitude_basse_station de ski'],
                          df.loc[mask_stations, 'Altitude_haute_station de ski']):
        fig.add_trace(go.Scatter(
            x=[xi, xi],
            y=[yb, yh],
            mode='lines',
            line=dict(color='#BDF4FF', width=8),
            name='Espace couvert par le domaine skiable' if not added_legend else None,
            showlegend=not added_legend
        ))
        added_legend = True  # après le premier ajout, on ne met plus dans la légende

    for key in ["Isotherme 0° pour l'année la plus froide sur la période",
                "Isotherme 0° moyen sur la période",
                "Isotherme 0° pour l'année la plus chaude sur la période"]:

        # Définir le style du trait
        if key == "Isotherme 0° moyen sur la période":
            dash_style = 'solid'  # trait continu pour la moyenne
        else:
            dash_style = 'dash'  # pointillé pour min et max

        fig.add_trace(go.Scatter(
            x=[x[0], x[-1]],
            y=[stats[key], stats[key]],
            mode='lines',
            line=dict(color=colors[key], width=2, dash=dash_style),
            name=f'{key} {periode}'
        ))

    fig.update_layout(
        title=f"Profil de crêtes avec altitudes de l'isotherme 0°C ({periode})",
        xaxis=dict(tickmode='array', tickvals=x, ticktext=df['Département'], tickangle=45),
        yaxis_title="Altitude (m)",
        width=3000,
        height=1200
    )

    # Sauvegarder en HTML
    os.makedirs("crete_animations_plotly", exist_ok=True)
    fig.write_html(f"crete_animations_plotly/profile_0C_{periode.replace('-', '_')}.html")


