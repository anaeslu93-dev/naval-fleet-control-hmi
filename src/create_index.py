from sqlalchemy import text
from database_manager import DatabaseManager

def create_database_index():
    # Inicializar el gestor y abrir la conexión con la base de datos
    db = DatabaseManager()
    db.connect()
    
    # Crear un cursor para la ejecución de comandos SQL directos
    cursor = db.conn.cursor()
    
    print("Creando índice inteligente para 'VesselType' en Docker... Esto puede tardar unos segundos.")
    
    # Definir la sentencia DDL para la indexación de la columna de tipos de buques
    sql_command = 'CREATE INDEX IF NOT EXISTS idx_vessel_type ON ais_ships ("VesselType");'
    
    try:
        # Ejecutar la creación del índice y consolidar los cambios en la transacción
        cursor.execute(sql_command)
        db.conn.commit()
        print("¡Índice creado con éxito! Las búsquedas del HMI ahora están indexadas.")
    except Exception as e:
        print(f"Error al crear el índice: {e}")
    finally:
        # Cerrar el cursor y liberar de forma segura la conexión física
        cursor.close()
        db.disconnect()

if __name__ == "__main__":
    create_database_index()