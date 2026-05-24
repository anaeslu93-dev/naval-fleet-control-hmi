# ⚓ NAVAL FLEET CONTROL HMI & BIG DATA ARCHITECTURE

Este proyecto consiste en el desarrollo de un **Centro de Control Naval (HMI)** profesional e interactivo diseñado para la ingesta, procesamiento, almacenamiento y análisis analítico de datos de geolocalización marítima (sistema AIS) con más de **1.1 millones de registros**.

La arquitectura ha sido migrada de un modelo plano y estático basado en archivos CSV a una infraestructura moderna de datos empresariales utilizando contenedores virtuales.

---

## Documentación Técnica e Informe Ejecutivo

Toda la auditoría de la arquitectura del sistema, la estrategia de optimización mediante indexación en el backend y el análisis de funcionalidades de la interfaz se han recopilado en un informe formal de ingeniería en inglés.

**[Descargar Informe Técnico de Arquitectura (PDF)](./docs/Naval_Fleet_Control_Architecture_Report.pdf)**

---

## Tecnologías y Arquitectura Utilizadas

* **Front-end / Interfaz**: `Streamlit` y `Plotly Express` para la visualización de mapas interactivos de geolocalización, histogramas analíticos de velocidad (SOG) y métricas de rendimiento en tiempo real.
* **Back-end / Lógica**: `Python 3` utilizando programación modular y gestión optimizada de memoria.
* **Base de Datos**: `PostgreSQL 15` corriendo de manera aislada y persistente.
* **ORM / Conectores**: `SQLAlchemy` y `Psycopg2` para inyección masiva de datos estructurados en bloques (*chunksize*).
* **Infraestructura**: `Docker` y `Docker Compose` para garantizar la portabilidad y despliegue inmediato del entorno en cualquier sistema operativo.
* **Optimización**: Creación de un **Índice B-Tree SQL (`idx_vessel_type`)** en el motor de la base de datos para reducir los tiempos de consulta y filtrado a submilisegundos, optimizando el consumo de memoria RAM.

---

## Cómo Ejecutar el Proyecto

### 1. Requisitos Previos
Tener instalado **Docker Desktop**, **Python 3** y las dependencias del entorno virtual (`streamlit`, `pandas`, `sqlalchemy`, `plotly`).

### 2. Levantar la Base de Datos (Docker)
Abre la terminal en la raíz del proyecto y enciende el contenedor virtual en segundo plano:
```bash
docker compose up -d