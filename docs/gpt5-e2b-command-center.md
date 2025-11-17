# 📚 E2B Command Center - Documentación Técnica

## 🎯 Introducción

E2B Command Center es un servicio FastAPI que permite ejecutar código Python de forma segura en sandboxes aislados. Proporciona una API RESTful completa y WebSocket para monitoreo en tiempo real.

**Tecnologías:**
- FastAPI 0.104+
- Python 3.11+
- E2B Code Interpreter
- Docker
- PostgreSQL (opcional)

## 🚀 Quick Start

### 1. Instalación Local

```bash
cd services/e2b-monitor
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Variables de Entorno

```bash
cp .env.example .env
# Edita .env con tus valores
```

### 3. Ejecutar

```bash
python main.py
```

O con uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### 4. Acceso

- **API Documentation:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc
- **Health Check:** http://localhost:8001/health

## 📡 API Endpoints

### Ejecución de Código

#### `POST /api/execute`

Ejecutar código Python en sandbox.

**Request:**
```json
{
  "code": "print('Hello, E2B!')\nresult = 2 + 2\nprint(result)",
  "timeout": 30,
  "requirements": ["numpy", "pandas"],
  "metadata": {"user_id": "123"}
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "output": "Hello, E2B!\n4",
  "error": null,
  "duration": 1.23,
  "timestamp": "2025-11-17T10:30:00Z",
  "metadata": {"user_id": "123"}
}
```

**Parámetros:**
- `code` (string, required): Código Python a ejecutar
- `timeout` (integer, 1-300, default: 30): Timeout en segundos
- `requirements` (array, optional): Dependencias pip
- `metadata` (object, optional): Datos adicionales

**Códigos de Estado:**
- `200 OK`: Ejecución completada
- `400 Bad Request`: Solicitud inválida
- `503 Service Unavailable`: Servicio no disponible

### Estado de Ejecución

#### `GET /api/status/{execution_id}`

Obtener estado de una ejecución en progreso.

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "output": "Parcial...",
  "error": null,
  "duration": null,
  "timestamp": "2025-11-17T10:30:00Z"
}
```

### Logs

#### `GET /api/logs/{execution_id}`

Obtener logs detallados de una ejecución.

**Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-11-17T10:30:00Z",
    "level": "INFO",
    "message": "Ejecución iniciada (timeout: 30s)"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-11-17T10:30:01Z",
    "level": "INFO",
    "message": "Ejecución completada en 1.23s"
  }
]
```

### Cancelación

#### `DELETE /api/cancel/{execution_id}`

Cancelar una ejecución en progreso.

**Response:**
```json
{
  "message": "Ejecución cancelada",
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### WebSocket Streaming

#### `WS /ws/stream/{execution_id}`

Conectar a WebSocket para recibir logs en tiempo real.

**JavaScript Example:**
```javascript
const ws = new WebSocket('ws://localhost:8001/ws/stream/550e8400-e29b-41d4-a716-446655440000');

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log(message);
  
  if (message.type === 'log') {
    console.log(`[${message.data.level}] ${message.data.message}`);
  } else if (message.type === 'completed') {
    console.log('Output:', message.data.output);
  }
};

ws.onerror = (error) => console.error('Error:', error);
ws.onclose = () => console.log('Desconectado');
```

### Health Check

#### `GET /health`

Verificar estado del servicio.

**Response:**
```json
{
  "status": "healthy",
  "uptime": 3600.5,
  "executions_total": 42,
  "executions_running": 2,
  "memory_usage": 125.5
}
```

## 🔧 Configuración

### Variables de Entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DEBUG` | `False` | Modo debug |
| `HOST` | `0.0.0.0` | Host del servidor |
| `PORT` | `8001` | Puerto del servidor |
| `E2B_API_KEY` | - | Clave API de E2B |
| `E2B_TIMEOUT` | `30` | Timeout por defecto |
| `MAX_EXECUTION_TIMEOUT` | `300` | Timeout máximo |
| `MAX_CONCURRENT_EXECUTIONS` | `10` | Máximo concurrente |
| `MAX_CODE_LENGTH` | `10000` | Longitud máxima de código |
| `RATE_LIMIT_ENABLED` | `True` | Habilitar rate limit |
| `RATE_LIMIT_PER_MINUTE` | `60` | Límite por minuto |
| `LOG_LEVEL` | `INFO` | Nivel de logging |
| `DATABASE_URL` | - | URL de base de datos |

### Docker

**Build:**
```bash
docker build -t e2b-monitor .
```

**Run:**
```bash
docker run -p 8001:8001 \
  -e E2B_API_KEY=your_key \
  e2b-monitor
```

**Docker Compose:**
```bash
docker-compose up e2b-monitor
```

## 🔒 Seguridad

### Sandboxing

- Código ejecutado en sandboxes aislados (E2B)
- Sin acceso al filesystem del host
- Sin acceso a red externa (configurable)
- Timeout automático

### Rate Limiting

- 60 requests/minuto por defecto
- Configurable vía `RATE_LIMIT_PER_MINUTE`
- HTTP 429 si se excede

### Validación

- Pydantic v2 con validación estricta
- Input validation en todos los endpoints
- Max code length: 10,000 caracteres

### Logging

- Auditoría de todas las ejecuciones
- Logs estructurados
- Integración con ELK/Datadog

## 📊 Monitoreo

### Métricas Disponibles

- Total de ejecuciones
- Ejecuciones activas
- Uptime del servicio
- Uso de memoria
- Duración promedio

### Integración con Prometheus

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'e2b-monitor'
    static_configs:
      - targets: ['localhost:8001']
```

## 🐛 Troubleshooting

### "Connection refused"

```bash
# Verificar que el servicio está corriendo
curl http://localhost:8001/health

# Iniciar en verbose mode
uvicorn main:app --log-level debug
```

### "Timeout exceeded"

Aumentar `MAX_EXECUTION_TIMEOUT` en `.env`:

```env
MAX_EXECUTION_TIMEOUT=600
```

### "Module not found"

Instalar dependencias con `requirements`:

```json
{
  "code": "import numpy",
  "requirements": ["numpy"]
}
```

## 📚 Ejemplos

### Python - Requests

```python
import requests
import json

# Ejecutar código
response = requests.post(
    'http://localhost:8001/api/execute',
    json={
        'code': '''
import math
result = math.sqrt(16)
print(f"Raíz cuadrada de 16: {result}")
        ''',
        'timeout': 30
    }
)

execution = response.json()
print(f"ID: {execution['id']}")
print(f"Status: {execution['status']}")
print(f"Output: {execution['output']}")
```

### cURL

```bash
# Ejecutar
curl -X POST http://localhost:8001/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(sum(range(1, 101)))",
    "timeout": 30
  }'

# Obtener estado
curl http://localhost:8001/api/status/{execution_id}

# Obtener logs
curl http://localhost:8001/api/logs/{execution_id}

# Cancelar
curl -X DELETE http://localhost:8001/api/cancel/{execution_id}
```

### JavaScript - Fetch

```javascript
// Ejecutar
const response = await fetch('http://localhost:8001/api/execute', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    code: `
import random
numbers = [random.randint(1, 100) for _ in range(5)]
print(f"Números: {numbers}")
    `,
    timeout: 30
  })
});

const execution = await response.json();
console.log(execution);

// Obtener estado
const statusResponse = await fetch(
  `http://localhost:8001/api/status/${execution.id}`
);
const status = await statusResponse.json();
console.log(status);
```

## 🚀 Deployment

### Railway

```bash
railway link
railway up
```

### Heroku

```bash
heroku create e2b-monitor
git push heroku main
```

### AWS (Elastic Beanstalk)

```bash
eb init
eb create
eb deploy
```

## 📞 Soporte

- **Issues:** GitHub Issues
- **Email:** support@sistemaproyectomunidal.com
- **Docs:** http://localhost:8001/docs

---

**Versión:** 1.0.0
**Última actualización:** 2025-11-17
