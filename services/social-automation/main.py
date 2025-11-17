from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="E2B Social Automation Service", version="0.1")

class DeployRequest(BaseModel):
    service: str
    env: str

class StatusRequest(BaseModel):
    service: str

@app.post("/api/deploy")
async def deploy_service(req: DeployRequest):
    return {
        "status": "success",
        "service": req.service,
        "env": req.env,
        "message": f"Social Automation {req.service} desplegado en {req.env}."
    }

@app.post("/api/status")
async def get_status(req: StatusRequest):
    return {
        "status": "running",
        "service": req.service,
        "uptime": "99.7%",
        "message": f"Estado de {req.service}: running."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8103)
