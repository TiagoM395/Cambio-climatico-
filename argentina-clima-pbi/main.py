"""
main.py — Punto de entrada informativo del proyecto argentina-clima-pbi.
Para correr el pipeline completo, ver COMO_EJECUTAR.md (9 scripts en orden).
"""

from src.data_loader import listar_datasets_crudos_disponibles, cargar_fuentes_documentadas


def main():
    print("Proyecto: Análisis del cambio climático y su relación con el "
          "crecimiento económico en Argentina")
    print("-" * 70)
    datasets = listar_datasets_crudos_disponibles()
    print(f"Datasets crudos disponibles en data/raw/: {datasets or 'ninguno todavía'}")
    try:
        fuentes = cargar_fuentes_documentadas()
        print(f"Fuentes documentadas en data/sources.csv: {len(fuentes)}")
    except FileNotFoundError as e:
        print(f"Aviso: {e}")
    print("-" * 70)
    print("Ver COMO_EJECUTAR.md para correr el pipeline completo (9 pasos).")


if __name__ == "__main__":
    main()
