import pandas as pd
from sqlalchemy import create_engine
from database_manager import DatabaseManager

def import_data():
    # Instanciar el gestor de base de datos para recuperar credenciales
    db = DatabaseManager()
    
    # Configurar el motor de conexión de SQLAlchemy para escrituras masivas
    # Estructura estándar: postgresql://usuario:contraseña@servidor:puerto/base_datos
    engine_url = f"postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}"
    engine = create_engine(engine_url)
    
    # Definir la ruta local del archivo de datos marítimos (CSV)
    csv_path = r"C:\Users\Annam\Desktop\PROYECTOS\NAVAL FLEET CONTROL HMI\data\processed_AIS_dataset.csv"
    
    print("Leyendo el dataset CSV...")
    # Cargar el archivo CSV completo en un DataFrame de Pandas
    df = pd.read_csv(csv_path)
    
    print(f"Dataset cargado en memoria. Total de filas a importar: {len(df):,}")
    print("Iniciando la inyección masiva de datos en Docker (PostgreSQL)...")
    
    # Volcar los registros en la base de datos PostgreSQL alojada en Docker
    # Sobrescribir la tabla 'ais_ships' si ya existe y procesar en bloques de 50.000 filas
    df.to_sql('ais_ships', engine, if_exists='replace', index=False, chunksize=50000)
    
    print("Todos los datos de la flota naval están guardados en la base de datos de Docker.")

if __name__ == "__main__":
    import_data()