"""ML Service Routes"""

from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter(prefix="/api/ml", tags=["ML Service"])

ML_BASE_URL = os.getenv("ML_API_URL", "http://ml-service:8003")

@router.post("/predict")
async def ml_predict(request: dict):
    """Hacer predicción ML"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ML_BASE_URL}/predict",
                json=request
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/models")
async def list_models():
    """Listar modelos disponibles"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ML_BASE_URL}/models")
            response.raise_for_status()
            return response.json()
    except:
        raise HTTPException(status_code=503, detail="ML service unavailable")
