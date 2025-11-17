import streamlit as st
import requests

st.set_page_config(page_title="E2B Intelligent Dashboard", layout="wide")
st.title("🤖 E2B Intelligent Dashboard (v2 - Chatbot Mode)")

st.markdown("""
Este dashboard es la interfaz central para interactuar con el sistema E2B vía ChatBot inteligente.

**¿Cómo funciona?**
1. Escribe una instrucción en lenguaje natural
2. El sistema la interpreta y ejecuta
3. Ves el resultado en tiempo real

""")

# --- Sidebar con ejemplos ---
st.sidebar.header("📚 Ejemplos de Comandos")
st.sidebar.markdown("""
### 🚀 Deploy
- "Desplegar ml-engine en producción"
- "Lanzar social-automation en staging"
- "Deploy music-production en dev"

### 📊 Status
- "Estado de todos los servicios"
- "Check del monitor"
- "Status ml-engine"

### 📈 Métricas
- "Muestra las métricas"
- "Reportes del sistema"
- "Datos del sistema"

### ❓ Ayuda
- "Ayuda"
- "Qué puedo hacer"
- "Ejemplos"
""")

# --- Input Panel ---
st.header("1️⃣ Chat con el Sistema E2B")
user_input = st.text_input("Escribe tu instrucción aquí (ej: 'deploy ml-engine en prod'):", placeholder="Ej: Desplegar social-automation...")

if st.button("📤 Enviar instrucción"):
    if user_input.strip():
        # Llamar al Command Interpreter (chatbot)
        try:
            with st.spinner("🔄 Procesando instrucción..."):
                response = requests.post(
                    "http://localhost:8000/api/command",
                    json={"input": user_input},
                    timeout=10
                )
            
            if response.status_code == 200:
                result = response.json()
                
                # Mostrar acción interpretada
                st.success(f"✅ Acción: `{result['action']}`")
                
                # Mostrar mensaje del chatbot
                st.info(f"💬 {result['message']}")
                
                # Mostrar parámetros
                if result['params']:
                    st.json(result['params'])
                
                # Mostrar resultado del orquestador
                if result['orchestrator_result']:
                    st.subheader("📋 Respuesta del Sistema")
                    st.json(result['orchestrator_result'])
            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"❌ No se pudo conectar: {e}")
    else:
        st.warning("⚠️ Por favor, escribe una instrucción")

# --- Métricas Panel ---
st.header("2️⃣ Métricas del Sistema")
col1, col2, col3 = st.columns(3)
col1.metric("🟢 Sandboxes Activos", "5", "+2")
col2.metric("💰 Costo Diario ($)", "3.45", "-0.50")
col3.metric("⏱️ Uptime (%)", "99.9%", "+0.1%")

st.info("📝 Nota: Esta es la v2 con chatbot. Los paneles de métricas en tiempo real se conectarán en siguientes actualizaciones.")
