from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI(title="Command Interpreter API", version="0.1")

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


import httpx
from .gpt_client import get_gpt5_client
import os

@app.post("/api/command", response_model=CommandResponse)
async def interpret_command(req: CommandRequest):
    """
    Interpreta la instrucción y ejecuta la acción vía orquestador.
    """
    # Paso 1: intentar interpretar con GPT-5 si está configurado
    gpt = get_gpt5_client()
    action = "unknown"
    params = {}
    message = "No se pudo interpretar la instrucción."
    orchestrator_result = None

    if gpt is not None:
        try:
            system_prompt = os.getenv("COMMAND_INTERPRETER_SYSTEM_PROMPT")
            out = await gpt.generate_action(req.input, system_prompt=system_prompt)
            # Normalizar salida esperada
            action = out.get("action", "unknown")
            params = out.get("params", {}) or {}
            message = out.get("message", "Interpretación generada por GPT-5.")
        except Exception as e:
            # Fall back a mock si falla la llamada a GPT-5
            message = f"Error GPT-5: {e}. Usando interpretación mock."

    if gpt is None or action == "unknown":
        # Mock simple: si la instrucción contiene "deploy", responde con acción de deploy
        txt = req.input.lower()
        if "deploy" in txt:
            action = "deploy_service"
            params = {"service": "ml-engine", "env": "prod"}
            message = "Desplegando servicio ml-engine en producción."
        elif "status" in txt:
            action = "get_status"
            params = {"service": "all"}
            message = "Consultando estado de todos los servicios."

    # Paso 2: Llamar al orquestador si la acción es conocida
    if action != "unknown":
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://localhost:8100/api/orchestrate",
                    json={"action": action, "params": params},
                    timeout=15,
                )
                orchestrator_result = resp.json()
        except Exception as e:
            orchestrator_result = {"error": str(e)}

    return CommandResponse(
        action=action,
        params=params,
        message=message,
        orchestrator_result=orchestrator_result,
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
