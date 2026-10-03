"""
data_loader.py
================

Funciones para cargar los datos crudos (`data/raw/`) provenientes de las
fuentes documentadas en `data/sources.csv`.

IMPORTANTE (ver proyecto.txt, secciones 4 y 5):
- Ninguna función de este módulo debe inventar datos ni generar valores
  artificiales si una fuente no está disponible.
- Si una fuente no pudo descargarse automáticamente, la función debe
  informarlo explícitamente (excepción o log claro) en lugar de continuar
  con datos faltantes silenciosos.
- Todo dataset multipaís debe filtrarse exclusivamente a Argentina
  (código de país "ARG" o equivalente de la fuente) antes de devolverlo.
"""

from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
SOURCES_FILE = Path(__file__).resolve().parent.parent / "data" / "sources.csv"

# Listado oficial de jurisdicciones argentinas válidas (23 provincias + CABA).
PROVINCIAS_ARGENTINA = [
    "Buenos Aires",
    "Catamarca",
    "Chaco",
    "Chubut",
    "Córdoba",
    "Corrientes",
    "Entre Ríos",
    "Formosa",
    "Jujuy",
    "La Pampa",
    "La Rioja",
    "Mendoza",
    "Misiones",
    "Neuquén",
    "Río Negro",
    "Salta",
    "San Juan",
    "San Luis",
    "Santa Cruz",
    "Santa Fe",
    "Santiago del Estero",
    "Tierra del Fuego, Antártida e Islas del Atlántico Sur",
    "Tucumán",
]

CABA = "CABA"
NACIONAL = "Argentina"

JURISDICCIONES_VALIDAS = PROVINCIAS_ARGENTINA + [CABA, NACIONAL]


def cargar_fuentes_documentadas() -> pd.DataFrame:
    """Carga data/sources.csv con el registro de fuentes utilizadas."""
    if not SOURCES_FILE.exists():
        raise FileNotFoundError(
            f"No se encontró {SOURCES_FILE}. Documentar la fuente antes de usarla."
        )
    return pd.read_csv(SOURCES_FILE)


def listar_datasets_crudos_disponibles() -> list[str]:
    """Devuelve los archivos actualmente presentes en data/raw/."""
    if not RAW_DIR.exists():
        return []
    return sorted(
        p.name for p in RAW_DIR.iterdir() if p.is_file() and not p.name.startswith(".")
    )
