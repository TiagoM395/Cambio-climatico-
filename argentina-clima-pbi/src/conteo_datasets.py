"""
conteo_datasets.py
==================

Cuenta las filas reales de cada archivo descargado en data/raw/ y de los
datasets integrados en data/processed/. No inventa nada: solo mide.

Ejecutar:
    python -m src.conteo_datasets
"""

from pathlib import Path

import geopandas as gpd
import openpyxl
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
PROC = BASE / "data" / "processed"
SALIDA = BASE / "outputs" / "tables" / "conteo_datasets.csv"


def _filas_excel(archivo: Path, hojas_excluir=()) -> tuple[int, int]:
    """(hojas con datos, filas de datos): filas con etiqueta y al menos un valor numérico."""
    wb = openpyxl.load_workbook(archivo, read_only=True, data_only=True)
    hojas = filas = 0
    for ws in wb.worksheets:
        if ws.title in hojas_excluir:
            continue
        n = 0
        for fila in ws.iter_rows(values_only=True):
            etiqueta = next((c for c in fila[:2] if isinstance(c, str) and c.strip()), None)
            numeros = [c for c in fila[1:] if isinstance(c, (int, float)) and not isinstance(c, bool)]
            if etiqueta and len(numeros) >= 2:
                n += 1
        if n:
            hojas += 1
            filas += n
    return hojas, filas


def contar() -> pd.DataFrame:
    reg = []

    d = pd.read_csv(RAW / "ciam_anomalia_temp_precip_nacional.csv", sep=";")
    reg.append(("Anomalía de temperatura y precipitación nacional", "CIAM / SMN", "1961-2025", len(d), "años"))

    d = pd.read_csv(RAW / "ciam_precipitacion_estaciones.csv", sep=";")
    reg.append(("Precipitación anual por estación meteorológica", "CIAM / SMN", "2010-2024", len(d), "estaciones"))

    d = pd.read_csv(RAW / "banco_mundial_pbi_crecimiento.csv")
    reg.append(("Crecimiento anual del PBI", "Banco Mundial", f"{d['año'].min()}-{d['año'].max()}", len(d), "años"))

    tot = pd.read_csv(RAW / "owid_co2_data_mundial.csv", usecols=["country"])
    arg = pd.read_csv(RAW / "owid_co2_data_argentina.csv")
    reg.append((
        "Emisiones de CO₂, población y PBI (solo Argentina)", "Global Carbon Project / OWID",
        f"{arg['year'].min()}-{arg['year'].max()}", len(arg),
        f"años; filtrados de {len(tot):,} filas del archivo mundial".replace(",", "."),
    ))

    d = pd.read_csv(RAW / "nasa_power_temperatura_provincial.csv")
    reg.append(("Temperatura anual por provincia", "NASA POWER", f"{d['año'].min()}-{d['año'].max()}", len(d), "provincia-año"))

    d = pd.read_csv(RAW / "nasa_power_clima_mensual_provincial.csv")
    reg.append(("Clima mensual por provincia (temperatura, lluvia, viento)", "NASA POWER", f"{d['año'].min()}-{d['año'].max()}", len(d), "provincia-mes"))

    h, f = _filas_excel(RAW / "cepal_pbg_provincial.xlsx", hojas_excluir=("VABpb",))
    reg.append(("Producto bruto geográfico provincial (por sector)", "CEPAL", "2004-2024", f, f"filas en {h} hojas"))

    serie = pd.read_excel(RAW / "inventario-nacional-gei-emisiones_hasta_2022.xlsx", sheet_name=0, header=None)
    reg.append(("Inventario Nacional de GEI, serie por gas y sector", "Secretaría de Ambiente", "1990-2022", int((serie.notna().sum(axis=1) >= 3).sum()), "filas, hoja de la serie"))

    h, f = _filas_excel(RAW / "desagregacion-provincial_hasta_2022.xlsx")
    reg.append(("Inventario de GEI desagregado por provincia", "Secretaría de Ambiente", "2010-2022", f, f"filas en {h} hojas"))

    d = pd.read_csv(RAW / "magyp_estimaciones_agricolas.csv", low_memory=False)
    reg.append((
        "Estimaciones agrícolas por cultivo, provincia y departamento", "Ministerio de Economía (Agricultura)",
        f"{int(d['anio'].min())}-{int(d['anio'].max())}", len(d), "cultivo-departamento-año",
    ))

    pob = pd.ExcelFile(RAW / "indec_poblacion_provincial_2010_2040.xls")
    filas_pob = 0
    for hoja in pob.sheet_names:
        if hoja == "GraphData" or hoja.startswith("01-"):
            continue
        t = pob.parse(hoja, header=None)
        filas_pob += int(pd.to_numeric(t[0], errors="coerce").between(2010, 2040).sum())
    reg.append(("Población por provincia (proyecciones)", "INDEC", "2010-2040", filas_pob, "provincia-año"))

    g = gpd.read_file(RAW / "geo_ign_provincias" / "ign_provincia.shp")
    reg.append(("Límites de provincias (mapa)", "IGN", "—", len(g), "polígonos"))

    out = pd.DataFrame(reg, columns=["dataset", "fuente", "periodo", "filas", "unidad"])
    out["tipo"] = "descargado"

    for nombre, archivo, unidad in [
        ("Dataset nacional integrado", "dataset_nacional.csv", "años"),
        ("Dataset provincial integrado", "dataset_provincial.csv", "provincia-año"),
    ]:
        d = pd.read_csv(PROC / archivo)
        out.loc[len(out)] = [nombre, "Unión por año de los anteriores", f"{d['año'].min()}-{d['año'].max()}", len(d), unidad, "integrado"]
    return out


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    df = contar()
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SALIDA, index=False)
    pd.set_option("display.width", 250, "display.max_colwidth", 70)
    print(df)
