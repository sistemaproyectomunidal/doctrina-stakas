"""E2B Monitor Routes"""

from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter(prefix="/api/e2b", tags=["E2B Monitor"])

E2B_BASE_URL = os.getenv("E2B_API_URL", "http://localhost:8001")

@router.post("/execute")
async def execute_code(request: dict):
    """Ejecutar código en E2B"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{E2B_BASE_URL}/api/execute",
                json=request
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/status/{execution_id}")
async def get_execution_status(execution_id: str):
    """Obtener estado de ejecución"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{E2B_BASE_URL}/api/status/{execution_id}"
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Execution not found")

@router.get("/health")
async def e2b_health():
    """Verificar estado de E2B"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{E2B_BASE_URL}/health")
            response.raise_for_status()
            return response.json()
    except:
        raise HTTPException(status_code=503, detail="E2B service unavailable")
