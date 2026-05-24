import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from database_manager import DatabaseManager

# Configurar la geometría y parámetros iniciales de la ventana en Streamlit
st.set_page_config(page_title="NAVAL COMMAND CENTER", layout="wide", page_icon="⚓")

st.title("⚓ NAVAL COMMAND CENTER")
st.subheader("Panel del Sistema de Control Marítimo (Powered by PostgreSQL & Docker)")

# ==========================================
# 1. DICCIONARIO INTERNACIONAL AMPLIADO (AIS)
# ==========================================
VESSEL_MAP = {
    0: "Not Available (No disponible)",
    30: "Fishing (Pesca)",
    31: "Tug / Tow (Remolcador Especial)",
    32: "Tug / Tow (Remolcador de Empuje)",
    33: "Dredging / Underwater Ops (Draga / Operaciones Subacuáticas)",
    34: "Dive Vessel (Buque de Buceo)",
    35: "Military Ops (Operaciones Militares)",
    36: "Sailing Vessel (Velero)",
    37: "Pleasure Craft (Embarcación de Recreo)",
    38: "Search and Rescue (Búsqueda y Rescate)",
    39: "Local Vessel / Small Craft",
    40: "High Speed Craft (Alta Velocidad)",
    50: "Pilot Vessel (Buque Práctico)",
    51: "Search and Rescue (Salvamento)",
    52: "Tug / Tow (Remolcador Estándar)",
    53: "Port Tender (Embarcación de Puerto)",
    54: "Anti-Pollution (Buque Anticontaminación)",
    55: "Law Enforcement (Patrullera / Policía)",
    56: "Local Vessel (Fuerzas Locales)",
    57: "Local Vessel B",
    58: "Medical Transport (Transporte Médico)",
    59: "Non-Combatant Vessel (Buque No Combatiente)",
    60: "Passenger (Pasajeros / Ferry)",
    70: "Cargo (Carga General)",
    71: "Cargo - Hazard Cat A (Carga Peligrosa A)",
    72: "Cargo - Hazard Cat B (Carga Peligrosa B)",
    73: "Cargo - Hazard Cat C (Carga Peligrosa C)",
    74: "Cargo - Hazard Cat D (Carga Peligrosa D)",
    80: "Tanker (Petrolero / Tanque)",
    81: "Tanker - Hazard Cat A (Petrolero Cat A)",
    82: "Tanker - Hazard Cat B (Petrolero Cat B)",
    90: "Other Type of Ship (Otros tipos)"
}

# ==========================================
# 2. CONEXIÓN DE MOTOR CON LA BASE DE DATOS
# ==========================================
@st.cache_resource
def get_db_engine():
    # Inicializar el gestor de base de datos para recuperar credenciales
    db = DatabaseManager()
    engine_url = f"postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}"
    return create_engine(engine_url)

engine = get_db_engine()

# ==========================================
# 3. DISEÑO DE LA BARRA LATERAL (SIDEBAR)
# ==========================================
st.sidebar.header("🔍 Filtros de Operación")

# Extraer de forma dinámica los códigos numéricos únicos disponibles en la base de datos
@st.cache_data
def get_unique_vessel_types():
    query = "SELECT DISTINCT \"VesselType\" FROM ais_ships WHERE \"VesselType\" IS NOT NULL ORDER BY \"VesselType\";"
    df_types = pd.read_sql(query, engine)
    return df_types["VesselType"].tolist()

try:
    numeric_types = get_unique_vessel_types()
    
    # Formatear el diccionario de selección traduciendo identificadores numéricos a texto
    dropdown_options = {t: f"{t} - {VESSEL_MAP.get(int(t), 'Other / Unknown')}" for t in numeric_types}
    
    # Desplegar selector de multiselección en la barra de controles
    selected_labels = st.sidebar.multiselect(
        "Filtrar por Tipo de Buque:", 
        options=list(dropdown_options.values()),
        default=list(dropdown_options.values())[:4]  # Inicializar con las primeras 4 opciones por defecto
    )
    
    # Mapear las etiquetas seleccionadas de vuelta a sus valores enteros originales para el SQL
    selected_types = [k for k, v in dropdown_options.items() if v in selected_labels]

except Exception as e:
    st.sidebar.error(f"Error al cargar tipos de buques: {e}")
    selected_types = []

# Control para ajustar el número máximo de registros a renderizar en el mapa interactivo
max_rows = st.sidebar.slider("Límite de tráfico en mapa:", min_value=1000, max_value=30000, value=10000, step=1000)


# ==========================================
# 4. CONSULTA DINÁMICA OPTIMIZADA A DOCKER
# ==========================================
def load_filtered_data(types, limit_rows):
    if not types:
        return pd.DataFrame()
    
    # Construir la sentencia SQL parametrizada con la cláusula WHERE IN
    types_str = ",".join([str(t) for t in types])
    query = f"""
        SELECT * FROM ais_ships 
        WHERE "VesselType" IN ({types_str}) 
        LIMIT {limit_rows};
    """
    df_result = pd.read_sql(query, engine)
    
    # Asignar la traducción textual de la categoría de buque directamente en memoria
    if not df_result.empty and "VesselType" in df_result.columns:
        df_result["VesselTypeName"] = df_result["VesselType"].astype(int).map(VESSEL_MAP).fillna("Other / Unknown")
        
    return df_result

# Ejecutar la consulta con un indicador visual de carga
with st.spinner("⚡ Consultando base de datos naval en Docker..."):
    df = load_filtered_data(selected_types, max_rows)


# ==========================================
# 5. RENDERIZADO DE LA INTERFAZ DE CONTROL
# ==========================================
if not df.empty:
    st.markdown("---")
    
    # --- INDICADORES CLAVE DE RENDIMIENTO (KPIs) ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Buques en Pantalla", value=f"{len(df):,}")
    
    with col2:
        # Evaluar la velocidad media operacional de los buques seleccionados (SOG)
        avg_speed = df["SOG"].mean() if "SOG" in df.columns else 0.0
        st.metric(label="Velocidad Media Flota", value=f"{avg_speed:.2f} Nudos")
        
    with col3:
        # Determinar de forma dinámica el nombre y velocidad de la unidad más veloz
        if "SOG" in df.columns and "VesselName" in df.columns:
            fastest_row = df.loc[df["SOG"].idxmax()]
            st.metric(label="Buque Más Rápido", value=str(fastest_row["VesselName"]), delta=f"{fastest_row['SOG']} Nds")
        else:
            st.metric(label="Buque Más Rápido", value="N/A")
            
    with col4:
        st.metric(label="Estado del Servidor", value="ONLINE", delta="Puerto 5433")

    # --- VISUALIZACIÓN CARTOGRÁFICA INTERACTIVA ---
    st.markdown("### 🗺️ Centro de Geolocalización de la Flota")
    
    # Mapear de manera flexible la ubicación de las columnas de coordenadas
    lat_col = next((c for c in df.columns if c.lower() in ['lat', 'latitude']), None)
    lon_col = next((c for c in df.columns if c.lower() in ['lon', 'longitude', 'long']), None)

    if lat_col and lon_col:
        fig_map = px.scatter_mapbox(
            df, 
            lat=lat_col, 
            lon=lon_col, 
            color="VesselTypeName",  # Segregar visualmente la leyenda por el nombre real de buque
            hover_name="VesselName" if "VesselName" in df.columns else None,
            hover_data=["SOG", "VesselType"] if "SOG" in df.columns else None,
            zoom=2, 
            mapbox_style="carto-positron",
            title="Posiciones Reportadas por Sistema AIS"
        )
        fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("⚠️ No se encontraron las columnas de coordenadas requeridas en la base de datos.")

    # --- ANÁLISIS ANALÍTICO AVANZADO ---
    st.markdown("### 📊 Análisis Avanzado de Operaciones")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### Volumen Operativo por Tipo de Buque")
        vessel_counts = df["VesselTypeName"].value_counts().reset_index()
        vessel_counts.columns = ["Tipo Buque", "Cantidad"]
        fig_bars = px.bar(vessel_counts, x="Tipo Buque", y="Cantidad", color="Tipo Buque", template="plotly_dark")
        st.plotly_chart(fig_bars, use_container_width=True)
        
    with col_chart2:
        st.markdown("#### Histograma Analítico de Velocidades (SOG)")
        if "SOG" in df.columns:
            fig_hist = px.histogram(df, x="SOG", nbins=30, color_discrete_sequence=['#10b981'], template="plotly_dark")
            st.plotly_chart(fig_hist, use_container_width=True)

    # --- TABLA DE REGISTROS TÉCNICOS ---
    st.markdown("### 📋 Inspección de Filas en Tiempo Real (Muestra M-100)")
    st.dataframe(df.head(100), use_container_width=True)

else:
    st.info("💡 Selecciona al menos un Tipo de Buque en el panel izquierdo para inicializar el radar.")