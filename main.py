import pandas as pd
from src.parser import load_dataset
from src.analysis import plot_categories, plot_vehicles_map, plot_accident_history


def main():
    df = load_dataset("data/out_200000.csv")
    if df.empty:
        print("El DataFrame está vacío. Asegúrate de que el archivo CSV tenga datos válidos.")
        return

    print("Análisis de datos:")
    df.describe(include="all")
    df.info()
    df.head()
    df.isnull().sum()

    # Vehicle Distribution
    columns_to_plot = ["brand", "year", "fuel_type", "transmission_type"]
    plot_categories(df, columns_to_plot, nrows=2, ncols=2, namefile="cars_distribution.png")

    # Insurance Distribution
    columns_to_plot = ["insurance_provider", "vehicle_type", "vehicle_status", "accident_history"]
    plot_categories(df, columns_to_plot, nrows=2, ncols=2, namefile="insurance_distribution.png")

    plot_vehicles_map(df)

    plot_accident_history(df)

    # plot_status_vs_value(df)
    print("Análisis completado. Gráficos guardados en carpeta 'plots'.")


if __name__ == "__main__":
    main()
