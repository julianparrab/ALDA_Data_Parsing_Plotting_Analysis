import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"

os.makedirs("plots", exist_ok=True)


def plot_categories(df: pd.DataFrame, columns: list, nrows: int, ncols: int, namefile: str):
    # Create figure
    fig, axes = plt.subplots(nrows, ncols, figsize=(18, 12))
    axes = axes.flatten()

    # Graph pie charts
    for i, column in enumerate(columns):
        value_counts = df[column].value_counts()
        axes[i].pie(value_counts, labels=value_counts.index, autopct="%1.1f%%", startangle=90)
        axes[i].set_title(f"{column} Distribution", fontsize=12)
        axes[i].axis("equal")

    plt.tight_layout()
    plt.savefig("plots/" + namefile)
    plt.clf()


def plot_vehicles_map(df: pd.DataFrame):

    if df.empty or 'city' not in df.columns:
        raise KeyError("DataFrame is empty or missing 'city' column")
    
    grouped = (
        df["city"].value_counts().reset_index().rename(columns={"vehicle_count": "city", "count": "vehicle_count"})
    )

    # print(grouped.head())

    coordenadas = {
        "Bogotá": {"lat": 4.7110, "lon": -74.0721},
        "Medellín": {"lat": 6.2442, "lon": -75.5812},
        "Cali": {"lat": 3.4516, "lon": -76.5320},
        "Barranquilla": {"lat": 10.9639, "lon": -74.7964},
        "Cartagena": {"lat": 10.3910, "lon": -75.4794},
        "Bucaramanga": {"lat": 7.1193, "lon": -73.1227},
        "Pereira": {"lat": 4.8140, "lon": -75.6989},
        "Santa Marta": {"lat": 11.2408, "lon": -74.1990},
        "Cúcuta": {"lat": 7.8932, "lon": -72.5078},
        "Ibagué": {"lat": 4.4389, "lon": -75.2234},
        "Villavicencio": {"lat": 4.1420, "lon": -73.6266},
        "Manizales": {"lat": 5.0703, "lon": -75.5135},
        "Pasto": {"lat": 1.2136, "lon": -77.2811},
        "Neiva": {"lat": 2.9345, "lon": -75.2809},
        "Armenia": {"lat": 4.5380, "lon": -75.6721},
        "Popayán": {"lat": 2.4448, "lon": -76.6147},
        "Valledupar": {"lat": 10.4631, "lon": -73.2532},
        "Montería": {"lat": 8.7500, "lon": -75.8833},
        "Sincelejo": {"lat": 9.3047, "lon": -75.3978},
        "Tunja": {"lat": 5.5353, "lon": -73.3677},
        "Riohacha": {"lat": 11.5444, "lon": -72.9072},
        "Quibdó": {"lat": 5.6956, "lon": -76.6498},
        "Arauca": {"lat": 7.0903, "lon": -70.7617},
        "Yopal": {"lat": 5.3378, "lon": -72.3958},
        "Mocoa": {"lat": 1.1472, "lon": -76.6469},
        "Mitú": {"lat": 1.1983, "lon": -70.1736},
        "Puerto Carreño": {"lat": 6.1846, "lon": -67.4932},
        "Leticia": {"lat": -4.2153, "lon": -69.9406},
        "Inírida": {"lat": 3.8683, "lon": -67.9239},
        "San Andrés": {"lat": 12.5847, "lon": -81.7006},
        "Florencia": {"lat": 1.6144, "lon": -75.6061},
    }

    # Añadir coordenadas al DataFrame
    grouped["lat"] = grouped["city"].map(lambda x: coordenadas.get(x, {}).get("lat", None))
    grouped["lon"] = grouped["city"].map(lambda x: coordenadas.get(x, {}).get("lon", None))

    # Eliminar filas sin coordenadas
    grouped = grouped.dropna(subset=['lat', 'lon'])

    # Crear el mapa
    fig = px.density_mapbox(
        grouped,
        lat="lat",
        lon="lon",
        z="vehicle_count",
        radius=20,
        zoom=5,
        center=dict(lat=4.5, lon=-74),
        mapbox_style="open-street-map",
        hover_name="city",
        title="Distribución de vehículos por ciudad y departamento",
    )

    fig.show()


def plot_accident_history(df: pd.DataFrame):
    df["accident_history"] = df["accident_history"].astype(str).str.lower().isin(["true"])

    # Estilo general
    sns.set(style="whitegrid")
    plt.figure(figsize=(15, 10))

    # === ACCIDENTES POR CIUDAD ===
    plt.subplot(3, 1, 1)
    city_accidents = df[df["accident_history"]].groupby("city").size().sort_values(ascending=False)
    sns.barplot(x=city_accidents.values, y=city_accidents.index, palette="Reds_r")
    plt.title("Distribución de accidentes por ciudad")
    plt.xlabel("Cantidad de accidentes")
    plt.ylabel("Ciudad")

    # === ACCIDENTES POR DEPARTAMENTO ===
    plt.subplot(3, 1, 2)
    dept_accidents = df[df["accident_history"]].groupby("department").size().sort_values(ascending=False)
    sns.barplot(x=dept_accidents.values, y=dept_accidents.index, palette="Oranges_r")
    plt.title("Distribución de accidentes por departamento")
    plt.xlabel("Cantidad de accidentes")
    plt.ylabel("Departamento")

    # === ACCIDENTES POR MARCA ===
    plt.subplot(3, 1, 3)
    brand_accidents = df[df["accident_history"]].groupby("brand").size().sort_values(ascending=False).head(10)
    sns.barplot(x=brand_accidents.values, y=brand_accidents.index, palette="Blues_r")
    plt.title("Top 10 marcas con más accidentes")
    plt.xlabel("Cantidad de accidentes")
    plt.ylabel("Marca")

    plt.tight_layout()
    plt.savefig("plots/accident_history.png")
    plt.clf()


def plot_status_vs_value(df: pd.DataFrame):
    sns.boxplot(data=df, x="vehicle_status", y="estimated_market_value")
    plt.title("Valor de Mercado Estimado vs Estado del Vehículo")
    plt.xlabel("Estado del Vehículo")
    plt.ylabel("Valor de Mercado Estimado")
    plt.tight_layout()
    plt.savefig("plots/status_vs_value.png")
    plt.clf()
