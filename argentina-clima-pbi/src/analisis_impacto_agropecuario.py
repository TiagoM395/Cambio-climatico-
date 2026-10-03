"""
analisis_impacto_agropecuario.py
================================

¿El clima afecta a la economía? Se mira por sector: el agropecuario (el más
expuesto al clima) contra el total de cada provincia.

Datos (todos descargados, nada inventado):
  - Valor agregado bruto por sector y provincia, 2004-2024 (CEPAL).
  - Lluvia y temperatura mensual por provincia, 1981-2023 (NASA POWER).

Método:
  - Crecimiento anual (%) del valor agregado agropecuario y del total provincial.
  - "Año seco": lluvia anual dentro del 25 % más bajo de la propia historia
    1981-2023 de esa provincia (misma definición que analisis_sequia_economia).
  - Regresión con efectos fijos de provincia Y de año (sacan lo que es propio de
    cada provincia y los shocks que afectan a todo el país a la vez, como 2009
    o 2020), errores agrupados por provincia.

Salidas (outputs/tables):
  impacto_agro_panel.csv, impacto_agro_resultados.csv,
  impacto_agro_por_provincia.csv, impacto_nacional_percapita.csv

Ejecutar:
    python -m src.analisis_impacto_agropecuario
"""

from pathlib import Path

import openpyxl
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

from src.construir_dataset import RAW_DIR, _parsear_año_encabezado, mapear_jurisdiccion

BASE = Path(__file__).resolve().parent.parent
TABLES = BASE / "outputs" / "tables"
PROCESSED = BASE / "data" / "processed"


def cargar_valor_agregado_por_sector() -> pd.DataFrame:
    wb = openpyxl.load_workbook(RAW_DIR / "cepal_pbg_provincial.xlsx", data_only=True)
    filas = []
    for ws in wb.worksheets:
        prov = mapear_jurisdiccion(ws.title)
        if prov is None:
            continue
        rows = list(ws.iter_rows(values_only=True))
        hdr = next(i for i, r in enumerate(rows) if r[1] == "Sector de actividad económica")
        años = [_parsear_año_encabezado(v) for v in rows[hdr][2:]]
        for r in rows[hdr + 1:]:
            if not isinstance(r[1], str):
                continue
            for a, v in zip(años, r[2:]):
                if a and isinstance(v, (int, float)):
                    filas.append((prov, a, r[1].strip(), v))
    return pd.DataFrame(filas, columns=["jurisdiccion", "año", "sector", "vab"])


def cargar_clima_anual() -> pd.DataFrame:
    clima = pd.read_csv(RAW_DIR / "nasa_power_clima_mensual_provincial.csv")
    anual = clima.groupby(["jurisdiccion", "año"]).agg(
        lluvia_mm=("precipitacion_mm", "sum"), temp=("temperatura_c", "mean")
    ).reset_index()
    anual["jurisdiccion"] = anual["jurisdiccion"].map(lambda x: mapear_jurisdiccion(x) or x)
    g = anual.groupby("jurisdiccion")
    anual["lluvia_rel"] = g["lluvia_mm"].transform(lambda s: (s / s.mean() - 1) * 100)
    anual["temp_anom"] = g["temp"].transform(lambda s: s - s.mean())
    anual["seco"] = g["lluvia_mm"].transform(lambda s: s <= s.quantile(0.25)).astype(int)
    return anual


def armar_panel() -> pd.DataFrame:
    sec = cargar_valor_agregado_por_sector()
    agro = sec[sec["sector"].str.startswith("Agricultura")][["jurisdiccion", "año", "vab"]].rename(columns={"vab": "vab_agro"})
    total = sec.groupby(["jurisdiccion", "año"], as_index=False)["vab"].sum().rename(columns={"vab": "vab_total"})
    p = agro.merge(total, on=["jurisdiccion", "año"]).sort_values(["jurisdiccion", "año"])
    p["peso_agro_pct"] = p["vab_agro"] / p["vab_total"] * 100
    g = p.groupby("jurisdiccion")
    p["crec_agro"] = g["vab_agro"].pct_change() * 100
    p["crec_total"] = g["vab_total"].pct_change() * 100
    p["peso_agro_medio"] = g["peso_agro_pct"].transform("mean")
    p = p.merge(cargar_clima_anual(), on=["jurisdiccion", "año"])
    return p.dropna(subset=["crec_agro", "crec_total", "lluvia_rel"]).reset_index(drop=True)


def resultados_regresion(panel: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for y, nombre_y in [("crec_agro", "Producción agropecuaria"), ("crec_total", "Economía total de la provincia")]:
        for f, nombre_f in [("seco", "Año seco"), ("temp_anom", "Temperatura (+1 °C)"), ("lluvia_rel", "Lluvia (+1 %)")]:
            mod = smf.ols(f"{y} ~ {f} + C(jurisdiccion) + C(año)", data=panel).fit(
                cov_type="cluster", cov_kwds={"groups": panel["jurisdiccion"]}
            )
            ci = mod.conf_int().loc[f]
            filas.append({
                "resultado": nombre_y, "factor": nombre_f, "coeficiente_pp": mod.params[f],
                "p_valor": mod.pvalues[f], "ic95_inf": ci[0], "ic95_sup": ci[1], "n": int(mod.nobs),
            })
    return pd.DataFrame(filas)


def resumen_por_provincia(panel: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for prov, g in panel.groupby("jurisdiccion"):
        s, n = g[g["seco"] == 1], g[g["seco"] == 0]
        filas.append({
            "jurisdiccion": prov, "peso_agro_medio_pct": g["peso_agro_medio"].iloc[0],
            "crec_agro_secos": s["crec_agro"].mean(), "crec_agro_normales": n["crec_agro"].mean(),
            "crec_total_secos": s["crec_total"].mean(), "crec_total_normales": n["crec_total"].mean(),
            "n_secos": len(s), "n_normales": len(n),
        })
    out = pd.DataFrame(filas)
    out["perdida_agro_pp"] = out["crec_agro_secos"] - out["crec_agro_normales"]
    out["perdida_total_pp"] = out["crec_total_secos"] - out["crec_total_normales"]
    return out


def nacional_percapita() -> pd.DataFrame:
    d = pd.read_csv(PROCESSED / "dataset_nacional.csv")
    filas = []
    for var, nombre in [
        ("anomalia_temperatura", "Anomalía de temperatura"),
        ("anomalia_precipitacion_pct", "Anomalía de precipitación"),
        ("emisiones_co2_fosil", "Emisiones de CO₂ fósil"),
    ]:
        x = d[["pib_per_capita_crecimiento_pct", var]].dropna()
        r, p = stats.pearsonr(x[var], x["pib_per_capita_crecimiento_pct"])
        filas.append({"variable": nombre, "pearson_r": r, "p_valor": p, "n": len(x)})
    return pd.DataFrame(filas)


def main():
    panel = armar_panel()
    res = resultados_regresion(panel)
    prov = resumen_por_provincia(panel)
    nac = nacional_percapita()
    TABLES.mkdir(parents=True, exist_ok=True)
    panel.to_csv(TABLES / "impacto_agro_panel.csv", index=False)
    res.to_csv(TABLES / "impacto_agro_resultados.csv", index=False)
    prov.to_csv(TABLES / "impacto_agro_por_provincia.csv", index=False)
    nac.to_csv(TABLES / "impacto_nacional_percapita.csv", index=False)
    pd.set_option("display.width", 220)
    print(f"Panel: {len(panel)} observaciones provincia-año, {panel['año'].min()}-{panel['año'].max()}")
    print(res.round(3).to_string(index=False))
    print(nac.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
