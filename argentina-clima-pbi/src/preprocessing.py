"""
preprocessing.py
=================

Funciones de limpieza, validación y control de calidad geográfico/temporal
(ver proyecto.txt, secciones 14, 33, 34 y 35).
"""

import pandas as pd

from .data_loader import JURISDICCIONES_VALIDAS


def validar_jurisdicciones(df: pd.DataFrame, columna: str = "jurisdiccion") -> pd.DataFrame:
    """Verifica que todas las jurisdicciones sean válidas. No corrige nada automáticamente."""
    presentes = set(df[columna].dropna().unique())
    invalidas = presentes - set(JURISDICCIONES_VALIDAS)
    return pd.DataFrame({"jurisdiccion_invalida": sorted(invalidas)})


def detectar_duplicados(df: pd.DataFrame, claves: list[str]) -> pd.DataFrame:
    """Devuelve las filas duplicadas según las columnas clave."""
    return df[df.duplicated(subset=claves, keep=False)].sort_values(claves)


def detectar_anios_faltantes(df: pd.DataFrame, columna_anio: str = "año") -> list[int]:
    """Devuelve los años faltantes dentro del rango [mín, máx] observado."""
    anios_presentes = sorted(df[columna_anio].dropna().unique())
    if not anios_presentes:
        return []
    rango_completo = set(range(int(anios_presentes[0]), int(anios_presentes[-1]) + 1))
    return sorted(rango_completo - set(int(a) for a in anios_presentes))


def verificar_multiplicacion_por_merge(
    df_izquierda: pd.DataFrame, df_resultado: pd.DataFrame
) -> bool:
    """Comprueba que un merge no haya multiplicado accidentalmente las filas."""
    return len(df_resultado) > len(df_izquierda)


def generar_informe_calidad(df: pd.DataFrame) -> dict:
    """Genera un resumen básico de calidad de datos."""
    informe = {
        "n_filas": len(df),
        "n_columnas": df.shape[1],
        "nulos_por_columna": df.isna().sum().to_dict(),
    }
    if "año" in df.columns:
        informe["anio_min"] = df["año"].min()
        informe["anio_max"] = df["año"].max()
    return informe
