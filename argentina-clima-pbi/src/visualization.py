"""
visualization.py
==================

Funciones de graficación (ver proyecto.txt, secciones 15, 16 y 30).
Todo gráfico incluye título, ejes con unidades y fuente.
"""

from pathlib import Path
import matplotlib.pyplot as plt

FIGURES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"


def graficar_serie_temporal(
    df, columna_anio: str, columna_valor: str, titulo: str, etiqueta_y: str,
    fuente: str, nombre_archivo: str,
):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df[columna_anio], df[columna_valor], marker="o")
    ax.set_title(titulo)
    ax.set_xlabel("Año")
    ax.set_ylabel(etiqueta_y)
    ax.figure.text(0.01, 0.01, f"Fuente: {fuente}", fontsize=8, color="gray")
    fig.tight_layout()
    ruta = FIGURES_DIR / nombre_archivo
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def graficar_normalizado(df, columna_anio: str, columnas_valor: dict, titulo: str,
                          fuente: str, nombre_archivo: str):
    """Varias variables en z-score en un mismo eje, para comparar tendencias."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for columna, etiqueta in columnas_valor.items():
        serie = df[[columna_anio, columna]].dropna()
        z = (serie[columna] - serie[columna].mean()) / serie[columna].std()
        ax.plot(serie[columna_anio], z, marker="o", markersize=3, label=etiqueta)
    ax.set_title(titulo)
    ax.set_xlabel("Año")
    ax.set_ylabel("Valor normalizado (z-score, adimensional)")
    ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
    ax.legend(fontsize=8)
    ax.figure.text(
        0.01, 0.01,
        f"Fuente: {fuente} | Normalización z-score: no comparar magnitudes absolutas entre series",
        fontsize=7, color="gray",
    )
    fig.tight_layout()
    ruta = FIGURES_DIR / nombre_archivo
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def graficar_comparacion_provincias(df, columna_jurisdiccion: str, columna_valor: str,
                                     titulo: str, etiqueta_y: str, fuente: str,
                                     nombre_archivo: str, agregacion: str = "mean"):
    """Ranking descriptivo (barras horizontales) entre provincias."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    datos = df[[columna_jurisdiccion, columna_valor]].dropna()
    if agregacion == "last":
        resumen = datos.groupby(columna_jurisdiccion)[columna_valor].last()
    else:
        resumen = datos.groupby(columna_jurisdiccion)[columna_valor].agg(agregacion)
    resumen = resumen.sort_values()

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(resumen.index, resumen.values)
    ax.set_title(titulo, fontsize=11)
    ax.set_xlabel(etiqueta_y)
    ax.set_ylabel("Jurisdicción")
    ax.figure.text(0.01, 0.01, f"Fuente: {fuente}", fontsize=8, color="gray")
    fig.tight_layout()
    ruta = FIGURES_DIR / nombre_archivo
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta
