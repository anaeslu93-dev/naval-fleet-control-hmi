# ⚓ NAVAL FLEET CONTROL HMI & BIG DATA ARCHITECTURE

[![Validación de Infraestructura & QA](https://github.com/anaeslu93-dev/naval-fleet-control-hmi/actions/workflows/ci-pipeline.yml/badge.svg)](https://github.com/anaeslu93-dev/naval-fleet-control-hmi/actions/workflows/ci-pipeline.yml)

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
## Estructura del Proyecto

```text
NAVAL_FLEET_CONTROL/
├── .github/
│   └── workflows/
│       └── ci-pipeline.yml     # Orquestación de Integración Continua (CI/CD)
├── docs/
│   └── Naval_Fleet_Control_Architecture_Report.pdf  # Informe oficial de ingeniería
├── src/
│   ├── import_csv_to_db.py     # Pipeline ETL optimizado para inyección masiva
│   └── hmi_main.py             # Interfaz web analítica reactiva (Streamlit)
├── docker-compose.yml          # Configuración de la infraestructura de PostgreSQL
└── requirements.txt            # Dependencias técnicas del entorno virtual
---

## Cómo Ejecutar el Proyecto

### 1. Requisitos Previos
Tener instalado **Docker Desktop**, **Python 3** y las dependencias del entorno virtual (`streamlit`, `pandas`, `sqlalchemy`, `plotly`).

### 2. Levantar la Base de Datos (Docker)
Abre la terminal en la raíz del proyecto y enciende el contenedor virtual en segundo plano:
```bash
docker compose up -d
```
### 3. Ejecutar el Pipeline ETL (Ingesta de Datos)
Inicia el script encargado de extraer los datos masivos del archivo original, transformarlos y transmitirlos en micro-batches estructurados hacia el contenedor activo de PostgreSQL:
```bash
python src/import_csv_to_db.py
```
### 4. Lanzar la Interfaz Táctica (HMI)
Inicializar la aplicación web de monitorización en tiempo real para desplegar el cuadro de mando interactivo en el navegador:
```bash
python -m streamlit run src/hmi_main.py
```
---

## Automatización DevOps e Infraestructura (CI/CD)

Este proyecto incorpora un flujo de **Integración Continua (CI)** automatizado mediante **GitHub Actions** (`.github/workflows/ci-pipeline.yml`). 

Cada vez que se realiza un empuje (`git push`) a la rama principal del repositorio, un servidor virtualizado en la nube (Ubuntu Enterprise Runner) ejecuta de forma autónoma las siguientes tareas de orquestación:
* **Aislamiento del Entorno:** Configura y despliega de forma nativa dependencias optimizadas de Python 3.11.
* **Verificación de la Infraestructura:** Levanta, orquesta y arranca el entorno de la base de datos **PostgreSQL** mediante **Docker Compose** en tiempo real para validar la integridad del despliegue.
* **Cierre Limpio del Sistema:** Desconecta e interrumpe las instancias de los contenedores de forma segura, garantizando que no existan fugas de memoria en el sistema objetivo.
