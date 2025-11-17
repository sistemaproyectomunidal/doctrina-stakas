"""Ads Service Routes"""

from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter(prefix="/api/ads", tags=["Ads Service"])

ADS_BASE_URL = os.getenv("ADS_API_URL", "http://ads-service:8005")

@router.post("/campaign")
async def create_campaign(request: dict):
    """Crear campaña publicitaria"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ADS_BASE_URL}/campaign",
                json=request
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/campaigns")
async def list_campaigns():
    """Listar campañas"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ADS_BASE_URL}/campaigns")
            response.raise_for_status()
            return response.json()
    except:
        raise HTTPException(status_code=503, detail="Ads service unavailable")
