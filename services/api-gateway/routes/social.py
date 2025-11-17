"""Social Service Routes"""

from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter(prefix="/api/social", tags=["Social Service"])

SOCIAL_BASE_URL = os.getenv("SOCIAL_API_URL", "http://social-service:8004")

@router.post("/publish")
async def publish_social(request: dict):
    """Publicar en redes sociales"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SOCIAL_BASE_URL}/publish",
                json=request
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/accounts")
async def list_accounts():
    """Listar cuentas conectadas"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SOCIAL_BASE_URL}/accounts")
            response.raise_for_status()
            return response.json()
    except:
        raise HTTPException(status_code=503, detail="Social service unavailable")
