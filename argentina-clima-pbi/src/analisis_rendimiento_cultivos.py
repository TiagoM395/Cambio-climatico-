"""
analisis_rendimiento_cultivos.py
================================

¿El clima de la temporada de cultivo afecta el rendimiento (kg por hectárea) de soja, maíz, trigo y
girasol en cada provincia? El rendimiento es la medida más directa del efecto del clima sobre el campo:
no depende de los precios ni de cuánta superficie se decidió sembrar.

Datos (todos descargados):
  - Estimaciones agrícolas por cultivo, provincia y departamento, 1969-2025 (Ministerio de Economía).
  - Temperatura y lluvia mensual por provincia, 1981-2023 (NASA POWER).

Método:
  - Rendimiento provincial = producción total / superficie cosechada total de la provincia (solo provincias
    con al menos 2.000 ha cosechadas del cultivo ese año).
  - Clima de la temporada de cultivo (no del año calendario): soja y maíz/girasol, octubre-noviembre del
    año de siembra a marzo del siguiente; trigo, julio a noviembre del mismo año.
  - Anomalía de temperatura y de lluvia de la temporada respecto del promedio de esa provincia.
  - Regresión del logaritmo del rendimiento con efectos fijos de provincia y de campaña (el efecto fijo de
    campaña descuenta el avance tecnológico y los shocks comunes a todo el país), errores agrupados por
    provincia. Robustez: tendencia propia de cada provincia (queda una colinealidad menor con los efectos fijos de campaña, que no afecta al coeficiente de
    la temperatura), prueba de permutación, sacar de a una provincia y placebo con el clima de la campaña siguiente.

Salidas (outputs/tables):
  rendimiento_panel.csv, rendimiento_resultados.csv, rendimiento_por_provincia.csv, rendimiento_nacional.csv

Ejecutar:
    python -m src.analisis_rendimiento_cultivos
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from src.construir_dataset import RAW_DIR, mapear_jurisdiccion

BASE = Path(__file__).resolve().parent.parent
TABLES = BASE / "outputs" / "tables"
MIN_HA = 2000
MIN_ANIOS = 15
N_PERM = 1000
SEMILLA = 42

# cultivo -> (nombres en el archivo, meses de la temporada como (desplazamiento de año, mes))
CULTIVOS = {
    "Soja": (["soja total"], [(0, 11), (0, 12), (1, 1), (1, 2), (1, 3)]),
    "Maíz": (["maíz"], [(0, 10), (0, 11), (0, 12), (1, 1), (1, 2), (1, 3)]),
    "Girasol": (["girasol"], [(0, 10), (0, 11), (0, 12), (1, 1), (1, 2), (1, 3)]),
    "Trigo": (["trigo total"], [(0, 7), (0, 8), (0, 9), (0, 10), (0, 11)]),
}


def cargar_clima_mensual():
    c = pd.read_csv(RAW_DIR / "nasa_power_clima_mensual_provincial.csv")
    c["jurisdiccion"] = c["jurisdiccion"].map(lambda x: mapear_jurisdiccion(x) or x)
    return c


def clima_de_temporada(clima, meses):
    """Temperatura media y lluvia total de la temporada, indexadas por (provincia, año de siembra)."""
    filas = []
    años = sorted(clima["año"].unique())
    idx = clima.set_index(["jurisdiccion", "año", "mes"])
    for prov in clima["jurisdiccion"].unique():
        for y in años:
            t, ll, n = [], [], 0
            for d, m in meses:
                clave = (prov, y + d, m)
                if clave in idx.index:
                    r = idx.loc[clave]
                    t.append(r["temperatura_c"])
                    ll.append(r["precipitacion_mm"])
                    n += 1
            if n == len(meses):
                filas.append((prov, y, float(np.mean(t)), float(np.sum(ll))))
    return pd.DataFrame(filas, columns=["jurisdiccion", "anio", "temp_temporada", "lluvia_temporada"])


def rendimientos(cultivos_archivo):
    e = pd.read_csv(RAW_DIR / "magyp_estimaciones_agricolas.csv", low_memory=False).dropna(subset=["provincia"])
    e["jurisdiccion"] = e["provincia"].map(lambda x: mapear_jurisdiccion(x) or x)
    e["anio"] = e["anio"].astype(int)
    e = e[e["cultivo"].str.lower().isin(cultivos_archivo)]
    g = e.groupby(["jurisdiccion", "anio"], as_index=False).agg(
        cosechada=("superficie_cosechada_ha", "sum"), produccion=("produccion_tm", "sum")
    )
    g = g[(g["cosechada"] >= MIN_HA) & (g["produccion"] > 0)].copy()
    g["rendimiento_kgha"] = g["produccion"] * 1000 / g["cosechada"]
    g["log_rend"] = np.log(g["rendimiento_kgha"])
    return g


def armar_panel():
    clima = cargar_clima_mensual()
    paneles = []
    for cultivo, (archivo, meses) in CULTIVOS.items():
        r = rendimientos(archivo)
        c = clima_de_temporada(clima, meses)
        p = r.merge(c, on=["jurisdiccion", "anio"])
        g = p.groupby("jurisdiccion")
        p = p[g["anio"].transform("count") >= MIN_ANIOS].copy()
        g = p.groupby("jurisdiccion")
        p["temp_anom"] = p["temp_temporada"] - g["temp_temporada"].transform("mean")
        p["lluvia_rel"] = (p["lluvia_temporada"] / g["lluvia_temporada"].transform("mean") - 1) * 100
        p["cultivo"] = cultivo
        paneles.append(p)
    return pd.concat(paneles, ignore_index=True)


def ajustar(d, y, x, tendencia=False, fe="grupo"):
    """Efectos fijos del grupo (provincia, o cultivo-provincia en el conjunto) y de campaña; errores agrupados por provincia."""
    tend = f" + C({fe}):anio" if tendencia else ""
    return smf.ols(f"{y} ~ {x} + C({fe}) + C(anio){tend}", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["jurisdiccion"]}
    )


def resultados(panel):
    filas, controles = [], []
    rng = np.random.default_rng(SEMILLA)
    grupos = [(c, d.assign(grupo=d["jurisdiccion"])) for c, d in panel.groupby("cultivo")]
    grupos.append(("Todos los cultivos", panel.assign(grupo=panel["cultivo"] + "|" + panel["jurisdiccion"])))
    for cultivo, d in grupos:
        d = d.copy()
        base = "temp_anom + lluvia_rel"
        m = ajustar(d, "log_rend", base)
        m_t = ajustar(d, "log_rend", base, tendencia=True)
        real = m.params["temp_anom"]
        mayor, p = 0, d.copy()
        for _ in range(N_PERM):
            p["temp_anom"] = p.groupby("grupo")["temp_anom"].transform(lambda s: rng.permutation(s.values))
            c = smf.ols("log_rend ~ temp_anom + lluvia_rel + C(grupo) + C(anio)", data=p).fit().params["temp_anom"]
            mayor += abs(c) >= abs(real)
        # sacar de a una provincia
        ps, cs = [], []
        for prov in d["jurisdiccion"].unique():
            mm = ajustar(d[d["jurisdiccion"] != prov], "log_rend", base)
            ps.append(mm.pvalues["temp_anom"])
            cs.append(100 * mm.params["temp_anom"])
        # placebo: temperatura de la campaña siguiente (el clima futuro no puede afectar una cosecha pasada)
        dd = d.sort_values(["grupo", "anio"]).copy()
        dd["temp_futura"] = dd.groupby("grupo")["temp_anom"].shift(-1)
        dd["lluvia_futura"] = dd.groupby("grupo")["lluvia_rel"].shift(-1)
        dd = dd.dropna(subset=["temp_futura", "lluvia_futura"])
        mp = ajustar(dd, "log_rend", "temp_futura + lluvia_futura")
        # calentamiento de la temporada por década (promedio de las provincias)
        pend = np.mean([np.polyfit(g["anio"], g["temp_anom"], 1)[0] for _, g in d.groupby("grupo") if len(g) >= MIN_ANIOS]) * 10
        ci = m.conf_int().loc["temp_anom"]
        filas.append({
            "cultivo": cultivo, "n": int(m.nobs), "provincias": d["jurisdiccion"].nunique(),
            "anios": f"{int(d['anio'].min())}-{int(d['anio'].max())}",
            "temp_pct_por_grado": 100 * real, "temp_ic95_inf": 100 * ci[0], "temp_ic95_sup": 100 * ci[1],
            "temp_p": m.pvalues["temp_anom"], "temp_p_permutacion": (mayor + 1) / (N_PERM + 1),
            "temp_pct_con_tendencia": 100 * m_t.params["temp_anom"], "temp_p_con_tendencia": m_t.pvalues["temp_anom"],
            "sacar_provincia_p_max": max(ps), "sacar_provincia_efecto_min": min(cs), "sacar_provincia_efecto_max": max(cs),
            "sacar_provincia_significativas": f"{sum(x < 0.05 for x in ps)} de {len(ps)}",
            "placebo_temp_futura_pct": 100 * mp.params["temp_futura"], "placebo_temp_futura_p": mp.pvalues["temp_futura"],
            "lluvia_pct_por_10pct": 100 * 10 * m.params["lluvia_rel"], "lluvia_p": m.pvalues["lluvia_rel"],
            "calentamiento_temporada_por_decada": pend,
            "efecto_por_decada_pct": 100 * real * pend,
        })
    return pd.DataFrame(filas)


def por_provincia(panel):
    filas = []
    for (cultivo, prov), d in panel.groupby(["cultivo", "jurisdiccion"]):
        if len(d) < MIN_ANIOS:
            continue
        m = smf.ols("log_rend ~ temp_anom + lluvia_rel + anio", data=d).fit()
        filas.append({"cultivo": cultivo, "jurisdiccion": prov, "n": len(d),
                      "temp_pct_por_grado": 100 * m.params["temp_anom"], "temp_p": m.pvalues["temp_anom"],
                      "lluvia_pct_por_10pct": 1000 * m.params["lluvia_rel"], "lluvia_p": m.pvalues["lluvia_rel"]})
    return pd.DataFrame(filas)


def nacional(panel):
    """Serie nacional: rendimiento del país (producción total / superficie cosechada total) contra la temperatura y la lluvia
    promedio de las provincias productoras, con tendencia lineal (avance tecnológico) y errores robustos a la autocorrelación."""
    filas = []
    for cultivo, (archivo, _) in CULTIVOS.items():
        e = pd.read_csv(RAW_DIR / "magyp_estimaciones_agricolas.csv", low_memory=False).dropna(subset=["provincia"])
        e["anio"] = e["anio"].astype(int)
        e = e[e["cultivo"].str.lower().isin(archivo)]
        tot = e.groupby("anio", as_index=False).agg(cosechada=("superficie_cosechada_ha", "sum"), produccion=("produccion_tm", "sum"))
        tot["log_rend"] = np.log(tot["produccion"] * 1000 / tot["cosechada"])
        cl = panel[panel["cultivo"] == cultivo].groupby("anio", as_index=False).agg(temp_anom=("temp_anom", "mean"), lluvia_rel=("lluvia_rel", "mean"))
        d = tot.merge(cl, on="anio").sort_values("anio")
        m = smf.ols("log_rend ~ temp_anom + lluvia_rel + anio", data=d).fit(cov_type="HAC", cov_kwds={"maxlags": 2})
        ci = m.conf_int().loc["temp_anom"]
        reciente = tot[tot["anio"] >= tot["anio"].max() - 4]["produccion"].mean() / 1e6
        filas.append({
            "cultivo": cultivo, "n": int(m.nobs), "anios": f"{int(d['anio'].min())}-{int(d['anio'].max())}",
            "temp_pct_por_grado": 100 * m.params["temp_anom"], "temp_ic95_inf": 100 * ci[0], "temp_ic95_sup": 100 * ci[1], "temp_p": m.pvalues["temp_anom"],
            "produccion_reciente_mt": reciente, "perdida_mt_por_grado": reciente * abs(m.params["temp_anom"]) if m.params["temp_anom"] < 0 else 0.0,
            "r2": m.rsquared,
        })
    return pd.DataFrame(filas)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    panel = armar_panel()
    res = resultados(panel)
    prov = por_provincia(panel)
    nac = nacional(panel)
    TABLES.mkdir(parents=True, exist_ok=True)
    panel.to_csv(TABLES / "rendimiento_panel.csv", index=False)
    res.to_csv(TABLES / "rendimiento_resultados.csv", index=False)
    prov.to_csv(TABLES / "rendimiento_por_provincia.csv", index=False)
    nac.to_csv(TABLES / "rendimiento_nacional.csv", index=False)
    pd.set_option("display.width", 250)
    print(res.round(4).to_string(index=False))
    print(nac.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
