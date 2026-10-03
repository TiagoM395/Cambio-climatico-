"""
utils/datos.py
================

Carga de datos para el front, con cache. Lee exclusivamente de
`data_front/` (copia local de los resultados reales generados por
`argentina-clima-pbi`). No recalcula nada: solo lee y presenta.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent / "data_front"
PROVINCIAS_ORDEN = [
    "Buenos Aires", "CABA", "Catamarca", "Chaco", "Chubut", "Córdoba",
    "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja",
    "Mendoza", "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan",
    "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero",
    "Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Tucumán",
]


@st.cache_data
def cargar_dataset_nacional() -> pd.DataFrame:
    return pd.read_csv(BASE_DIR / "processed" / "dataset_nacional.csv")


@st.cache_data
def cargar_dataset_provincial() -> pd.DataFrame:
    return pd.read_csv(BASE_DIR / "processed" / "dataset_provincial.csv")


@st.cache_data
def cargar_tabla(nombre_archivo: str) -> pd.DataFrame:
    return pd.read_csv(BASE_DIR / "tables" / nombre_archivo)


@st.cache_data
def cargar_fuentes() -> pd.DataFrame:
    return pd.read_csv(BASE_DIR / "sources.csv")


@st.cache_data
def cargar_geometria():
    import geopandas as gpd
    return gpd.read_file(BASE_DIR / "geo" / "ign_provincia.shp")


def ruta_figura(nombre_archivo: str) -> Path:
    return BASE_DIR / "figures" / nombre_archivo


def leer_markdown(nombre_archivo: str) -> str:
    return (BASE_DIR / nombre_archivo).read_text(encoding="utf-8")
