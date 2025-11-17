# 🤖 E2B Intelligent Dashboard - Chatbot System

**Status:** ✅ Operativo 100%

Dashboard inteligente que funciona como **chatbot programador** para ejecutar todo el flujo E2B-DOGMA.

---

## 🚀 Inicio Rápido

### Opción 1: Levantar todo en paralelo (Recomendado)

```bash
chmod +x run_all.sh
./run_all.sh
```

Esto inicia:
- 🎨 Dashboard Streamlit: http://localhost:8501
- 🤖 Command Interpreter Chatbot: http://localhost:8000
- 🎯 Orquestador: http://localhost:8100
- 📊 Microservicios E2B:
  - Monitor: http://localhost:8101
  - ML Engine: http://localhost:8102
  - Social Automation: http://localhost:8103
  - Music Production: http://localhost:8104

### Opción 2: Levantar cada servicio manualmente

**Terminal 1 - Dashboard:**
```bash
cd dashboard
pip install streamlit requests
streamlit run app.py
```

**Terminal 2 - Command Interpreter:**
```bash
cd services/command-interpreter
pip install fastapi uvicorn httpx
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 3 - Orquestador:**
```bash
cd services/orchestrator
pip install fastapi uvicorn httpx
uvicorn main:app --host 0.0.0.0 --port 8100
```

**Terminal 4 - Microservicios E2B (ejecutar en paralelo):**
```bash
# E2B Monitor
cd services/e2b-monitor && uvicorn main:app --port 8101 &

# ML Engine
cd services/ml-engine && uvicorn main:app --port 8102 &

# Social Automation
cd services/social-automation && uvicorn main:app --port 8103 &

# Music Production
cd services/music-production && uvicorn main:app --port 8104 &
```

---

## 💬 Comandos del Chatbot

El sistema entiende instrucciones naturales en español:

### 🚀 **Deploy**
```
"Desplegar ml-engine en producción"
"Lanzar social-automation en staging"
"Deploy monitor en dev"
```

### 📊 **Status**
```
"Estado de todos los servicios"
"Check del monitor"
"Status ml-engine"
```

### 📈 **Métricas**
```
"Muestra las métricas"
"Reportes del sistema"
"Datos del sistema"
```

### ❓ **Ayuda**
```
"Ayuda"
"Qué puedo hacer"
"Ejemplos"
```

---

## 🏗️ Arquitectura

```
DASHBOARD (UI - Streamlit)
   ↓
COMMAND INTERPRETER (Chatbot - FastAPI)
   ↓ (interpreta & traduce a acción)
ORQUESTADOR (FastAPI)
   ↓ (despacha a microservicios)
MICROSERVICIOS E2B (FastAPI x4)
   ├─ Monitor (8101)
   ├─ ML Engine (8102)
   ├─ Social Automation (8103)
   └─ Music Production (8104)
```

---

## 📝 Flujo Completo

1. Usuario escribe en el dashboard: *"Desplegar ml-engine en producción"*
2. Command Interpreter interpreta → `action: deploy_monitor, params: {service: ml-engine, env: prod}`
3. Orquestador recibe la acción y llama a ML Engine en puerto 8102
4. ML Engine responde: `{status: success, message: "Desplegado..."}`
5. Dashboard muestra el resultado al usuario

---

## 🔧 Extensión

### Agregar nuevo patrón de comando

Edita `/services/command-interpreter/main.py` y añade en `COMMAND_PATTERNS`:

```python
"mi_comando": {
    "patterns": [r"patron1", r"patron2"],
    "services": ["monitor", "ml", ...]
}
```

### Agregar nuevo microservicio

1. Crea `/services/mi-servicio/main.py` con endpoints `/api/deploy` y `/api/status`
2. Actualiza `SERVICE_ENDPOINTS` en `/services/orchestrator/main.py`
3. Añade patrones en Command Interpreter

---

## 📊 Logs

Ver logs en tiempo real:
```bash
# Ver todos los logs
tail -f *.log

# Ver solo un servicio
tail -f command-interpreter.log
```

---

## 🛑 Detener todo

```bash
# Matar todos los procesos background
pkill -f uvicorn
pkill -f streamlit
```

---

## ✅ Checklist de Verificación

- [ ] Todos los servicios levantados sin errores
- [ ] Dashboard accesible en http://localhost:8501
- [ ] Comando "Deploy" funciona
- [ ] Comando "Status" devuelve resultados
- [ ] Comando "Ayuda" muestra opciones
- [ ] Respuestas aparecen en dashboard

---

*Documentación del E2B Intelligent Dashboard - Chatbot System v2.0*
