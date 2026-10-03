"""
analisis_nacional.py
======================

Análisis exploratorio nacional (proyecto.txt, sección 15).

Ejecutar:
    python -m src.analisis_nacional
"""

from pathlib import Path
import pandas as pd

from src.visualization import graficar_serie_temporal, graficar_normalizado
from src.analysis import estadistica_descriptiva, tendencia_temporal

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
TABLES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "tables"

FUENTE_TEMP = "Secretaría de Ambiente (CIAM) / SMN, 1961-2025"
FUENTE_GEI = "Inventario Nacional de GEI, Secretaría de Ambiente, 2010-2022"
FUENTE_PBI = "Banco Mundial, GDP growth (annual %), 1961-2025"


def generar_graficos(df: pd.DataFrame):
    graficar_serie_temporal(
        df, "año", "anomalia_temperatura",
        titulo="Anomalía de temperatura media anual en Argentina (1961-2025)",
        etiqueta_y="Anomalía de temperatura (°C, base 1991-2020)",
        fuente=FUENTE_TEMP, nombre_archivo="temperatura_argentina.png",
    )
    graficar_serie_temporal(
        df, "año", "anomalia_precipitacion_pct",
        titulo="Anomalía de precipitación anual en Argentina (1961-2025)",
        etiqueta_y="Anomalía de precipitación (% respecto de la media de referencia)",
        fuente=FUENTE_TEMP, nombre_archivo="precipitaciones_argentina.png",
    )
    graficar_serie_temporal(
        df, "año", "emisiones_gei_co2eq",
        titulo="Emisiones de gases de efecto invernadero en Argentina (2010-2022)",
        etiqueta_y="Emisiones de GEI (millones de toneladas de CO2 equivalente)",
        fuente=FUENTE_GEI, nombre_archivo="co2_argentina.png",
    )
    graficar_serie_temporal(
        df, "año", "pbi_crecimiento_pct",
        titulo="Crecimiento real anual del PBI de Argentina (1961-2025)",
        etiqueta_y="Crecimiento del PBI (% anual)",
        fuente=FUENTE_PBI, nombre_archivo="pbi_argentina.png",
    )
    graficar_normalizado(
        df, "año",
        {
            "anomalia_temperatura": "Anomalía de temperatura",
            "anomalia_precipitacion_pct": "Anomalía de precipitación",
            "emisiones_gei_co2eq": "Emisiones de GEI",
            "pbi_crecimiento_pct": "Crecimiento del PBI",
        },
        titulo="Comparación de tendencias normalizadas — Argentina",
        fuente=f"{FUENTE_TEMP}; {FUENTE_GEI}; {FUENTE_PBI}",
        nombre_archivo="correlaciones_argentina.png",
    )
    print("Gráficos guardados en outputs/figures/")


def generar_estadistica_descriptiva(df: pd.DataFrame) -> pd.DataFrame:
    variables = ["anomalia_temperatura", "anomalia_precipitacion_pct",
                 "emisiones_gei_co2eq", "pbi_crecimiento_pct"]
    filas = []
    for var in variables:
        stats = estadistica_descriptiva(df, var)
        stats["variable"] = var
        filas.append(stats)
    resultado = pd.DataFrame(filas).set_index("variable")
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(TABLES_DIR / "estadistica_descriptiva_nacional.csv")
    return resultado


def generar_tendencias(df: pd.DataFrame) -> pd.DataFrame:
    variables = ["anomalia_temperatura", "anomalia_precipitacion_pct",
                 "emisiones_gei_co2eq", "pbi_crecimiento_pct"]
    filas = []
    for var in variables:
        try:
            t = tendencia_temporal(df, "año", var)
            t["variable"] = var
            filas.append(t)
        except ValueError as e:
            print(f"AVISO: no se pudo estimar tendencia para {var}: {e}")
    resultado = pd.DataFrame(filas).set_index("variable")
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(TABLES_DIR / "tendencias_nacional.csv")
    return resultado


def main():
    df = pd.read_csv(PROCESSED_DIR / "dataset_nacional.csv")
    print("Generando gráficos nacionales...")
    generar_graficos(df)
    print("\nEstadística descriptiva nacional:")
    print(generar_estadistica_descriptiva(df).round(3).to_string())
    print("\nTendencias temporales nacionales:")
    print(generar_tendencias(df).round(4).to_string())
    print("\nNota: la pendiente describe una tendencia estadística, no una relación causal.")


if __name__ == "__main__":
    main()
