"""
analisis_sequia_economia.py
==============================

¿En los años de sequía, la economía creció menos? En vez de mirar la
lluvia como un número continuo (mm o su tendencia), acá se define
directamente "año seco" / "año normal" y se comparan los dos grupos — la
forma más directa de contestar la pregunta, en vez de leer un coeficiente
de correlación. Sigue siendo asociación, no causalidad (proyecto.txt,
sección 21).

Nivel nacional: año seco = anomalía de precipitación nacional en el 25%
más bajo de toda la serie 1961-2025. Se compara contra el crecimiento del
PBI y del PBI per cápita.

Nivel provincial: "seco" se define con la PROPIA distribución histórica de
cada provincia (25% más bajo de SU serie de lluvia, 1981-2025) — no un
umbral en mm igual para todas, porque lo que es seco en Misiones es
normal en Santa Cruz. Como cada provincia por separado tiene muy pocos
años con PBG (13-15), se agrupan las 24 provincias en un solo análisis
(panel), comparando el crecimiento de cada provincia contra su PROPIO
promedio histórico — para no confundir "provincia seca" con "provincia
pobre" (eso ya se descartó en analisis_clima_economia_provincial.py).

Ejecutar:
    python -m src.analisis_sequia_economia
"""

from pathlib import Path
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

from src.modelo_provincial import calcular_crecimiento_pbg
from src.visualization import FIGURES_DIR

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
TABLES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "tables"

PERCENTIL_SEQUIA = 25


def analisis_nacional():
    df = pd.read_csv(PROCESSED_DIR / "dataset_nacional.csv")
    umbral = df["anomalia_precipitacion_pct"].quantile(PERCENTIL_SEQUIA / 100)
    df["año_seco"] = df["anomalia_precipitacion_pct"] <= umbral

    resultados = {}
    for variable_economica in ["pbi_crecimiento_pct", "pib_per_capita_crecimiento_pct"]:
        datos = df.dropna(subset=["año_seco", variable_economica])
        secos = datos[datos["año_seco"]][variable_economica]
        normales = datos[~datos["año_seco"]][variable_economica]
        t, p = stats.ttest_ind(secos, normales, equal_var=False)
        resultados[variable_economica] = {
            "umbral_anomalia_precipitacion_pct": umbral,
            "n_años_secos": len(secos), "n_años_normales": len(normales),
            "media_crecimiento_secos": secos.mean(), "media_crecimiento_normales": normales.mean(),
            "diferencia": secos.mean() - normales.mean(),
            "t_valor": t, "p_valor": p,
        }
    columnas = ["año", "anomalia_precipitacion_pct", "año_seco",
                "pbi_crecimiento_pct", "pib_per_capita_crecimiento_pct"]
    return resultados, df[columnas]


def analisis_provincial():
    clima = pd.read_csv(PROCESSED_DIR / "provincias_clima_anual.csv")
    umbrales = clima.groupby("jurisdiccion")["precipitacion_mm"].quantile(PERCENTIL_SEQUIA / 100)
    clima["umbral_provincia"] = clima["jurisdiccion"].map(umbrales)
    clima["año_seco"] = clima["precipitacion_mm"] <= clima["umbral_provincia"]

    provincial = pd.read_csv(PROCESSED_DIR / "dataset_provincial.csv")
    provincial = calcular_crecimiento_pbg(provincial)

    panel = clima[["jurisdiccion", "año", "año_seco", "precipitacion_mm"]].merge(
        provincial[["jurisdiccion", "año", "pbg_crecimiento_pct"]],
        on=["jurisdiccion", "año"], how="inner",
    ).dropna(subset=["pbg_crecimiento_pct"])

    promedio_provincia = panel.groupby("jurisdiccion")["pbg_crecimiento_pct"].transform("mean")
    panel["crecimiento_relativo_a_su_promedio"] = panel["pbg_crecimiento_pct"] - promedio_provincia

    secos = panel[panel["año_seco"]]["crecimiento_relativo_a_su_promedio"]
    normales = panel[~panel["año_seco"]]["crecimiento_relativo_a_su_promedio"]
    t, p = stats.ttest_ind(secos, normales, equal_var=False)
    resultado = {
        "n_provincias": panel["jurisdiccion"].nunique(),
        "n_provincia_años_secos": len(secos), "n_provincia_años_normales": len(normales),
        "media_relativa_secos": secos.mean(), "media_relativa_normales": normales.mean(),
        "diferencia": secos.mean() - normales.mean(),
        "t_valor": t, "p_valor": p,
    }
    return panel, resultado


def graficar_comparacion_nacional(df: pd.DataFrame, ruta: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    variables = [
        ("pbi_crecimiento_pct", "Crecimiento del PBI (%)"),
        ("pib_per_capita_crecimiento_pct", "Crecimiento del PBI per cápita (%)"),
    ]
    for ax, (variable, etiqueta) in zip(axes, variables):
        datos = df.dropna(subset=["año_seco", variable])
        grupos = [datos[~datos["año_seco"]][variable], datos[datos["año_seco"]][variable]]
        ax.boxplot(grupos, tick_labels=["Años normales", "Años secos"])
        ax.set_ylabel(etiqueta)
        ax.axhline(0, color="gray", linewidth=0.8, linestyle=":")
    fig.suptitle("Argentina: crecimiento económico en años secos vs. normales")
    fig.text(0.01, 0.01,
              "Año seco = anomalía de precipitación en el 25% más bajo de la serie 1961-2025. "
              "Fuente: CIAM/SMN + Banco Mundial + Maddison Project (vía OWID).",
              fontsize=7, color="gray")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def graficar_comparacion_provincial(panel: pd.DataFrame, ruta: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))
    grupos = [panel[~panel["año_seco"]]["crecimiento_relativo_a_su_promedio"],
              panel[panel["año_seco"]]["crecimiento_relativo_a_su_promedio"]]
    ax.boxplot(grupos, tick_labels=["Años normales", "Años secos"])
    ax.set_ylabel("Crecimiento del PBG vs. promedio de esa provincia (p.p.)")
    ax.axhline(0, color="gray", linewidth=0.8, linestyle=":")
    ax.set_title("Las 24 provincias juntas: ¿crecen menos en sus propios años secos?")
    fig.text(0.02, 0.025,
              "Año seco = precipitación en el 25% más bajo de la historia de ESA provincia (1981-2025).\n"
              "Cada provincia comparada contra su propio promedio, no contra las demás.",
              fontsize=7, color="gray")
    fig.tight_layout(rect=(0.02, 0.1, 1, 1))
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def main():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Nacional: años secos vs. normales ===")
    resultados_nac, df_nac = analisis_nacional()
    for variable, r in resultados_nac.items():
        print(f"\n{variable}:")
        for k, v in r.items():
            print(f"  {k}: {v:.3f}" if isinstance(v, float) else f"  {k}: {v}")
    pd.DataFrame(resultados_nac).T.to_csv(TABLES_DIR / "sequia_vs_crecimiento_nacional.csv")
    graficar_comparacion_nacional(df_nac, FIGURES_DIR / "sequia_vs_crecimiento_nacional.png")

    print("\n=== Provincial (panel, 24 provincias): años secos vs. normales ===")
    panel, resultado_prov = analisis_provincial()
    for k, v in resultado_prov.items():
        print(f"  {k}: {v:.3f}" if isinstance(v, float) else f"  {k}: {v}")
    pd.DataFrame([resultado_prov]).to_csv(TABLES_DIR / "sequia_vs_crecimiento_provincial.csv", index=False)
    panel.to_csv(TABLES_DIR / "sequia_panel_provincial.csv", index=False)
    graficar_comparacion_provincial(panel, FIGURES_DIR / "sequia_vs_crecimiento_provincial.png")

    print("\nRECORDATORIO: asociación estadística, NO causalidad.")


if __name__ == "__main__":
    main()
