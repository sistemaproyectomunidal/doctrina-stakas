# E2B Monitor API - Configuration

import os
from typing import Optional

class Settings:
    """Configuración de la aplicación"""
    
    # Aplicación
    APP_NAME: str = "E2B Command Center"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8001))
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"
    
    # E2B
    E2B_API_KEY: str = os.getenv("E2B_API_KEY", "")
    E2B_TIMEOUT: int = int(os.getenv("E2B_TIMEOUT", 30))
    
    # Límites
    MAX_EXECUTION_TIMEOUT: int = int(os.getenv("MAX_EXECUTION_TIMEOUT", 300))
    MAX_CONCURRENT_EXECUTIONS: int = int(os.getenv("MAX_CONCURRENT_EXECUTIONS", 10))
    MAX_CODE_LENGTH: int = int(os.getenv("MAX_CODE_LENGTH", 10000))
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", 60))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:8501,http://localhost:8000"
    ).split(",")
    
    # Base de Datos (opcional para sesiones persistentes)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")


settings = Settings()
