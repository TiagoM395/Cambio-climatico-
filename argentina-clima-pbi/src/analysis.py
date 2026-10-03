"""
analysis.py
============

Estadística descriptiva, tendencias temporales y análisis de correlación
clima-economía (ver proyecto.txt, secciones 18, 19, 20 y 21).
"""

import pandas as pd
from scipy import stats


def estadistica_descriptiva(df: pd.DataFrame, columna: str) -> dict:
    """Calcula media, mediana, desvío estándar, mín, máx, percentiles y CV."""
    serie = df[columna].dropna()
    if serie.empty:
        raise ValueError(f"No hay datos válidos en la columna '{columna}'.")
    media = serie.mean()
    return {
        "media": media,
        "mediana": serie.median(),
        "desvio_estandar": serie.std(),
        "minimo": serie.min(),
        "maximo": serie.max(),
        "rango": serie.max() - serie.min(),
        "percentil_25": serie.quantile(0.25),
        "percentil_75": serie.quantile(0.75),
        "coeficiente_variacion": (serie.std() / media) if media != 0 else None,
    }


def tendencia_temporal(df: pd.DataFrame, columna_anio: str, columna_valor: str) -> dict:
    """Estima la tendencia temporal mediante regresión lineal simple. No implica causalidad."""
    datos = df[[columna_anio, columna_valor]].dropna()
    if len(datos) < 3:
        raise ValueError("Se requieren al menos 3 observaciones para estimar una tendencia.")
    resultado = stats.linregress(datos[columna_anio], datos[columna_valor])
    return {
        "pendiente": resultado.slope,
        "intercepto": resultado.intercept,
        "r_valor": resultado.rvalue,
        "r_cuadrado": resultado.rvalue ** 2,
        "p_valor": resultado.pvalue,
        "error_estandar": resultado.stderr,
    }


def correlacion_clima_economia(
    df: pd.DataFrame, columna_clima: str, columna_economia: str, metodo: str = "pearson"
) -> dict:
    """Correlación Pearson o Spearman. Describe asociación, nunca causalidad."""
    datos = df[[columna_clima, columna_economia]].dropna()
    if len(datos) < 3:
        raise ValueError("Se requieren al menos 3 observaciones para calcular la correlación.")
    if metodo == "pearson":
        r, p = stats.pearsonr(datos[columna_clima], datos[columna_economia])
    elif metodo == "spearman":
        r, p = stats.spearmanr(datos[columna_clima], datos[columna_economia])
    else:
        raise ValueError("metodo debe ser 'pearson' o 'spearman'.")
    return {"metodo": metodo, "coeficiente": r, "p_valor": p, "n_observaciones": len(datos)}
