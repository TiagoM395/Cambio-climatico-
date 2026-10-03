"""
analisis_clima_economia_provincial.py
========================================

Cruce provincia por provincia entre la tendencia de precipitación y el
crecimiento económico (PBG), para responder: ¿qué provincias pierden más
lluvia, y cómo les fue económicamente en ese mismo período?

Diferencia con analisis_correlacion.py: ese script corre 96 pruebas DENTRO
de cada provincia, con apenas ~13-15 años de datos cada una (por eso casi
ninguna da significativa: muy poco poder estadístico). Acá se corre UNA
sola prueba, con 24 provincias como observaciones (una fila por provincia):
tendencia de lluvia por década vs. crecimiento del PBG en el período con
dato. Sigue siendo asociación estadística, nunca causalidad (proyecto.txt,
sección 21), pero es la pregunta correcta para comparar provincias entre sí.

Ejecutar:
    python -m src.analisis_clima_economia_provincial
"""

from pathlib import Path
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

from src.visualization import FIGURES_DIR

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
TABLES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "tables"


def crecimiento_pbg_por_provincia(df: pd.DataFrame) -> pd.DataFrame:
    """Tasa de crecimiento anual compuesta (CAGR) del PBG de cada provincia,
    entre el primer y el último año con dato disponible."""
    filas = []
    for juris, grupo in df.groupby("jurisdiccion"):
        datos = grupo[["año", "pbg"]].dropna().sort_values("año")
        if len(datos) < 2:
            continue
        primero, ultimo = datos.iloc[0], datos.iloc[-1]
        n_años = ultimo["año"] - primero["año"]
        if n_años <= 0 or primero["pbg"] <= 0:
            continue
        cagr = ((ultimo["pbg"] / primero["pbg"]) ** (1 / n_años) - 1) * 100
        filas.append({
            "jurisdiccion": juris,
            "pbg_año_inicio": int(primero["año"]), "pbg_inicio": primero["pbg"],
            "pbg_año_fin": int(ultimo["año"]), "pbg_fin": ultimo["pbg"],
            "pbg_crecimiento_anual_pct": cagr,
            "pbg_n_años": len(datos),
        })
    return pd.DataFrame(filas)


def construir_ranking(tendencia: pd.DataFrame, crecimiento: pd.DataFrame) -> pd.DataFrame:
    ranking = tendencia.merge(crecimiento, on="jurisdiccion", how="inner")
    columnas = [
        "jurisdiccion",
        "tendencia_precipitacion_por_decada", "precipitacion_p_valor",
        "pbg_crecimiento_anual_pct", "pbg_año_inicio", "pbg_año_fin", "pbg_n_años",
    ]
    return ranking[columnas].sort_values("tendencia_precipitacion_por_decada").reset_index(drop=True)


def correlacion_cruzada(ranking: pd.DataFrame) -> dict:
    """Una sola prueba, n=24 provincias: tendencia de lluvia vs. crecimiento del PBG."""
    datos = ranking[["tendencia_precipitacion_por_decada", "pbg_crecimiento_anual_pct"]].dropna()
    r_p, p_p = stats.pearsonr(datos["tendencia_precipitacion_por_decada"], datos["pbg_crecimiento_anual_pct"])
    r_s, p_s = stats.spearmanr(datos["tendencia_precipitacion_por_decada"], datos["pbg_crecimiento_anual_pct"])
    return {"n_provincias": len(datos), "pearson_r": r_p, "pearson_p": p_p, "spearman_r": r_s, "spearman_p": p_s}


def graficar_dispersion(ranking: pd.DataFrame, ruta: Path) -> None:
    datos = ranking.dropna(subset=["tendencia_precipitacion_por_decada", "pbg_crecimiento_anual_pct"])
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(datos["tendencia_precipitacion_por_decada"], datos["pbg_crecimiento_anual_pct"],
               s=70, alpha=0.75, color="#2b6cb0", edgecolor="white", linewidth=0.5)
    for _, fila in datos.iterrows():
        ax.annotate(fila["jurisdiccion"],
                    (fila["tendencia_precipitacion_por_decada"], fila["pbg_crecimiento_anual_pct"]),
                    fontsize=8, xytext=(5, 3), textcoords="offset points")
    if len(datos) >= 3:
        recta = stats.linregress(datos["tendencia_precipitacion_por_decada"], datos["pbg_crecimiento_anual_pct"])
        xs = [datos["tendencia_precipitacion_por_decada"].min(), datos["tendencia_precipitacion_por_decada"].max()]
        ax.plot(xs, [recta.slope * x + recta.intercept for x in xs], "r--", linewidth=1, label="Línea de tendencia")
        ax.legend()
    ax.axvline(0, color="gray", linewidth=0.8, linestyle=":")
    ax.set_xlabel("Tendencia de precipitación (mm por década) — negativo = cada vez llueve menos")
    ax.set_ylabel("Crecimiento anual compuesto del PBG (%), período con dato")
    ax.set_title("¿Las provincias donde más baja la lluvia son las que menos crecen?")
    ax.figure.text(0.01, 0.01,
                    "Fuente: provincias_tendencia.csv + dataset_provincial.csv (elaboración propia). "
                    "Asociación estadística, no causalidad.", fontsize=7, color="gray")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def main():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    provincial = pd.read_csv(PROCESSED_DIR / "dataset_provincial.csv")
    tendencia = pd.read_csv(PROCESSED_DIR / "provincias_tendencia.csv")

    crecimiento = crecimiento_pbg_por_provincia(provincial)
    ranking = construir_ranking(tendencia, crecimiento)
    ranking.to_csv(TABLES_DIR / "ranking_precipitacion_crecimiento_pbg_provincial.csv", index=False)

    print(f"Ranking: {len(ranking)} provincias con tendencia de lluvia y crecimiento de PBG.")
    print(ranking.round(2).to_string(index=False))

    cruce = correlacion_cruzada(ranking)
    pd.DataFrame([cruce]).to_csv(TABLES_DIR / "correlacion_precipitacion_crecimiento_pbg_provincial.csv", index=False)
    print("\nCorrelación cruzada entre provincias (n=24; distinta de las 96 pruebas dentro de cada provincia):")
    print(cruce)

    graficar_dispersion(ranking, FIGURES_DIR / "precipitacion_vs_crecimiento_pbg_provincial.png")
    print(f"\nGráfico guardado en {FIGURES_DIR / 'precipitacion_vs_crecimiento_pbg_provincial.png'}")

    print("\nRECORDATORIO: asociación estadística, NO causalidad.")


if __name__ == "__main__":
    main()
