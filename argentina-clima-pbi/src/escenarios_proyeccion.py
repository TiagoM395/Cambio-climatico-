"""
escenarios_proyeccion.py
==========================

Escenarios de proyección futura de temperatura (proyecto.txt, sección 27).
NO usa los modelos multivariados de modelo_nacional.py (R² negativo,
documentado) para no proyectar con algo ya probado como no confiable.
Usa extrapolación de tendencia simple (año -> anomalía), que no requiere
inventar valores futuros de otras variables.

Escenarios:
- A: continuidad de tendencia histórica completa (1961-2025).
- B: proyección científica EXTERNA (IPCC AR5, Barros et al. 2014, vía
  Tercera Comunicación Nacional de Argentina). No calculada por este
  proyecto.
- C: aceleración reciente (solo últimos 15 años).

Ejecutar:
    python -m src.escenarios_proyeccion
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
TABLES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "tables"
FIGURES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"

AÑO_LIMITE_PROYECCION = 2050
AÑOS_ESCENARIO_C = 15


def ajustar_ols_con_intervalo(df: pd.DataFrame, columna_anio: str, columna_valor: str):
    datos = df[[columna_anio, columna_valor]].dropna()
    X = sm.add_constant(datos[columna_anio])
    modelo = sm.OLS(datos[columna_valor], X).fit()
    return modelo, datos


def proyectar(modelo, años_futuros: np.ndarray) -> pd.DataFrame:
    X_futuro = sm.add_constant(pd.DataFrame({"año": años_futuros}), has_constant="add")
    prediccion = modelo.get_prediction(X_futuro)
    resumen = prediccion.summary_frame(alpha=0.05)
    resumen["año"] = años_futuros
    return resumen.rename(columns={
        "mean": "anomalia_proyectada", "obs_ci_lower": "ic95_inferior", "obs_ci_upper": "ic95_superior",
    })[["año", "anomalia_proyectada", "ic95_inferior", "ic95_superior"]]


def construir_escenario_a(df_nacional: pd.DataFrame):
    modelo, _ = ajustar_ols_con_intervalo(df_nacional, "año", "anomalia_temperatura")
    años_futuros = np.arange(2026, AÑO_LIMITE_PROYECCION + 1)
    proyeccion = proyectar(modelo, años_futuros)
    proyeccion["escenario"] = "A - Continuidad de tendencia histórica (1961-2025)"
    return proyeccion, modelo


def construir_escenario_c(df_nacional: pd.DataFrame):
    año_inicio = df_nacional["año"].max() - AÑOS_ESCENARIO_C + 1
    df_reciente = df_nacional[df_nacional["año"] >= año_inicio]
    modelo, _ = ajustar_ols_con_intervalo(df_reciente, "año", "anomalia_temperatura")
    años_futuros = np.arange(2026, AÑO_LIMITE_PROYECCION + 1)
    proyeccion = proyectar(modelo, años_futuros)
    proyeccion["escenario"] = f"C - Aceleración reciente ({año_inicio}-2025)"
    return proyeccion, modelo, año_inicio


def tabla_escenario_b() -> pd.DataFrame:
    filas = [
        {"escenario": "B - IPCC AR5 (Barros et al. 2014), RCP4.5, nacional",
         "horizonte": "Fin de siglo XXI (~2081-2100)", "anomalia_proyectada_c_min": 1.0,
         "anomalia_proyectada_c_max": 2.0, "nota_geografica": "1.0°C país, hasta 2.0°C en NOA"},
        {"escenario": "B - IPCC AR5 (Barros et al. 2014), RCP8.5, NOA",
         "horizonte": "Fin de siglo XXI (~2081-2100)", "anomalia_proyectada_c_min": None,
         "anomalia_proyectada_c_max": 3.5, "nota_geografica": "Solo dato regional NOA; sin promedio nacional"},
        {"escenario": "B - IPCC AR5 (Barros et al. 2014), corto plazo",
         "horizonte": "2016-2035", "anomalia_proyectada_c_min": 0.5,
         "anomalia_proyectada_c_max": 1.0, "nota_geografica": "Rango similar RCP4.5 y RCP8.5"},
    ]
    df = pd.DataFrame(filas)
    df["fuente"] = "IPCC AR5 (Barros et al. 2014), vía Tercera Comunicación Nacional de Argentina"
    df["tipo"] = "Proyección científica externa (NO calculada por este proyecto)"
    df["incertidumbre"] = "Alta: depende del escenario de emisiones global y trayectoria real"
    df["limitaciones"] = ("Período base no verificado con precisión; sin cifra nacional para RCP8.5 "
                           "a fin de siglo, solo regional (NOA)")
    return df


def graficar_escenarios(df_nacional, proy_a, proy_c, año_inicio_c):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.plot(df_nacional["año"], df_nacional["anomalia_temperatura"], "o-",
            color="black", markersize=3, linewidth=1, label="Observado (1961-2025)")
    ax.plot(proy_a["año"], proy_a["anomalia_proyectada"], "--", color="tab:blue",
            label="Escenario A: continuidad tendencia histórica completa")
    ax.fill_between(proy_a["año"], proy_a["ic95_inferior"], proy_a["ic95_superior"], color="tab:blue", alpha=0.15)
    ax.plot(proy_c["año"], proy_c["anomalia_proyectada"], "--", color="tab:orange",
            label=f"Escenario C: aceleración reciente ({año_inicio_c}-2025)")
    ax.fill_between(proy_c["año"], proy_c["ic95_inferior"], proy_c["ic95_superior"], color="tab:orange", alpha=0.15)
    ax.axvline(2025, color="gray", linewidth=0.8, linestyle=":")
    ax.text(2025.3, ax.get_ylim()[1] * 0.9, "← observado | proyectado →", fontsize=8, color="gray")
    ax.set_title("Escenarios de proyección de la anomalía de temperatura en Argentina hasta 2050\n"
                 "(A y C: extrapolación propia con IC 95%. Escenario B (IPCC) en tabla aparte)", fontsize=10)
    ax.set_xlabel("Año")
    ax.set_ylabel("Anomalía de temperatura (°C, base 1991-2020)")
    ax.legend(fontsize=8, loc="upper left")
    ax.figure.text(0.01, 0.01, "Fuente datos observados: CIAM/SMN. Proyecciones A y C: extrapolación "
                                "lineal propia, NO son un pronóstico validado.", fontsize=7, color="gray")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "prediccion_temperatura_escenarios.png", dpi=150)
    plt.close(fig)


def main():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    df_nacional = pd.read_csv(PROCESSED_DIR / "dataset_nacional.csv")

    print("=== Escenario A ===")
    proy_a, modelo_a = construir_escenario_a(df_nacional)
    print(f"Pendiente: {modelo_a.params['año']:.4f} °C/año (p={modelo_a.pvalues['año']:.4g})")
    print(proy_a[proy_a["año"].isin([2030, 2040, 2050])].round(3).to_string(index=False))

    print("\n=== Escenario C ===")
    proy_c, modelo_c, año_inicio_c = construir_escenario_c(df_nacional)
    print(f"Período base: {año_inicio_c}-2025 | Pendiente: {modelo_c.params['año']:.4f} °C/año "
          f"(p={modelo_c.pvalues['año']:.4g})")
    print(proy_c[proy_c["año"].isin([2030, 2040, 2050])].round(3).to_string(index=False))

    print("\n=== Escenario B (IPCC AR5, externo) ===")
    tabla_b = tabla_escenario_b()
    print(tabla_b[["escenario", "horizonte", "anomalia_proyectada_c_min", "anomalia_proyectada_c_max"]].to_string(index=False))

    proy_a.assign(escenario="A").to_csv(TABLES_DIR / "escenario_a_continuidad_tendencia.csv", index=False)
    proy_c.assign(escenario="C").to_csv(TABLES_DIR / "escenario_c_aceleracion_reciente.csv", index=False)
    tabla_b.to_csv(TABLES_DIR / "escenarios_proyeccion_b_ipcc.csv", index=False)
    graficar_escenarios(df_nacional, proy_a, proy_c, año_inicio_c)

    print(f"\nComparación en 2050: A = {proy_a[proy_a['año']==2050]['anomalia_proyectada'].values[0]:.2f}°C, "
          f"C = {proy_c[proy_c['año']==2050]['anomalia_proyectada'].values[0]:.2f}°C.")
    print("\nRECORDATORIO: observado=dato real. A/C=predicción de este proyecto. B=cita externa, no calculada.")


if __name__ == "__main__":
    main()
