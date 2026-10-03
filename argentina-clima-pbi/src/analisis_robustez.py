"""
analisis_robustez.py
====================

¿Aguanta la única señal encontrada (el calor frena al campo)? Se la somete a
pruebas que intentan romperla. Si sobrevive, es más creíble; si se cae, se dice.

Pruebas (todas sobre el mismo panel de analisis_impacto_agropecuario.py):
  1. Corrección por comparaciones múltiples (Holm) sobre las 6 pruebas originales.
  2. Sacar de a una provincia (24 veces): ¿la señal depende de una sola?
  3. Sacar valores extremos (winsorizar al 5 % y 95 %).
  4. Prueba de permutación: mezclar al azar la temperatura entre años dentro de cada
     provincia 2.000 veces. Sin supuestos estadísticos: ¿cuántas veces el azar iguala el efecto?
  5. Prueba placebo: el mismo cálculo sobre sectores que NO dependen del clima
     (construcción, comercio, transporte, finanzas). Si dieran el mismo efecto, el
     resultado sería sospechoso.
  6. Sector agroindustrial (alimentos y bebidas), que sí depende del campo.
  7. Efecto rezagado: temperatura del año anterior.
  8. Año muy cálido (temperatura en el 25 % más alto de esa provincia), no solo grados de más.
  9. Dosis-respuesta: ¿el efecto es mayor donde el campo pesa más en la economía?

Salida: outputs/tables/robustez_resultados.csv

Ejecutar:
    python -m src.analisis_robustez
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.multitest import multipletests

from src.analisis_impacto_agropecuario import (
    armar_panel,
    cargar_valor_agregado_por_sector,
    resultados_regresion,
)

BASE = Path(__file__).resolve().parent.parent
TABLES = BASE / "outputs" / "tables"
SEMILLA = 42
N_PERMUTACIONES = 2000

SECTORES_PLACEBO = {
    "Construcción": "Construcci",
    "Comercio": "Comercio mayorista",
    "Transporte": "Transporte",
    "Intermediación financiera": "Intermediaci",
}


def ajustar(datos, y, x, extra=""):
    """Regresión con efectos fijos de provincia y año, errores agrupados por provincia."""
    mod = smf.ols(f"{y} ~ {x} {extra} + C(jurisdiccion) + C(año)", data=datos).fit(
        cov_type="cluster", cov_kwds={"groups": datos["jurisdiccion"]}
    )
    return mod


def fila(prueba, detalle, coef, p, n):
    return {"prueba": prueba, "detalle": detalle, "coeficiente": coef, "p_valor": p, "n": n}


def crecimiento_sector(prefijo, nombre):
    sec = cargar_valor_agregado_por_sector()
    s = sec[sec["sector"].str.startswith(prefijo)].groupby(["jurisdiccion", "año"], as_index=False)["vab"].sum()
    s = s.sort_values(["jurisdiccion", "año"])
    s[nombre] = s.groupby("jurisdiccion")["vab"].pct_change() * 100
    return s[["jurisdiccion", "año", nombre]]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    panel = armar_panel()
    filas = []

    # 1. Holm
    res = resultados_regresion(panel)
    ajustado = multipletests(res["p_valor"], method="holm")[1]
    for (_, r), pa in zip(res.iterrows(), ajustado):
        filas.append(fila("1. Corrección Holm (6 pruebas)", f"{r['factor']} → {r['resultado']}", r["coeficiente_pp"], pa, int(r["n"])))

    # 2. Sacar de a una provincia
    coefs, ps = [], []
    for prov in panel["jurisdiccion"].unique():
        m = ajustar(panel[panel["jurisdiccion"] != prov], "crec_agro", "temp_anom")
        coefs.append(m.params["temp_anom"])
        ps.append(m.pvalues["temp_anom"])
    filas.append(fila("2. Sacar una provincia (peor caso)", f"p más alto al sacar {panel['jurisdiccion'].unique()[int(np.argmax(ps))]}", coefs[int(np.argmax(ps))], max(ps), len(panel)))
    filas.append(fila("2. Sacar una provincia (mejor caso)", f"efecto más fuerte al sacar {panel['jurisdiccion'].unique()[int(np.argmin(coefs))]}", min(coefs), ps[int(np.argmin(coefs))], len(panel)))
    filas.append(fila("2. Sacar una provincia (cuántas mantienen p<0,05)", f"{sum(p < 0.05 for p in ps)} de {len(ps)}", float(np.median(coefs)), float(np.median(ps)), len(panel)))

    # 3. Extremos
    p3 = panel.copy()
    lo, hi = p3["crec_agro"].quantile([0.05, 0.95])
    p3["crec_agro"] = p3["crec_agro"].clip(lo, hi)
    m = ajustar(p3, "crec_agro", "temp_anom")
    filas.append(fila("3. Sin valores extremos", "crecimiento agro recortado al 5 %-95 %", m.params["temp_anom"], m.pvalues["temp_anom"], int(m.nobs)))

    # 4. Permutación
    rng = np.random.default_rng(SEMILLA)
    real = ajustar(panel, "crec_agro", "temp_anom").params["temp_anom"]
    p4 = panel.copy()
    mas_extremos = 0
    for _ in range(N_PERMUTACIONES):
        p4["temp_anom"] = p4.groupby("jurisdiccion")["temp_anom"].transform(lambda s: rng.permutation(s.values))
        c = smf.ols("crec_agro ~ temp_anom + C(jurisdiccion) + C(año)", data=p4).fit().params["temp_anom"]
        mas_extremos += abs(c) >= abs(real)
    filas.append(fila("4. Permutación (azar puro)", f"{N_PERMUTACIONES} mezclas; veces que el azar iguala el efecto: {mas_extremos}", real, (mas_extremos + 1) / (N_PERMUTACIONES + 1), len(panel)))

    # 5. Placebo
    for nombre, prefijo in SECTORES_PLACEBO.items():
        c = crecimiento_sector(prefijo, "crec_placebo")
        d = panel.merge(c, on=["jurisdiccion", "año"]).replace([np.inf, -np.inf], np.nan).dropna(subset=["crec_placebo"])
        m = ajustar(d, "crec_placebo", "temp_anom")
        filas.append(fila("5. Placebo (sector sin relación con el clima)", nombre, m.params["temp_anom"], m.pvalues["temp_anom"], int(m.nobs)))

    # 6. Agroindustria
    c = crecimiento_sector("Elaboración de productos alimenticios", "crec_alim")
    d = panel.merge(c, on=["jurisdiccion", "año"]).replace([np.inf, -np.inf], np.nan).dropna(subset=["crec_alim"])
    m = ajustar(d, "crec_alim", "temp_anom")
    filas.append(fila("6. Agroindustria", "Alimentos y bebidas (depende del campo)", m.params["temp_anom"], m.pvalues["temp_anom"], int(m.nobs)))

    # 7. Rezago
    p7 = panel.sort_values(["jurisdiccion", "año"]).copy()
    p7["temp_anom_prev"] = p7.groupby("jurisdiccion")["temp_anom"].shift(1)
    p7 = p7.dropna(subset=["temp_anom_prev"])
    m = ajustar(p7, "crec_agro", "temp_anom_prev")
    filas.append(fila("7. Efecto rezagado", "temperatura del año anterior → campo", m.params["temp_anom_prev"], m.pvalues["temp_anom_prev"], int(m.nobs)))

    # 8. Año muy cálido
    p8 = panel.copy()
    p8["muy_calido"] = p8.groupby("jurisdiccion")["temp_anom"].transform(lambda s: s >= s.quantile(0.75)).astype(int)
    m = ajustar(p8, "crec_agro", "muy_calido")
    filas.append(fila("8. Año muy cálido", "25 % más cálido de cada provincia → campo", m.params["muy_calido"], m.pvalues["muy_calido"], int(m.nobs)))

    # 9. Dosis-respuesta
    p9 = panel.copy()
    p9["peso_c"] = p9["peso_agro_medio"] - p9["peso_agro_medio"].mean()
    m = smf.ols("crec_total ~ temp_anom + temp_anom:peso_c + C(jurisdiccion) + C(año)", data=p9).fit(
        cov_type="cluster", cov_kwds={"groups": p9["jurisdiccion"]}
    )
    k = "temp_anom:peso_c"
    filas.append(fila("9. Dosis-respuesta (economía total)", "calor × peso del campo: ¿pega más donde el campo pesa más?", m.params[k], m.pvalues[k], int(m.nobs)))
    prov = pd.read_csv(TABLES / "impacto_agro_por_provincia.csv")
    rho, p = stats.spearmanr(prov["peso_agro_medio_pct"], prov["perdida_agro_pp"])
    filas.append(fila("9. Dosis-respuesta (por provincia)", "peso del campo vs. pérdida en años secos (Spearman, 24 provincias)", rho, p, len(prov)))

    out = pd.DataFrame(filas)
    out.to_csv(TABLES / "robustez_resultados.csv", index=False)
    pd.set_option("display.width", 250, "display.max_colwidth", 90)
    print(out.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
