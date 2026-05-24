import psycopg2
import pandas as pd

class DatabaseManager:
    def __init__(self):
        # Configurar los parámetros de conexión definidos en docker-compose.yml
        # Nota técnica: utilizar el puerto 5433 para mitigar conflictos locales
        self.host = "localhost"
        self.port = "5433"
        self.user = "ana_admin"
        self.password = "password_proyecto_123"
        self.database = "naval_fleet_db"
        self.conn = None

    def connect(self):
        """Establecer la conexión con la base de datos PostgreSQL alojada en Docker."""
        try:
            if not self.conn or self.conn.closed:
                self.conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                print("Conexión exitosa a la base de datos del proyecto NAVAL FLEET CONTROL HMI en Docker.")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        """Cerrar la conexión física de forma segura y liberar recursos."""
        if self.conn and not self.conn.closed:
            self.conn.close()
            print("Conexión cerrada de forma segura.")

if __name__ == "__main__":
    # Realizar una prueba de ciclo completo de conexión y desconexión
    db = DatabaseManager()
    db.connect()
    db.disconnect()