from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
import httpx
import re

app = FastAPI(title="Command Interpreter Chatbot API", version="1.0")

# Permitir CORS para dashboard local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    input: str

class CommandResponse(BaseModel):
    action: str
    params: Dict[str, Any]
    message: str
    orchestrator_result: Any = None

# Patrones de reconocimiento para el chatbot
COMMAND_PATTERNS = {
    "deploy": {
        "patterns": [r"deploy", r"desplegar", r"lanzar", r"start", r"iniciar"],
        "services": ["monitor", "ml", "social", "music"],
        "envs": ["prod", "staging", "dev"]
    },
    "status": {
        "patterns": [r"status", r"estado", r"cómo está", r"check", r"revisar"],
        "services": ["monitor", "ml", "social", "music", "all"]
    },
    "help": {
        "patterns": [r"help", r"ayuda", r"qué puedo", r"ejemplos", r"comandos"]
    },
    "metrics": {
        "patterns": [r"métricas", r"metrics", r"datos", r"estadísticas", r"reportes"]
    }
}

def parse_instruction(text: str) -> Dict[str, Any]:
    """Parsea una instrucción natural en lenguaje conversacional."""
    text_lower = text.lower()
    
    # Detectar intención
    for cmd, patterns_dict in COMMAND_PATTERNS.items():
        for pattern in patterns_dict["patterns"]:
            if re.search(pattern, text_lower):
                if cmd == "deploy":
                    service = "ml-engine"
                    for svc in patterns_dict["services"]:
                        if svc in text_lower:
                            service = svc if svc != "ml" else "ml-engine"
                            break
                    env = "prod"
                    for e in patterns_dict["envs"]:
                        if e in text_lower:
                            env = e
                            break
                    return {
                        "action": "deploy_monitor",
                        "params": {"service": service, "env": env},
                        "message": f"🚀 Desplegando **{service}** en **{env}**..."
                    }
                elif cmd == "status":
                    service = "all"
                    for svc in patterns_dict["services"]:
                        if svc in text_lower:
                            service = svc if svc != "ml" else "ml-engine"
                            break
                    return {
                        "action": "status_monitor",
                        "params": {"service": service},
                        "message": f"📊 Consultando estado de **{service}**..."
                    }
                elif cmd == "help":
                    return {
                        "action": "help",
                        "params": {},
                        "message": """
**Comandos disponibles:**

🚀 **Deploy**
  - "Desplegar ml-engine en producción"
  - "Lanzar social-automation en staging"
  - "Deploy monitor en dev"

📊 **Status**
  - "Estado de todos los servicios"
  - "Check del monitor"
  - "Status ml-engine"

📈 **Métricas**
  - "Muestra las métricas"
  - "Reportes del sistema"

❓ **Ayuda**
  - "Ayuda" o "Qué puedo hacer"
"""
                    }
                elif cmd == "metrics":
                    return {
                        "action": "metrics",
                        "params": {},
                        "message": "📈 Recuperando métricas del sistema E2B..."
                    }
    
    return {
        "action": "unknown",
        "params": {},
        "message": "❌ No entendí esa instrucción. Intenta: 'deploy', 'status', 'métricas' o escribe 'ayuda' para ver ejemplos."
    }

@app.post("/api/command", response_model=CommandResponse)
async def interpret_command(req: CommandRequest):
    """
    Chatbot inteligente que interpreta instrucciones naturales en contexto E2B-DOGMA.
    """
    # Paso 1: Parsear instrucción
    parsed = parse_instruction(req.input)
    action = parsed["action"]
    params = parsed["params"]
    message = parsed["message"]
    
    # Paso 2: Ejecutar acción si es válida
    orchestrator_result = None
    if action not in ["unknown", "help"]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://localhost:8100/api/orchestrate",
                    json={"action": action, "params": params},
                    timeout=15
                )
                orchestrator_result = resp.json()
        except Exception as e:
            orchestrator_result = {"error": str(e), "message": "⚠️ No se pudo conectar al orquestador."}
    
    return CommandResponse(
        action=action,
        params=params,
        message=message,
        orchestrator_result=orchestrator_result
    )

@app.get("/")
async def root():
    return {
        "name": "E2B Command Interpreter Chatbot",
        "version": "1.0",
        "endpoint": "/api/command",
        "example": "POST /api/command con {'input': 'Deploy ml-engine en prod'}"
    }

@app.get("/api/health")
async def health():
    """Health check."""
    return {"status": "ok", "service": "command-interpreter"}
