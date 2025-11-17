import streamlit as st
import requests

st.set_page_config(page_title="E2B Intelligent Dashboard", layout="wide")
st.title("🤖 E2B Intelligent Dashboard (v1)")

st.markdown("""
Este dashboard es la interfaz central para interactuar con el sistema E2B vía Command Interpreter (GPT-5/Claude) y el orquestador.

- Escribe instrucciones en lenguaje natural o JSON.
- Visualiza resultados, métricas y logs.
- Integra IA para interpretación y validación de comandos.
""")

# --- Input Panel ---
st.header("1️⃣ Instrucción para el sistema")
user_input = st.text_area("Escribe tu instrucción (natural o JSON):", height=100)

if st.button("Enviar instrucción"):
    # Simulación: Llama a un endpoint mock (a reemplazar por Command Interpreter real)
    try:
        response = requests.post(
            "http://localhost:8000/api/command",  # Cambiar por endpoint real
            json={"input": user_input},
            timeout=10
        )
        if response.status_code == 200:
            st.success("Respuesta del sistema:")
            st.json(response.json())
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"No se pudo conectar al backend: {e}")

# --- Métricas Panel ---
st.header("2️⃣ Métricas del sistema (placeholder)")
col1, col2, col3 = st.columns(3)
col1.metric("Sandboxes activos", "-")
col2.metric("Costo diario ($)", "-")
col3.metric("Uptime (%)", "-")

st.info("Esta es una versión inicial. Los paneles de métricas y logs se conectarán a los endpoints reales en siguientes fases.")
