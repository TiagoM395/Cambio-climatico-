"""
modeling.py
============

Utilidades comunes de modelado, usadas para predecir el crecimiento
económico (PBI/PBG) a partir de variables climáticas (ver proyecto.txt,
secciones 22 a 28). División cronológica obligatoria (no aleatoria);
nunca se usa información futura para entrenar.
"""

import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def dividir_train_test_cronologico(df: pd.DataFrame, columna_anio: str, anio_corte: int):
    train = df[df[columna_anio] <= anio_corte].copy()
    test = df[df[columna_anio] > anio_corte].copy()
    if train.empty or test.empty:
        raise ValueError("La división cronológica dejó vacío el set de entrenamiento o prueba.")
    return train, test


def entrenar_regresion_lineal(X_train, y_train) -> LinearRegression:
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    return modelo


def entrenar_regresion_lineal_ols(X_train: pd.DataFrame, y_train: pd.Series):
    """Regresión OLS (statsmodels): coeficientes, IC, p-valor y diagnóstico de residuos."""
    X_train_const = sm.add_constant(X_train, has_constant="add")
    return sm.OLS(y_train, X_train_const).fit()


def resumen_ols(modelo) -> pd.DataFrame:
    ic = modelo.conf_int(alpha=0.05)
    ic.columns = ["ic_95_inferior", "ic_95_superior"]
    return pd.DataFrame({
        "coeficiente": modelo.params,
        "error_estandar": modelo.bse,
        "p_valor": modelo.pvalues,
    }).join(ic)


def entrenar_random_forest(X_train, y_train, **kwargs) -> RandomForestRegressor:
    modelo = RandomForestRegressor(random_state=42, **kwargs)
    modelo.fit(X_train, y_train)
    return modelo


def evaluar_modelo(modelo, X_test, y_test) -> dict:
    predicciones = modelo.predict(X_test)
    return {
        "MAE": mean_absolute_error(y_test, predicciones),
        "RMSE": mean_squared_error(y_test, predicciones) ** 0.5,
        "R2": r2_score(y_test, predicciones),
    }
