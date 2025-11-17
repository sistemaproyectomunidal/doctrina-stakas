from fastapi import FastAPI, Request
import os
from starlette.responses import JSONResponse
from shared.utils.logger import get_logger

app = FastAPI(title="api-gateway")
logger = get_logger("api-gateway")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "api-gateway"}

@app.post("/proxy")
async def proxy(request: Request):
    body = await request.json()
    # Example proxy route to other services
    return JSONResponse({"proxied": True, "body": body})
