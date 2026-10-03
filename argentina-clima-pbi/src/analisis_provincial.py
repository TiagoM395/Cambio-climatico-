"""
analisis_provincial.py
========================

Análisis provincial (proyecto.txt, secciones 16, 18, 19 y 29).

Ejecutar:
    python -m src.analisis_provincial
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

from src.analysis import estadistica_descriptiva, tendencia_temporal
from src.visualization import FIGURES_DIR, graficar_comparacion_provincias

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
TABLES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "tables"

FUENTE_TEMP = "NASA POWER (reanálisis MERRA-2, punto = capital provincial), 1981-2025"
FUENTE_PRECIP = "SMN / CIAM - Secretaría de Ambiente (estación representativa), 2010-2024"


def graficar_evolucion_por_provincia(df, columna_valor, titulo, etiqueta_y, fuente, nombre_archivo):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    jurisdicciones = sorted(df["jurisdiccion"].dropna().unique())
    cmap = plt.get_cmap("tab20", len(jurisdicciones))
    fig, ax = plt.subplots(figsize=(11, 7))
    for i, juris in enumerate(jurisdicciones):
        serie = df[df["jurisdiccion"] == juris][["año", columna_valor]].dropna()
        if serie.empty:
            continue
        ax.plot(serie["año"], serie[columna_valor], color=cmap(i), linewidth=1.2, label=juris)
    ax.set_title(titulo)
    ax.set_xlabel("Año")
    ax.set_ylabel(etiqueta_y)
    ax.legend(fontsize=6, ncol=2, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    ax.figure.text(0.01, 0.01, f"Fuente: {fuente}", fontsize=8, color="gray")
    fig.tight_layout()
    ruta = FIGURES_DIR / nombre_archivo
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return ruta


def calcular_tendencias_por_provincia(df, columna_valor) -> pd.DataFrame:
    filas = []
    for juris, grupo in df.groupby("jurisdiccion"):
        try:
            t = tendencia_temporal(grupo, "año", columna_valor)
            t["jurisdiccion"] = juris
            t["n_observaciones"] = grupo[columna_valor].notna().sum()
            filas.append(t)
        except ValueError:
            continue
    return pd.DataFrame(filas).set_index("jurisdiccion")


def calcular_estadistica_por_provincia(df, columna_valor) -> pd.DataFrame:
    filas = []
    for juris, grupo in df.groupby("jurisdiccion"):
        try:
            s = estadistica_descriptiva(grupo, columna_valor)
            s["jurisdiccion"] = juris
            filas.append(s)
        except ValueError:
            continue
    return pd.DataFrame(filas).set_index("jurisdiccion")


def main():
    df = pd.read_csv(PROCESSED_DIR / "dataset_provincial.csv")
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    print("Generando evolución de temperatura por provincia...")
    graficar_evolucion_por_provincia(
        df, "anomalia_temperatura",
        titulo="Anomalía de temperatura por provincia (base 1991-2020)",
        etiqueta_y="Anomalía de temperatura (°C)", fuente=FUENTE_TEMP,
        nombre_archivo="temperatura_provincias.png",
    )
    print("Generando evolución de precipitación por provincia...")
    graficar_evolucion_por_provincia(
        df, "precipitaciones_mm",
        titulo="Precipitación anual por provincia (estación representativa)",
        etiqueta_y="Precipitación (mm/año)", fuente=FUENTE_PRECIP,
        nombre_archivo="precipitaciones_provincias.png",
    )

    print("Calculando tendencias de temperatura por provincia...")
    tendencias_temp = calcular_tendencias_por_provincia(df, "anomalia_temperatura")
    tendencias_temp.to_csv(TABLES_DIR / "tendencias_temperatura_provincial.csv")

    print("Generando ranking descriptivo de tendencia de temperatura...")
    ranking_df = tendencias_temp.reset_index()[["jurisdiccion", "pendiente"]].rename(
        columns={"pendiente": "tendencia_temp_c_por_año"}
    )
    graficar_comparacion_provincias(
        ranking_df, "jurisdiccion", "tendencia_temp_c_por_año",
        titulo="Ranking descriptivo: tendencia de temperatura por provincia (°C/año)\n"
               "(orden estadístico, no implica 'mejor' o 'peor' provincia)",
        etiqueta_y="Pendiente de la tendencia (°C/año, 1981-2025)",
        fuente=FUENTE_TEMP, nombre_archivo="ranking_tendencia_temperatura_provincias.png",
    )

    est_temp = calcular_estadistica_por_provincia(df, "anomalia_temperatura")
    est_precip = calcular_estadistica_por_provincia(df, "precipitaciones_mm")
    est_temp.to_csv(TABLES_DIR / "estadistica_descriptiva_temperatura_provincial.csv")
    est_precip.to_csv(TABLES_DIR / "estadistica_descriptiva_precipitacion_provincial.csv")

    print("\nTop 5 provincias con mayor tendencia de aumento de temperatura:")
    print(tendencias_temp.sort_values("pendiente", ascending=False)[["pendiente", "p_valor", "n_observaciones"]].head(5).round(4))
    print("\nTop 5 provincias con menor tendencia:")
    print(tendencias_temp.sort_values("pendiente")[["pendiente", "p_valor", "n_observaciones"]].head(5).round(4))
    print("\nLIMITACIÓN: no se generan mapas en este script (ver src/mapas.py).")


if __name__ == "__main__":
    main()
