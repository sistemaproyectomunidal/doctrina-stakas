# E2B Monitor API - Pydantic Models

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class ExecutionStatus(str, Enum):
    """Estados posibles de una ejecución"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class ExecutionRequest(BaseModel):
    """Solicitud para ejecutar código"""
    code: str = Field(..., description="Código Python a ejecutar")
    timeout: int = Field(default=30, ge=1, le=300)
    requirements: Optional[list[str]] = Field(default=None)
    metadata: Optional[dict] = Field(default=None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "print('Hello')\nresult = 2 + 2\nprint(result)",
                "timeout": 30,
                "requirements": ["numpy"],
                "metadata": {"user_id": "123"}
            }
        }


class ExecutionResult(BaseModel):
    """Resultado de una ejecución"""
    id: str = Field(..., description="ID único")
    status: ExecutionStatus
    output: Optional[str] = None
    error: Optional[str] = None
    duration: Optional[float] = None
    timestamp: datetime
    metadata: Optional[dict] = None


class ExecutionLog(BaseModel):
    """Log de una ejecución"""
    id: str
    timestamp: datetime
    level: str  # INFO, WARNING, ERROR
    message: str


class ServiceHealth(BaseModel):
    """Estado del servicio"""
    status: str
    uptime: float
    executions_total: int
    executions_running: int
    memory_usage: float


class CancelResponse(BaseModel):
    """Respuesta de cancelación"""
    message: str
    id: str


class ErrorResponse(BaseModel):
    """Respuesta de error"""
    detail: str
    code: int
