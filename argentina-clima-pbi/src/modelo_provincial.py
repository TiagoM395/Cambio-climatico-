"""
modelo_provincial.py
======================

Modelo predictivo provincial conjunto (proyecto.txt, secciones 22, 23, 28).
Provincia codificada con dummies, nunca con números arbitrarios.

Variable elegida a predecir: `pbg_crecimiento_pct`, la variación del PBG
de cada provincia respecto del año anterior — no el nivel de PBG (que
está dominado por el tamaño de cada economía provincial y por eso no
serviría para comparar el efecto del clima entre provincias grandes y
chicas) ni la temperatura (la pregunta del proyecto es económica).
Predictoras: año, precipitación, temperatura y emisiones — el PBG del
año anterior no se usa como predictora para no filtrar el resultado
dentro de la propia variable que se quiere predecir.

Ejecutar:
    python -m src.modelo_provincial
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from src.modeling import dividir_train_test_cronologico, entrenar_random_forest, evaluar_modelo
from src.visualization import FIGURES_DIR

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
TABLES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "tables"
MODELS_DIR = Path(__file__).resolve().parent.parent / "outputs" / "models"

VARIABLE_OBJETIVO = "pbg_crecimiento_pct"
PREDICTORAS_BASE = ["año", "precipitaciones_mm", "anomalia_temperatura", "emisiones_gei_co2eq"]
MIN_OBS_MODELO_INDIVIDUAL = 15
AÑO_CORTE = 2018


def calcular_crecimiento_pbg(df: pd.DataFrame) -> pd.DataFrame:
    """Variación % del PBG respecto del año anterior, por provincia. Solo entre
    años consecutivos (año actual - 1 == año anterior); si hay un hueco, queda NaN."""
    df = df.sort_values(["jurisdiccion", "año"]).copy()
    anterior_pbg = df.groupby("jurisdiccion")["pbg"].shift(1)
    anterior_año = df.groupby("jurisdiccion")["año"].shift(1)
    consecutivo = (df["año"] - anterior_año) == 1
    df["pbg_crecimiento_pct"] = ((df["pbg"] / anterior_pbg - 1) * 100).where(consecutivo)
    return df


def preparar_datos() -> pd.DataFrame:
    df = pd.read_csv(PROCESSED_DIR / "dataset_provincial.csv")
    df = calcular_crecimiento_pbg(df)
    columnas = list(dict.fromkeys(["año", "jurisdiccion", VARIABLE_OBJETIVO] + PREDICTORAS_BASE))
    return df[columnas].dropna()


def evaluar_disponibilidad_por_provincia(df: pd.DataFrame) -> pd.DataFrame:
    conteo = df.groupby("jurisdiccion").size().rename("n_observaciones").sort_values(ascending=False)
    conteo_df = conteo.to_frame()
    conteo_df["suficiente_para_modelo_individual"] = conteo_df["n_observaciones"] >= MIN_OBS_MODELO_INDIVIDUAL
    conteo_df.to_csv(TABLES_DIR / "disponibilidad_datos_modelo_provincial.csv")
    return conteo_df


def construir_modelo_conjunto(df: pd.DataFrame):
    df_dummies = pd.get_dummies(df, columns=["jurisdiccion"], prefix="prov")
    df_dummies["jurisdiccion_original"] = df["jurisdiccion"].values
    columnas_dummy = [c for c in df_dummies.columns if c.startswith("prov_")]
    predictoras = PREDICTORAS_BASE + columnas_dummy

    train, test = dividir_train_test_cronologico(df_dummies, "año", AÑO_CORTE)
    X_train, y_train = train[predictoras], train[VARIABLE_OBJETIVO]
    X_test, y_test = test[predictoras], test[VARIABLE_OBJETIVO]

    modelo = entrenar_random_forest(X_train, y_train, n_estimators=300, max_depth=5)
    metricas = evaluar_modelo(modelo, X_test, y_test)
    pred = modelo.predict(X_test)
    return modelo, metricas, train, test, pred, predictoras


def main():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    df = preparar_datos()
    print(f"Observaciones con las 4 predictoras completas: {len(df)} filas, "
          f"{df['jurisdiccion'].nunique()} jurisdicciones, {df['año'].min()}-{df['año'].max()}")

    disponibilidad = evaluar_disponibilidad_por_provincia(df)
    print(disponibilidad.to_string())
    if not disponibilidad[disponibilidad["suficiente_para_modelo_individual"]].shape[0]:
        print(f"\nLIMITACIÓN: ninguna provincia alcanza {MIN_OBS_MODELO_INDIVIDUAL} obs. "
              f"No se construyen modelos individuales; se evalúa un modelo CONJUNTO.")

    print(f"\n=== Modelo conjunto (pooled), corte cronológico en {AÑO_CORTE} ===")
    modelo, metricas, train, test, pred, predictoras = construir_modelo_conjunto(df)
    print(f"Entrenamiento: {len(train)} obs | Prueba: {len(test)} obs")
    print("Métricas (prueba):", {k: round(v, 4) for k, v in metricas.items()})

    importancias = pd.Series(modelo.feature_importances_, index=predictoras).sort_values(ascending=False)
    print("\nImportancia de variables (top 8):")
    print(importancias.head(8).round(4))
    importancias.to_csv(TABLES_DIR / "modelo_rf_provincial_importancia_variables.csv")
    pd.DataFrame([metricas]).to_csv(TABLES_DIR / "modelo_provincial_metricas.csv", index=False)

    test_resultado = test[["año", "jurisdiccion_original", VARIABLE_OBJETIVO]].copy()
    test_resultado = test_resultado.rename(columns={"jurisdiccion_original": "jurisdiccion"})
    test_resultado["prediccion"] = pred
    test_resultado.to_csv(TABLES_DIR / "modelo_provincial_predicciones_test.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(test_resultado[VARIABLE_OBJETIVO], test_resultado["prediccion"], alpha=0.6)
    lims = [min(test_resultado[VARIABLE_OBJETIVO].min(), test_resultado["prediccion"].min()),
            max(test_resultado[VARIABLE_OBJETIVO].max(), test_resultado["prediccion"].max())]
    ax.plot(lims, lims, "r--", linewidth=1, label="Predicción perfecta")
    ax.set_xlabel("Crecimiento del PBG observado (%)")
    ax.set_ylabel("Crecimiento del PBG predicho (%)")
    ax.set_title(f"Modelo provincial conjunto (Random Forest) — prueba {test['año'].min()}-{test['año'].max()}")
    ax.legend()
    ax.figure.text(0.01, 0.01, "Fuente: dataset_provincial.csv (modelo de este proyecto)", fontsize=7, color="gray")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "prediccion_pbg_provincial.png", dpi=150)
    plt.close(fig)

    import joblib
    joblib.dump(modelo, MODELS_DIR / "modelo_rf_provincial_conjunto.joblib")
    print(f"\nModelo guardado en {MODELS_DIR / 'modelo_rf_provincial_conjunto.joblib'}")


if __name__ == "__main__":
    main()
