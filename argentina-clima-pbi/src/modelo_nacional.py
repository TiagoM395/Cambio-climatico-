"""
modelo_nacional.py
====================

Modelo predictivo del CRECIMIENTO DEL PBI a partir del clima, nivel
nacional (proyecto.txt, secciones 22 a 26). Variable elegida a predecir:
`pbi_crecimiento_pct` (variación anual del PBI, Banco Mundial). Se eligió
esta y no la temperatura porque la pregunta del proyecto es económica:
qué tan bien explica el clima al crecimiento, no al revés.

DECISIÓN DE DATOS: para emisiones_co2 se usa la serie de Our World in
Data / Global Carbon Project (emisiones_co2_fosil, 1961-2024), NO la
oficial de GEI (solo 2010-2022, 13 obs, insuficiente para una división
cronológica razonable). Sustitución documentada, no silenciosa.

Ejecutar:
    python -m src.modelo_nacional
"""

from pathlib import Path
import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

from src.modeling import (
    dividir_train_test_cronologico, entrenar_random_forest,
    entrenar_regresion_lineal_ols, evaluar_modelo, resumen_ols,
)
from src.visualization import FIGURES_DIR

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
TABLES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "tables"
MODELS_DIR = Path(__file__).resolve().parent.parent / "outputs" / "models"

VARIABLE_OBJETIVO = "pbi_crecimiento_pct"
PREDICTORAS = ["año", "anomalia_precipitacion_pct", "anomalia_temperatura", "emisiones_co2_fosil"]
AÑO_CORTE = 2009


def preparar_datos() -> pd.DataFrame:
    df = pd.read_csv(PROCESSED_DIR / "dataset_nacional.csv")
    columnas = list(dict.fromkeys(["año", VARIABLE_OBJETIVO] + PREDICTORAS))
    return df[columnas].dropna()


def evaluar_regresion_lineal(train, test):
    X_train, y_train = train[PREDICTORAS], train[VARIABLE_OBJETIVO]
    X_test, y_test = test[PREDICTORAS], test[VARIABLE_OBJETIVO]
    modelo = entrenar_regresion_lineal_ols(X_train, y_train)
    import statsmodels.api as sm
    X_test_const = sm.add_constant(X_test, has_constant="add")
    predicciones = modelo.predict(X_test_const)
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    metricas = {
        "MAE": mean_absolute_error(y_test, predicciones),
        "RMSE": mean_squared_error(y_test, predicciones) ** 0.5,
        "R2": r2_score(y_test, predicciones),
    }
    return modelo, metricas, predicciones


def evaluar_random_forest(train, test):
    X_train, y_train = train[PREDICTORAS], train[VARIABLE_OBJETIVO]
    X_test, y_test = test[PREDICTORAS], test[VARIABLE_OBJETIVO]
    modelo = entrenar_random_forest(X_train, y_train, n_estimators=300, max_depth=4)
    metricas = evaluar_modelo(modelo, X_test, y_test)
    predicciones = modelo.predict(X_test)
    return modelo, metricas, predicciones


def graficar_prediccion_vs_observado(test, pred_lr, pred_rf, ruta):
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(test["año"], test[VARIABLE_OBJETIVO], "o-", label="Observado", color="black")
    ax.plot(test["año"], pred_lr, "s--", label="Regresión lineal (predicho)", alpha=0.8)
    ax.plot(test["año"], pred_rf, "^--", label="Random Forest (predicho)", alpha=0.8)
    ax.set_title("Crecimiento del PBI observado vs. predicho a partir del clima — período de prueba")
    ax.set_xlabel("Año")
    ax.set_ylabel("Crecimiento del PBI (% anual)")
    ax.legend()
    ax.figure.text(0.01, 0.01, "Predicción sobre datos ya observados (no es proyección futura). "
                                "Fuente: dataset_nacional.csv", fontsize=7, color="gray")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def graficar_residuos(y_test, pred, nombre_modelo, ruta):
    residuos = y_test.values - pred
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].scatter(pred, residuos)
    axes[0].axhline(0, color="red", linestyle="--")
    axes[0].set_xlabel("Valor predicho (% crecimiento del PBI)")
    axes[0].set_ylabel("Residuo (puntos porcentuales)")
    axes[0].set_title(f"Residuos vs. predicho — {nombre_modelo}")
    axes[1].hist(residuos, bins=8, edgecolor="black")
    axes[1].set_xlabel("Residuo (puntos porcentuales)")
    axes[1].set_title("Distribución de residuos")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def main():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    df = preparar_datos()
    print(f"Observaciones con las 4 predictoras completas: {len(df)} ({df['año'].min()}-{df['año'].max()})")
    train, test = dividir_train_test_cronologico(df, "año", AÑO_CORTE)
    print(f"Entrenamiento: {len(train)} obs | Prueba: {len(test)} obs")

    print("\n=== Modelo 1: Regresión lineal múltiple ===")
    modelo_lr, metricas_lr, pred_lr = evaluar_regresion_lineal(train, test)
    resumen = resumen_ols(modelo_lr)
    resumen.to_csv(TABLES_DIR / "modelo_lineal_nacional_coeficientes.csv")
    print(resumen.round(4).to_string())
    print("Métricas (prueba):", {k: round(v, 4) for k, v in metricas_lr.items()})

    print("\n=== Modelo 2: Random Forest Regressor ===")
    modelo_rf, metricas_rf, pred_rf = evaluar_random_forest(train, test)
    print("Métricas (prueba):", {k: round(v, 4) for k, v in metricas_rf.items()})

    importancias = pd.Series(modelo_rf.feature_importances_, index=PREDICTORAS).sort_values(ascending=False)
    perm = permutation_importance(modelo_rf, test[PREDICTORAS], test[VARIABLE_OBJETIVO], n_repeats=30, random_state=42)
    importancia_perm = pd.Series(perm.importances_mean, index=PREDICTORAS).sort_values(ascending=False)
    pd.DataFrame({"feature_importance": importancias, "permutation_importance": importancia_perm}
                 ).to_csv(TABLES_DIR / "modelo_rf_nacional_importancia_variables.csv")
    print(importancias.round(4))

    comparacion = pd.DataFrame({"Regresión lineal": metricas_lr, "Random Forest": metricas_rf}).T
    comparacion.to_csv(TABLES_DIR / "modelo_nacional_comparacion_metricas.csv")
    print("\n=== Comparación de métricas (prueba) ===")
    print(comparacion.round(4).to_string())

    tscv = TimeSeriesSplit(n_splits=5)
    from sklearn.ensemble import RandomForestRegressor
    rf_cv = RandomForestRegressor(n_estimators=300, max_depth=4, random_state=42)
    scores = cross_val_score(rf_cv, df[PREDICTORAS], df[VARIABLE_OBJETIVO], cv=tscv, scoring="neg_root_mean_squared_error")
    print(f"\nRMSE promedio TimeSeriesSplit (5 folds): {-scores.mean():.4f} (desvío: {scores.std():.4f})")

    graficar_prediccion_vs_observado(test, pred_lr, pred_rf, FIGURES_DIR / "prediccion_temperatura.png")
    graficar_residuos(test[VARIABLE_OBJETIVO], pred_rf, "Random Forest", FIGURES_DIR / "residuos_modelo_rf_nacional.png")

    joblib.dump(modelo_rf, MODELS_DIR / "modelo_rf_nacional.joblib")
    modelo_lr.save(str(MODELS_DIR / "modelo_lineal_nacional_ols.pickle"))
    print(f"\nModelos guardados en {MODELS_DIR}")


if __name__ == "__main__":
    main()
