"""
mapas.py
=========

Mapas coropléticos (proyecto.txt, sección 16). Geometría: shapefile
oficial de provincias del IGN, en data/raw/geo_ign_provincias/.

Ejecutar:
    python -m src.mapas
"""

from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from src.construir_dataset import mapear_jurisdiccion

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
TABLES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "tables"
FIGURES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"

SHAPEFILE = RAW_DIR / "geo_ign_provincias" / "ign_provincia.shp"

# El polígono de Tierra del Fuego incluye el sector antártico reclamado
# por Argentina; se recorta solo el ENCUADRE visual (no el dato).
LIMITES_CONTINENTALES = {"xlim": (-75, -53), "ylim": (-56, -21)}


def cargar_geometria() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(SHAPEFILE)
    gdf["jurisdiccion"] = gdf["NAM"].apply(mapear_jurisdiccion)
    sin_mapear = gdf[gdf["jurisdiccion"].isna()]
    if not sin_mapear.empty:
        raise ValueError(f"Provincias del IGN sin mapear: {sin_mapear['NAM'].tolist()}")
    if gdf["jurisdiccion"].nunique() != 24:
        raise ValueError(f"Se esperaban 24 jurisdicciones, se mapearon {gdf['jurisdiccion'].nunique()}.")
    return gdf[["jurisdiccion", "geometry"]]


def graficar_mapa(gdf_con_valor, columna_valor, titulo, etiqueta_leyenda, fuente, nombre_archivo, cmap="viridis"):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.5, 9.5))
    gdf_con_valor.plot(
        column=columna_valor, ax=ax, legend=True, cmap=cmap, edgecolor="white", linewidth=0.4,
        missing_kwds={"color": "lightgrey", "label": "Sin datos"},
        legend_kwds={"label": etiqueta_leyenda, "shrink": 0.5},
    )
    ax.set_xlim(*LIMITES_CONTINENTALES["xlim"])
    ax.set_ylim(*LIMITES_CONTINENTALES["ylim"])
    ax.set_title(titulo, fontsize=12)
    ax.set_axis_off()
    ax.figure.text(0.02, 0.02, f"Fuente: {fuente} | Encuadre recortado al territorio continental + Tierra del Fuego",
                    fontsize=6.5, color="gray")
    fig.tight_layout()
    ruta = FIGURES_DIR / nombre_archivo
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    print(f"OK  {ruta}")
    return ruta


def main():
    print("Cargando geometría oficial IGN...")
    geometria = cargar_geometria()
    print(f"  -> {len(geometria)} jurisdicciones mapeadas correctamente")

    df_provincial = pd.read_csv(PROCESSED_DIR / "dataset_provincial.csv")
    tendencias = pd.read_csv(TABLES_DIR / "tendencias_temperatura_provincial.csv")

    gdf_tendencia = geometria.merge(tendencias[["jurisdiccion", "pendiente"]], on="jurisdiccion", how="left")
    graficar_mapa(gdf_tendencia, "pendiente",
                  titulo="Tendencia de temperatura por provincia (1981-2025)\nMapa descriptivo",
                  etiqueta_leyenda="Pendiente (°C/año)", fuente="NASA POWER + geometría IGN",
                  nombre_archivo="mapa_temperatura.png", cmap="Reds")

    ultima_decada = df_provincial[df_provincial["año"] >= 2016]
    anomalia_reciente = ultima_decada.groupby("jurisdiccion")["anomalia_temperatura"].mean().reset_index()
    anomalia_reciente.columns = ["jurisdiccion", "anomalia_media_2016_2025"]
    gdf_anomalia = geometria.merge(anomalia_reciente, on="jurisdiccion", how="left")
    graficar_mapa(gdf_anomalia, "anomalia_media_2016_2025",
                  titulo="Anomalía de temperatura promedio por provincia (2016-2025)\nBase: 1991-2020",
                  etiqueta_leyenda="Anomalía media (°C)", fuente="NASA POWER + geometría IGN",
                  nombre_archivo="mapa_anomalia_termica.png", cmap="OrRd")

    precip_media = df_provincial.groupby("jurisdiccion")["precipitaciones_mm"].mean().reset_index()
    gdf_precip = geometria.merge(precip_media, on="jurisdiccion", how="left")
    graficar_mapa(gdf_precip, "precipitaciones_mm",
                  titulo="Precipitación media anual por provincia (2010-2024)\nEstación representativa",
                  etiqueta_leyenda="Precipitación media (mm/año)", fuente="SMN/CIAM + geometría IGN",
                  nombre_archivo="mapa_precipitaciones.png", cmap="Blues")

    print("\nMapas descriptivos: no implican juicio de valor sobre ninguna provincia.")


if __name__ == "__main__":
    main()
