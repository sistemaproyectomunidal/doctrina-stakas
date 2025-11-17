from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from starlette.responses import JSONResponse
from shared.utils.logger import get_logger

# Import route modules
from routes import e2b, ml, social, ads

app = FastAPI(
    title="API Gateway",
    description="API Gateway centralizado para DOCTRINA-STAKAS",
    version="2.0.0"
)

logger = get_logger("api-gateway")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(e2b.router)
app.include_router(ml.router)
app.include_router(social.router)
app.include_router(ads.router)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "2.0.0"
    }

@app.get("/")
async def root():
    return {
        "service": "DOCTRINA-STAKAS API Gateway",
        "version": "2.0.0",
        "docs": "/docs",
        "endpoints": [
            "/api/e2b - E2B Command Center",
            "/api/ml - ML Service",
            "/api/social - Social Service",
            "/api/ads - Ads Service"
        ]
    }

@app.post("/proxy")
async def proxy(request: Request):
    """Legacy proxy endpoint"""
    body = await request.json()
    return JSONResponse({"proxied": True, "body": body})
