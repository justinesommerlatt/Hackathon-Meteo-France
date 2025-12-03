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

# Isothermes 0°C pour les 4 périodes avec min, mean et max
isothermes = {
    "2020-2040": {"Isotherme 0° pour l'année la plus froide sur la période": 1347.0, "Isotherme 0° moyen sur la période": 2039.4, "Isotherme 0° pour l'année la plus chaude sur la période": 2617.0},
    "2041-2060": {"Isotherme 0° pour l'année la plus froide sur la période": 1675.0, "Isotherme 0° moyen sur la période": 2231.5, "Isotherme 0° pour l'année la plus chaude sur la période": 2750.0},
    "2061-2080": {"Isotherme 0° pour l'année la plus froide sur la période": 1742.0, "Isotherme 0° moyen sur la période": 2339.5, "Isotherme 0° pour l'année la plus chaude sur la période": 2793.0},
    "2081-2100": {"Isotherme 0° pour l'année la plus froide sur la période": 2126.0, "Isotherme 0° moyen sur la période": 2565.5, "Isotherme 0° pour l'année la plus chaude sur la période": 2999.0}
}

colors = {"Isotherme 0° pour l'année la plus froide sur la période": "blue",
          "Isotherme 0° moyen sur la période": "orange",
          "Isotherme 0° pour l'année la plus chaude sur la période": "red"}

for periode, stats in isothermes.items():
    fig = go.Figure()

    # Remplissage sous la crête
    fig.add_trace(go.Scatter(
        x=x,
        y=df['Altitude_Sommet'],
        fill='tozeroy',
        fillcolor='lightgrey',
        line=dict(color='grey', width=2),
        mode='lines+markers+text',
        marker=dict(size=8),
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
    # Basse station
    fig.add_trace(go.Scatter(
        x=x[mask_stations],
        y=df.loc[mask_stations, 'Altitude_basse_station de ski'],
        mode='markers',
        marker=dict(color='cyan', size=10),
        name='Basse station de ski'
    ))
    # Haute station
    fig.add_trace(go.Scatter(
        x=x[mask_stations],
        y=df.loc[mask_stations, 'Altitude_haute_station de ski'],
        mode='markers',
        marker=dict(color='cyan', size=10),
        name='Haute station de ski'
    ))
    # Relier basse et haute
    for xi, yb, yh in zip(x[mask_stations], df.loc[mask_stations, 'Altitude_basse_station de ski'], df.loc[mask_stations, 'Altitude_haute_station de ski']):
        fig.add_trace(go.Scatter(
            x=[xi, xi],
            y=[yb, yh],
            mode='lines',
            line=dict(color='cyan', width=3),
            showlegend=False
        ))

    # Lignes min, mean, max
    for key in ["Isotherme 0° pour l'année la plus froide sur la période", "Isotherme 0° moyen sur la période", "Isotherme 0° pour l'année la plus chaude sur la période"]:
        fig.add_trace(go.Scatter(
            x=[x[0], x[-1]],
            y=[stats[key], stats[key]],
            mode='lines',
            line=dict(color=colors[key], width=2),
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


