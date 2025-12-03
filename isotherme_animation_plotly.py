import xarray as xr
import numpy as np
import glob
import os
import plotly.graph_objects as go

# -----------------------------
# Charger tous les fichiers
# -----------------------------
data_folder = 'Isotherme0_data'
input_pattern = os.path.join(data_folder, 'freezing_days_per_year_*.nc')
input_files = sorted(glob.glob(input_pattern))

datasets = [xr.open_dataset(f) for f in input_files]
combined = xr.concat(datasets, dim='year')

# Convertir freezing_days en nombre de jours
freezing_days_in_days = combined['freezing_days'] / np.timedelta64(1, 'D')

# Coordonnées
x = combined['x'].values.astype(float)
y = combined['y'].values.astype(float)
if np.issubdtype(combined['year'].dtype, np.datetime64):
    years = combined['year'].dt.year.values
else:
    years = combined['year'].values

# Définir limites couleurs
vmin = np.nanmin(freezing_days_in_days.values)
vmax = np.nanmax(freezing_days_in_days.values)

# -----------------------------
# Animation par année
# -----------------------------
frames_years = []
for i, year in enumerate(years):
    frames_years.append(go.Frame(
        data=[go.Heatmap(
            z=freezing_days_in_days[i, :, :].values,
            x=x,
            y=y,
            zmin=vmin,
            zmax=vmax,
            colorscale='Blues',
            colorbar=dict(title='Jours de gel')
        )],
        name=str(year)
    ))

fig_years = go.Figure(
    data=[go.Heatmap(
        z=freezing_days_in_days[0, :, :].values,
        x=x,
        y=y,
        zmin=vmin,
        zmax=vmax,
        colorscale='Blues',
        colorbar=dict(title='Jours de gel')
    )],
    frames=frames_years
)

sliders_years = [dict(
    steps=[dict(method='animate',
                args=[[str(year)], dict(mode='immediate', frame=dict(duration=200, redraw=True), transition=dict(duration=0))],
                label=str(year)) for year in years],
    transition=dict(duration=0),
    x=0, y=0, currentvalue=dict(prefix="Année: ", font=dict(size=16)),
    len=1.0
)]

fig_years.update_layout(
    title='Jours de gel - Évolution par année',
    xaxis_title='x',
    yaxis_title='y',
    width=800,
    height=600,
    sliders=sliders_years,
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        y=1.05,
        x=1.05,
        xanchor='right',
        yanchor='top',
        buttons=[
            dict(label='Play', method='animate',
                 args=[None, dict(frame=dict(duration=200, redraw=True),
                                  transition=dict(duration=0),
                                  fromcurrent=True,
                                  mode='immediate')]),
            dict(label='Pause', method='animate',
                 args=[[None], dict(frame=dict(duration=0, redraw=False),
                                    mode='immediate')])
        ]
    )]
)

os.makedirs("isotherme_animations_plotly", exist_ok=True)
fig_years.write_html("isotherme_animations_plotly/freezing_days_years_animation.html")

# -----------------------------
# Animation par intervalles
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
    mean_slice = freezing_days_in_days[mask, :, :].mean(dim='year')
    mean_slices.append(mean_slice)
    interval_labels.append(f"{start}-{end}")

mean_slices = xr.concat(mean_slices, dim='interval')

frames_intervals = []
for i, label in enumerate(interval_labels):
    frames_intervals.append(go.Frame(
        data=[go.Heatmap(
            z=mean_slices[i, :, :].values,
            x=x,
            y=y,
            zmin=vmin,
            zmax=vmax,
            colorscale='Blues',
            colorbar=dict(title='Jours de gel')
        )],
        name=label
    ))

fig_intervals = go.Figure(
    data=[go.Heatmap(
        z=mean_slices[0, :, :].values,
        x=x,
        y=y,
        zmin=vmin,
        zmax=vmax,
        colorscale='Blues',
        colorbar=dict(title='Jours de gel')
    )],
    frames=frames_intervals
)

sliders_intervals = [dict(
    steps=[dict(method='animate',
                args=[[label], dict(mode='immediate', frame=dict(duration=1000, redraw=True), transition=dict(duration=0))],
                label=label) for label in interval_labels],
    transition=dict(duration=0),
    x=0, y=0, currentvalue=dict(prefix="Intervalle: ", font=dict(size=16)),
    len=1.0
)]

fig_intervals.update_layout(
    title='Jours de gel - Moyenne par intervalle',
    xaxis_title='x',
    yaxis_title='y',
    width=800,
    height=600,
    sliders=sliders_intervals,
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        y=1.05,
        x=1.05,
        xanchor='right',
        yanchor='top',
        buttons=[
            dict(label='Play', method='animate',
                 args=[None, dict(frame=dict(duration=1000, redraw=True),
                                  transition=dict(duration=0),
                                  fromcurrent=True,
                                  mode='immediate')]),
            dict(label='Pause', method='animate',
                 args=[[None], dict(frame=dict(duration=0, redraw=False),
                                    mode='immediate')])
        ]
    )]
)

fig_intervals.write_html("isotherme_animations_plotly/freezing_days_intervals_animation.html")
