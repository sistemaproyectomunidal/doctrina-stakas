"""
E2B Command Center API
======================
FastAPI server para ejecutar código Python seguro en sandboxes E2B.

Proporciona endpoints RESTful y WebSocket para:
- Ejecución de código Python
- Monitoreo en tiempo real
- Gestión de recursos
- Auditoría y logging
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# MODELOS
# ============================================================================

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
    timeout: int = Field(default=30, ge=1, le=300, description="Timeout en segundos (1-300)")
    requirements: Optional[list[str]] = Field(default=None, description="Dependencias pip")
    metadata: Optional[dict] = Field(default=None, description="Datos adicionales")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "print('Hello, E2B!')\nresult = 2 + 2\nprint(f'2 + 2 = {result}')",
                "timeout": 30,
                "requirements": ["numpy", "pandas"],
                "metadata": {"user_id": "123", "project": "demo"}
            }
        }


class ExecutionResult(BaseModel):
    """Resultado de una ejecución"""
    id: str = Field(..., description="ID único de la ejecución")
    status: ExecutionStatus = Field(..., description="Estado de la ejecución")
    output: Optional[str] = Field(None, description="Output de stdout")
    error: Optional[str] = Field(None, description="Mensaje de error si aplica")
    duration: Optional[float] = Field(None, description="Duración en segundos")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")
    metadata: Optional[dict] = Field(None, description="Metadatos adicionales")


class ExecutionLog(BaseModel):
    """Log de una ejecución"""
    id: str
    timestamp: datetime
    level: str  # INFO, WARNING, ERROR
    message: str


class ServiceHealth(BaseModel):
    """Estado del servicio"""
    status: str = Field(..., description="Estado del servicio")
    uptime: float = Field(..., description="Uptime en segundos")
    executions_total: int = Field(..., description="Total de ejecuciones")
    executions_running: int = Field(..., description="Ejecuciones en progreso")
    memory_usage: float = Field(..., description="Uso de memoria en MB")


class DeployRequest(BaseModel):
    service: str
    env: str

class StatusRequest(BaseModel):
    service: str


# ============================================================================
# STORE DE EJECUCIONES (En memoria - para producción usar Redis)
# ============================================================================

class ExecutionStore:
    """Almacenamiento en memoria de ejecuciones"""
    
    def __init__(self):
        self.executions: dict[str, dict] = {}
        self.logs: dict[str, list[ExecutionLog]] = {}
        self.start_time = datetime.utcnow()
        self.total_executions = 0
    
    def create(self, code: str, timeout: int, requirements: Optional[list], metadata: Optional[dict]) -> str:
        """Crear una nueva ejecución"""
        exec_id = str(uuid.uuid4())
        self.executions[exec_id] = {
            "id": exec_id,
            "code": code,
            "timeout": timeout,
            "requirements": requirements or [],
            "metadata": metadata or {},
            "status": ExecutionStatus.PENDING,
            "output": "",
            "error": "",
            "start_time": None,
            "end_time": None,
            "duration": None,
        }
        self.logs[exec_id] = []
        self.total_executions += 1
        return exec_id
    
    def get(self, exec_id: str) -> Optional[dict]:
        """Obtener una ejecución"""
        return self.executions.get(exec_id)
    
    def update_status(self, exec_id: str, status: ExecutionStatus, **kwargs):
        """Actualizar estado de una ejecución"""
        if exec_id not in self.executions:
            return
        
        self.executions[exec_id]["status"] = status
        for key, value in kwargs.items():
            if key in self.executions[exec_id]:
                self.executions[exec_id][key] = value
    
    def add_log(self, exec_id: str, level: str, message: str):
        """Agregar un log"""
        if exec_id not in self.logs:
            self.logs[exec_id] = []
        self.logs[exec_id].append(ExecutionLog(
            id=exec_id,
            timestamp=datetime.utcnow(),
            level=level,
            message=message
        ))
    
    def get_logs(self, exec_id: str) -> list[ExecutionLog]:
        """Obtener logs de una ejecución"""
        return self.logs.get(exec_id, [])
    
    def get_health(self) -> dict:
        """Obtener estado del servicio"""
        running_count = sum(
            1 for e in self.executions.values()
            if e["status"] == ExecutionStatus.RUNNING
        )
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        
        return {
            "status": "healthy",
            "uptime": uptime,
            "executions_total": self.total_executions,
            "executions_running": running_count,
            "memory_usage": 0.0,  # Placeholder
        }


# ============================================================================
# APLICACIÓN FASTAPI
# ============================================================================

app = FastAPI(
    title="E2B Command Center",
    description="API para ejecutar código Python seguro en sandboxes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store de ejecuciones
store = ExecutionStore()


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/health", response_model=ServiceHealth)
async def health_check():
    """Verificar salud del servicio"""
    health = store.get_health()
    return ServiceHealth(**health)


@app.post("/api/execute", response_model=ExecutionResult)
async def execute_code(request: ExecutionRequest) -> ExecutionResult:
    """Ejecutar código Python en sandbox E2B
    
    Ejemplo:
    ```
    curl -X POST http://localhost:8001/api/execute \\
      -H "Content-Type: application/json" \\
      -d '{"code": "print(\\'Hello, E2B!\\')", "timeout": 30}'
    ```
    """
    # Crear ejecución
    exec_id = store.create(
        code=request.code,
        timeout=request.timeout,
        requirements=request.requirements,
        metadata=request.metadata
    )
    
    store.update_status(exec_id, ExecutionStatus.RUNNING, start_time=datetime.utcnow())
    store.add_log(exec_id, "INFO", f"Ejecución iniciada (timeout: {request.timeout}s)")
    
    logger.info(f"Executing code: {exec_id}")
    
    try:
        # Simulación de ejecución (En producción, usar E2B)
        # Para demostración, ejecutar código localmente con seguridad mejorada
        
        start = datetime.utcnow()
        output = ""
        error = ""
        
        try:
            # NOTA: En producción, usar E2B Code Interpreter
            # exec_result = await e2b_client.execute(request.code)
            # output = exec_result.output
            # error = exec_result.error
            
            # Simulación para demo
            import io
            import sys
            from contextlib import redirect_stdout, redirect_stderr
            
            # Capturar stdout/stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                # ADVERTENCIA: Esto es inseguro. En producción usar E2B sandbox
                try:
                    exec(request.code, {"__builtins__": {}})
                except Exception as e:
                    error = str(e)
            
            output = stdout_capture.getvalue()
            if not output and not error:
                output = "Ejecución completada sin output"
        
        except asyncio.TimeoutError:
            error = f"Ejecución excedió timeout de {request.timeout}s"
            store.update_status(exec_id, ExecutionStatus.TIMEOUT)
            store.add_log(exec_id, "ERROR", error)
        
        except Exception as e:
            error = f"Error en ejecución: {str(e)}"
            store.update_status(exec_id, ExecutionStatus.ERROR)
            store.add_log(exec_id, "ERROR", error)
        
        # Calcular duración
        duration = (datetime.utcnow() - start).total_seconds()
        
        # Actualizar resultado
        status = ExecutionStatus.ERROR if error else ExecutionStatus.COMPLETED
        store.update_status(
            exec_id,
            status=status,
            output=output,
            error=error,
            end_time=datetime.utcnow(),
            duration=duration
        )
        
        store.add_log(exec_id, "INFO", f"Ejecución completada en {duration:.2f}s")
        
    except Exception as e:
        logger.error(f"Error executing {exec_id}: {str(e)}")
        store.update_status(
            exec_id,
            ExecutionStatus.ERROR,
            error=str(e),
            end_time=datetime.utcnow()
        )
    
    # Retornar resultado
    exec_data = store.get(exec_id)
    return ExecutionResult(
        id=exec_id,
        status=exec_data["status"],
        output=exec_data["output"],
        error=exec_data["error"],
        duration=exec_data["duration"],
        timestamp=datetime.utcnow(),
        metadata=exec_data["metadata"]
    )


@app.get("/api/status/{execution_id}", response_model=ExecutionResult)
async def get_execution_status(execution_id: str) -> ExecutionResult:
    """Obtener estado de una ejecución
    
    Ejemplo:
    ```
    curl http://localhost:8001/api/status/{execution_id}
    ```
    """
    exec_data = store.get(execution_id)
    
    if not exec_data:
        raise HTTPException(status_code=404, detail="Ejecución no encontrada")
    
    return ExecutionResult(
        id=execution_id,
        status=exec_data["status"],
        output=exec_data["output"],
        error=exec_data["error"],
        duration=exec_data["duration"],
        timestamp=datetime.utcnow(),
        metadata=exec_data["metadata"]
    )


@app.get("/api/logs/{execution_id}", response_model=list[ExecutionLog])
async def get_execution_logs(execution_id: str) -> list[ExecutionLog]:
    """Obtener logs de una ejecución
    
    Ejemplo:
    ```
    curl http://localhost:8001/api/logs/{execution_id}
    ```
    """
    if not store.get(execution_id):
        raise HTTPException(status_code=404, detail="Ejecución no encontrada")
    
    return store.get_logs(execution_id)


@app.delete("/api/cancel/{execution_id}")
async def cancel_execution(execution_id: str) -> dict:
    """Cancelar una ejecución en progreso
    
    Ejemplo:
    ```
    curl -X DELETE http://localhost:8001/api/cancel/{execution_id}
    ```
    """
    exec_data = store.get(execution_id)
    
    if not exec_data:
        raise HTTPException(status_code=404, detail="Ejecución no encontrada")
    
    if exec_data["status"] != ExecutionStatus.RUNNING:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede cancelar ejecución en estado {exec_data['status']}"
        )
    
    store.update_status(execution_id, ExecutionStatus.CANCELLED)
    store.add_log(execution_id, "INFO", "Ejecución cancelada por usuario")
    
    return {"message": "Ejecución cancelada", "id": execution_id}


@app.websocket("/ws/stream/{execution_id}")
async def websocket_stream(websocket: WebSocket, execution_id: str):
    """WebSocket para streaming de logs en tiempo real
    
    Ejemplo en JavaScript:
    ```javascript
    const ws = new WebSocket('ws://localhost:8001/ws/stream/{execution_id}');
    ws.onmessage = (event) => console.log(JSON.parse(event.data));
    ```
    """
    await websocket.accept()
    
    if not store.get(execution_id):
        await websocket.close(code=404, reason="Ejecución no encontrada")
        return
    
    try:
        last_log_index = 0
        
        while True:
            # Enviar nuevos logs
            logs = store.get_logs(execution_id)
            if len(logs) > last_log_index:
                for log in logs[last_log_index:]:
                    await websocket.send_json({
                        "type": "log",
                        "data": {
                            "level": log.level,
                            "message": log.message,
                            "timestamp": log.timestamp.isoformat()
                        }
                    })
                last_log_index = len(logs)
            
            # Enviar estado
            exec_data = store.get(execution_id)
            await websocket.send_json({
                "type": "status",
                "data": {
                    "status": exec_data["status"],
                    "duration": exec_data["duration"]
                }
            })
            
            # Si terminó, enviar resultado final
            if exec_data["status"] in [
                ExecutionStatus.COMPLETED,
                ExecutionStatus.ERROR,
                ExecutionStatus.TIMEOUT,
                ExecutionStatus.CANCELLED
            ]:
                await websocket.send_json({
                    "type": "completed",
                    "data": {
                        "output": exec_data["output"],
                        "error": exec_data["error"]
                    }
                })
                break
            
            await asyncio.sleep(0.5)
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected for {execution_id}")


@app.post("/api/deploy")
async def deploy_service(req: DeployRequest = Body(...)):
    return {
        "status": "success",
        "service": req.service,
        "env": req.env,
        "message": f"Monitor {req.service} desplegado en {req.env}."
    }


@app.post("/api/status")
async def get_status(req: StatusRequest = Body(...)):
    return {
        "status": "running",
        "service": req.service,
        "uptime": "99.9%",
        "message": f"Estado de {req.service}: running."
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
