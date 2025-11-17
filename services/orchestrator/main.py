from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Any, Dict
import httpx
import os

PAUSE_DEPLOYS = os.getenv("PAUSE_DEPLOYS", "false").lower() in ("1", "true", "yes")

app = FastAPI(title="Orchestrator API", version="0.1")

class OrchestratorRequest(BaseModel):
    action: str
    params: Dict[str, Any]

class OrchestratorResponse(BaseModel):
    result: Any
    message: str

# Map actions to microservice endpoints (mock URLs, adjust as needed)
SERVICE_ENDPOINTS = {
    # E2B Monitor
    "deploy_monitor": "http://localhost:8101/api/deploy",
    "status_monitor": "http://localhost:8101/api/status",
    # ML Engine
    "deploy_ml": "http://localhost:8102/api/deploy",
    "status_ml": "http://localhost:8102/api/status",
    # Social Automation
    "deploy_social": "http://localhost:8103/api/deploy",
    "status_social": "http://localhost:8103/api/status",
    # Music Production
    "deploy_music": "http://localhost:8104/api/deploy",
    "status_music": "http://localhost:8104/api/status",
}

@app.post("/api/orchestrate", response_model=OrchestratorResponse)
async def orchestrate(req: OrchestratorRequest):
    action = req.action
    params = req.params

    # Caso especial: deploy_service -> decidir endpoint por nombre de servicio
    if action == "deploy_service":
        # Respect global pause flag to avoid accidental deploys during testing
        if PAUSE_DEPLOYS:
            return OrchestratorResponse(result=None, message="Deploys are temporarily paused (PAUSE_DEPLOYS=true).")
        svc = params.get("service")
        if not svc:
            return OrchestratorResponse(result=None, message="Parámetro 'service' requerido para deploy_service.")
        # Mapear nombres de servicio a keys
        if svc in ("e2b-monitor", "monitor"):
            endpoint = SERVICE_ENDPOINTS.get("deploy_monitor")
        elif svc in ("ml-engine", "ml"):
            endpoint = SERVICE_ENDPOINTS.get("deploy_ml")
        elif svc in ("social-automation", "social"):
            endpoint = SERVICE_ENDPOINTS.get("deploy_social")
        elif svc in ("music-production", "music"):
            endpoint = SERVICE_ENDPOINTS.get("deploy_music")
        else:
            return OrchestratorResponse(result=None, message=f"Servicio '{svc}' desconocido para deploy.")

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(endpoint, json=params, timeout=15)
                return OrchestratorResponse(result=resp.json(), message=f"Deploy de '{svc}' ejecutado.")
        except Exception as e:
            return OrchestratorResponse(result=None, message=f"Error al orquestar deploy: {e}")

    # Caso especial: get_status -> puede pedir 'all' o servicio específico
    if action == "get_status":
        svc = params.get("service")
        results = {}
        try:
            async with httpx.AsyncClient() as client:
                if svc == "all" or svc is None:
                    # llamar a todos los status endpoints
                    for key in ["status_monitor", "status_ml", "status_social", "status_music"]:
                        ep = SERVICE_ENDPOINTS.get(key)
                        try:
                            r = await client.post(ep, json={"service": key}, timeout=10)
                            results[key] = r.json()
                        except Exception as e:
                            results[key] = {"error": str(e)}
                else:
                    # mapear servicio específico
                    if svc in ("e2b-monitor", "monitor"):
                        ep = SERVICE_ENDPOINTS.get("status_monitor")
                    elif svc in ("ml-engine", "ml"):
                        ep = SERVICE_ENDPOINTS.get("status_ml")
                    elif svc in ("social-automation", "social"):
                        ep = SERVICE_ENDPOINTS.get("status_social")
                    elif svc in ("music-production", "music"):
                        ep = SERVICE_ENDPOINTS.get("status_music")
                    else:
                        return OrchestratorResponse(result=None, message=f"Servicio '{svc}' desconocido para status.")
                    r = await client.post(ep, json={"service": svc}, timeout=10)
                    results[svc] = r.json()

            return OrchestratorResponse(result=results, message="Status aggregated.")
        except Exception as e:
            return OrchestratorResponse(result=None, message=f"Error al obtener status: {e}")

    # Fallback: acciones mapeadas directamente
    endpoint = SERVICE_ENDPOINTS.get(action)
    if not endpoint:
        return OrchestratorResponse(result=None, message=f"Acción '{action}' no soportada.")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(endpoint, json=params, timeout=10)
            return OrchestratorResponse(result=resp.json(), message=f"Acción '{action}' ejecutada correctamente.")
    except Exception as e:
        return OrchestratorResponse(result=None, message=f"Error al orquestar: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
