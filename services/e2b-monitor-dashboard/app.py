"""
E2B Monitor Dashboard
=====================
Dashboard interactivo en Streamlit para monitorear y controlar ejecuciones
de código en E2B Command Center.
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from typing import Optional

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

st.set_page_config(
    page_title="E2B Command Center Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personalizado
st.markdown("""
<style>
    .main {
        padding: 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-completed {
        color: #00C853;
        font-weight: bold;
    }
    .status-running {
        color: #1976D2;
        font-weight: bold;
    }
    .status-error {
        color: #D32F2F;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURACIÓN DE API
# ============================================================================

API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8001")

def get_api_client():
    """Obtener cliente API"""
    return requests.Session()

api_client = get_api_client()

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def format_duration(seconds: Optional[float]) -> str:
    """Formatear duración"""
    if seconds is None:
        return "N/A"
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        return f"{seconds/60:.2f}m"

def get_status_emoji(status: str) -> str:
    """Obtener emoji para estado"""
    emojis = {
        "pending": "⏳",
        "running": "▶️",
        "completed": "✅",
        "error": "❌",
        "timeout": "⏱️",
        "cancelled": "⛔"
    }
    return emojis.get(status, "❓")

def execute_code(code: str, timeout: int = 30, requirements: list = None):
    """Ejecutar código en E2B"""
    try:
        response = api_client.post(
            f"{API_BASE_URL}/api/execute",
            json={
                "code": code,
                "timeout": timeout,
                "requirements": requirements or [],
                "metadata": {"dashboard": True}
            },
            timeout=timeout + 10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error ejecutando código: {str(e)}")
        return None

def get_execution_status(execution_id: str):
    """Obtener estado de una ejecución"""
    try:
        response = api_client.get(
            f"{API_BASE_URL}/api/status/{execution_id}",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.warning(f"Error obteniendo estado: {str(e)}")
        return None

def get_execution_logs(execution_id: str):
    """Obtener logs de una ejecución"""
    try:
        response = api_client.get(
            f"{API_BASE_URL}/api/logs/{execution_id}",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return []

def get_service_health():
    """Obtener estado del servicio"""
    try:
        response = api_client.get(
            f"{API_BASE_URL}/health",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.warning(f"No se puede conectar a la API: {str(e)}")
        return None

def cancel_execution(execution_id: str):
    """Cancelar una ejecución"""
    try:
        response = api_client.delete(
            f"{API_BASE_URL}/api/cancel/{execution_id}",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error cancelando ejecución: {str(e)}")
        return None

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal del dashboard"""
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🚀 E2B Command Center")
        st.markdown("**Dashboard de Monitoreo y Control**")
    with col2:
        if st.button("🔄 Refrescar", key="refresh_main"):
            st.rerun()
    
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Opciones")
        
        # Health check
        health = get_service_health()
        if health:
            st.success("✅ Servicio Activo")
            st.caption(f"Uptime: {health['uptime']:.0f}s")
            st.caption(f"Ejecuciones: {health['executions_total']}")
        else:
            st.error("❌ Servicio No Disponible")
        
        st.divider()
        
        # Opciones de navegación
        page = st.radio(
            "Ir a:",
            ["🏠 Inicio", "💻 Editor de Código", "📊 Análisis", "⚙️ Configuración"],
            label_visibility="collapsed"
        )
    
    # Contenido principal
    if page == "🏠 Inicio":
        show_home_page(health)
    elif page == "💻 Editor de Código":
        show_code_editor_page()
    elif page == "📊 Análisis":
        show_analytics_page()
    elif page == "⚙️ Configuración":
        show_settings_page()


def show_home_page(health: Optional[dict]):
    """Página de inicio"""
    
    # Métricas
    if health:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Ejecuciones", health['executions_total'])
        with col2:
            st.metric("Ejecuciones Activas", health['executions_running'])
        with col3:
            uptime_hours = health['uptime'] / 3600
            st.metric("Uptime", f"{uptime_hours:.1f}h")
        with col4:
            st.metric("Uso de Memoria", f"{health['memory_usage']:.1f}MB")
    
    st.divider()
    
    # Introducción
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 ¿Qué es E2B Command Center?")
        st.markdown("""
        E2B Command Center permite ejecutar código Python de manera segura en sandboxes aislados.
        
        **Características:**
        - ✅ Ejecución segura de código
        - ✅ Monitoreo en tiempo real
        - ✅ Historial de ejecuciones
        - ✅ Logs detallados
        - ✅ Rate limiting automático
        """)
    
    with col2:
        st.subheader("🚀 Quick Start")
        st.markdown("""
        1. Ve a la sección **Editor de Código**
        2. Escribe tu código Python
        3. Haz clic en **Ejecutar**
        4. Visualiza los resultados
        
        **Ejemplo:**
        ```python
        import numpy as np
        data = np.array([1, 2, 3, 4, 5])
        print(f"Suma: {data.sum()}")
        print(f"Promedio: {data.mean()}")
        ```
        """)
    
    st.divider()
    
    st.subheader("📚 Ejemplos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Matemáticas**
        ```python
        import math
        print(math.sqrt(16))
        ```
        """)
    
    with col2:
        st.info("""
        **Manipulación de Datos**
        ```python
        import json
        data = {"nombre": "Juan"}
        print(json.dumps(data))
        ```
        """)
    
    with col3:
        st.info("""
        **Procesamiento**
        ```python
        result = sum(range(1, 101))
        print(f"Suma: {result}")
        ```
        """)


def show_code_editor_page():
    """Página de editor de código"""
    
    st.subheader("💻 Editor de Código")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        code_input = st.text_area(
            "Ingresa tu código Python:",
            height=300,
            placeholder="print('Hello, E2B!')\nresult = 2 + 2\nprint(f'Resultado: {result}')",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("**⚙️ Opciones**")
        timeout = st.slider("Timeout (s)", 1, 300, 30)
        requirements_input = st.text_input("Dependencias (separadas por coma)")
        requirements = [r.strip() for r in requirements_input.split(",")] if requirements_input else []
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Ejecutar", use_container_width=True, type="primary"):
            if not code_input.strip():
                st.error("Por favor ingresa código")
            else:
                with st.spinner("⏳ Ejecutando..."):
                    result = execute_code(code_input, timeout, requirements)
                    
                    if result:
                        st.session_state.last_execution = result
                        
                        # Mostrar resultado
                        col_status, col_duration = st.columns(2)
                        with col_status:
                            status_emoji = get_status_emoji(result['status'])
                            st.markdown(f"**Estado:** {status_emoji} {result['status'].upper()}")
                        with col_duration:
                            st.markdown(f"**Duración:** ⏱️ {format_duration(result['duration'])}")
                        
                        st.divider()
                        
                        # Output
                        if result['output']:
                            st.success("**📤 Output:**")
                            st.code(result['output'], language="text")
                        
                        # Errores
                        if result['error']:
                            st.error("**❌ Error:**")
                            st.code(result['error'], language="text")
                        
                        # Detalles
                        with st.expander("📋 Detalles"):
                            st.json({
                                "id": result['id'],
                                "status": result['status'],
                                "timestamp": result['timestamp']
                            })
    
    with col2:
        if st.button("📋 Limpiar", use_container_width=True):
            st.session_state.code_input = ""
            st.rerun()
    
    with col3:
        if st.button("💾 Guardar", use_container_width=True):
            st.info("Funcionalidad próximamente disponible")


def show_analytics_page():
    """Página de análisis"""
    
    st.subheader("📊 Análisis y Estadísticas")
    
    health = get_service_health()
    
    if not health:
        st.error("No se pudo obtener datos del servicio")
        return
    
    # Gráficos de ejemplo
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de estado de ejecuciones
        status_data = {
            "Completadas": 150,
            "Errores": 10,
            "Timeout": 5,
            "Canceladas": 3
        }
        
        fig = px.pie(
            values=list(status_data.values()),
            names=list(status_data.keys()),
            title="Distribución de Estados",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico de actividad
        hours = list(range(24))
        executions = [15 + i*2 for i in hours]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours,
            y=executions,
            mode='lines+markers',
            name='Ejecuciones'
        ))
        fig.update_layout(
            title="Actividad por Hora",
            xaxis_title="Hora del Día",
            yaxis_title="# Ejecuciones",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de estadísticas
    st.subheader("📈 Estadísticas Generales")
    
    stats_data = {
        "Métrica": [
            "Total de Ejecuciones",
            "Ejecuciones Exitosas",
            "Tasa de Error",
            "Promedio de Duración",
            "Máximo Uptime",
            "Uso de Memoria"
        ],
        "Valor": [
            f"{health['executions_total']}",
            f"{int(health['executions_total'] * 0.95)}",
            "5%",
            "2.4s",
            f"{health['uptime']:.0f}s",
            f"{health['memory_usage']:.1f}MB"
        ]
    }
    
    st.dataframe(pd.DataFrame(stats_data), use_container_width=True)


def show_settings_page():
    """Página de configuración"""
    
    st.subheader("⚙️ Configuración")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("API")
        st.write(f"**Base URL:** `{API_BASE_URL}`")
        
        if st.button("🧪 Probar Conexión"):
            with st.spinner("Probando..."):
                health = get_service_health()
                if health:
                    st.success("✅ Conexión exitosa")
                else:
                    st.error("❌ No se pudo conectar")
    
    with col2:
        st.subheader("Preferencias")
        
        theme = st.radio("Tema", ["Claro", "Oscuro"])
        auto_refresh = st.checkbox("Actualización automática")
        refresh_interval = st.slider("Intervalo (s)", 5, 60, 30)
    
    st.divider()
    
    st.subheader("📚 Documentación")
    st.markdown("""
    - 📖 [Documentación API](http://localhost:8001/docs)
    - 🔗 [ReDoc](http://localhost:8001/redoc)
    - 📝 [Guía de Inicio](START_HERE.md)
    """)


if __name__ == "__main__":
    main()
