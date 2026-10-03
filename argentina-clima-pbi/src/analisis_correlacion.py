"""
analisis_correlacion.py
=========================

Relación clima-economía (proyecto.txt, sección 20). Nacional y
provincial siempre por separado; nunca implica causalidad (sección 21).

Ejecutar:
    python -m src.analisis_correlacion
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from src.analysis import correlacion_clima_economia
from src.visualization import FIGURES_DIR

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
TABLES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "tables"


def correlaciones_nacionales(df: pd.DataFrame) -> pd.DataFrame:
    pares = [
        ("anomalia_temperatura", "pbi_crecimiento_pct"),
        ("anomalia_precipitacion_pct", "pbi_crecimiento_pct"),
        ("emisiones_gei_co2eq", "pbi_crecimiento_pct"),
        ("anomalia_temperatura", "pib_per_capita_crecimiento_pct"),
        ("anomalia_precipitacion_pct", "pib_per_capita_crecimiento_pct"),
    ]
    filas = []
    for clima, econ in pares:
        for metodo in ("pearson", "spearman"):
            try:
                r = correlacion_clima_economia(df, clima, econ, metodo)
                r["variable_climatica"] = clima
                r["variable_economica"] = econ
                filas.append(r)
            except ValueError as e:
                print(f"AVISO: {metodo} {clima}-{econ}: {e}")
    return pd.DataFrame(filas)


def correlaciones_provinciales(df: pd.DataFrame, min_observaciones: int = 5) -> pd.DataFrame:
    filas = []
    for juris, grupo in df.groupby("jurisdiccion"):
        for clima in ("anomalia_temperatura", "precipitaciones_mm"):
            datos = grupo[[clima, "pbg"]].dropna()
            if len(datos) < min_observaciones:
                filas.append({
                    "jurisdiccion": juris, "variable_climatica": clima,
                    "metodo": "pearson", "coeficiente": None, "p_valor": None,
                    "n_observaciones": len(datos), "nota": "insuficientes observaciones",
                })
                continue
            for metodo in ("pearson", "spearman"):
                r = correlacion_clima_economia(grupo, clima, "pbg", metodo)
                r["jurisdiccion"] = juris
                r["variable_climatica"] = clima
                r["nota"] = ""
                filas.append(r)
    return pd.DataFrame(filas)


def graficar_dispersión_nacional(df, columna_x, columna_y, titulo, etiqueta_x, etiqueta_y, fuente, nombre_archivo):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    datos = df[[columna_x, columna_y]].dropna()
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.scatter(datos[columna_x], datos[columna_y], alpha=0.7)
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    ax.figure.text(0.01, 0.01, f"Fuente: {fuente}", fontsize=8, color="gray")
    fig.tight_layout()
    ruta = FIGURES_DIR / nombre_archivo
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def main():
    nacional = pd.read_csv(PROCESSED_DIR / "dataset_nacional.csv")
    provincial = pd.read_csv(PROCESSED_DIR / "dataset_provincial.csv")
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    print("Calculando correlaciones nacionales clima-economía...")
    corr_nac = correlaciones_nacionales(nacional)
    corr_nac.to_csv(TABLES_DIR / "correlaciones_nacional.csv", index=False)
    print(corr_nac.round(3).to_string(index=False))

    graficar_dispersión_nacional(
        nacional, "anomalia_temperatura", "pbi_crecimiento_pct",
        titulo="Anomalía de temperatura vs. crecimiento del PBI — Argentina",
        etiqueta_x="Anomalía de temperatura (°C)", etiqueta_y="Crecimiento del PBI (% anual)",
        fuente="CIAM/SMN + Banco Mundial",
        nombre_archivo="correlaciones_argentina_temp_pbi.png",
    )
    graficar_dispersión_nacional(
        nacional, "anomalia_precipitacion_pct", "pib_per_capita_crecimiento_pct",
        titulo="Anomalía de precipitación vs. crecimiento del PBI per cápita — Argentina",
        etiqueta_x="Anomalía de precipitación (%)", etiqueta_y="Crecimiento del PBI per cápita (% anual)",
        fuente="CIAM/SMN + Maddison Project Database (vía OWID)",
        nombre_archivo="correlaciones_argentina_precip_pbipercapita.png",
    )

    print("\nCalculando correlaciones provinciales clima-PBG...")
    corr_prov = correlaciones_provinciales(provincial)
    corr_prov.to_csv(TABLES_DIR / "correlaciones_provincial.csv", index=False)
    con_resultado = corr_prov[corr_prov["coeficiente"].notna()]
    print(f"  -> {con_resultado['jurisdiccion'].nunique()} provincias con correlación calculable")

    sig = corr_prov[(corr_prov["p_valor"].notna()) & (corr_prov["p_valor"] < 0.05)]
    print(f"\nCorrelaciones con p<0.05 (de {len(corr_prov[corr_prov['p_valor'].notna()])} pruebas, "
          f"sin corrección por comparaciones múltiples):")
    print(sig[["jurisdiccion", "variable_climatica", "metodo", "coeficiente", "p_valor"]].to_string(index=False))

    print("\nRECORDATORIO: asociación estadística, NO causalidad. No se mezcla nacional con provincial.")


if __name__ == "__main__":
    main()
