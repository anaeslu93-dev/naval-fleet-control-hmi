# Librerias
import pandas as pd
from rich.console import Console
from rich.table import Table

# Crear consola de Rich
console = Console()

# Ruta del dataset
csv_path = r"C:\Users\Annam\Desktop\PROYECTOS\NAVAL FLEET CONTROL HMI\data\processed_AIS_dataset.csv"

# Cargar CSV
ais_data = pd.read_csv(csv_path)

# Seleccionar columnas clave para mostrar
columns_to_show = ['VesselName', 'LAT', 'LON', 'SOG_kmh', 'COG', 'ETA_hours', 'Speed_Category']

# Mostrar primeras 10 filas en formato Rich
table = Table(title="Primeras filas del dataset AIS (columnas clave)")

# Agregar columnas a la tabla
for col in columns_to_show:
    table.add_column(col)

# Agregar las primeras 10 filas
for _, row in ais_data[columns_to_show].head(10).iterrows():
    table.add_row(*[str(x) for x in row])

# Imprimir la tabla
console.print(table)

# Mostrar estadísticas resumidas de las columnas clave
console.print("\nEstadísticas resumidas de las columnas clave:")
console.print(ais_data[columns_to_show].describe().to_string())