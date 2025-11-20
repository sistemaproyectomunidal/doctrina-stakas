# Stakazo - Orquestador AI API

API para el Orquestador del Sistema Maestro de IA. Maneja uploads de videos, jobs de procesamiento, clips, campañas y la integración con plataformas sociales.

## 🚀 Inicio Rápido

### Opción A: Con Docker (Recomendado)

```bash
# Iniciar PostgreSQL en Docker y backend localmente
./dev-start.sh

# O con make
make dev
```

**Acceder a:**
- **API Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050 (admin@stakazo.local / admin)

### Opción B: Desarrollo con SQLite (Fallback)

```bash
# Si Docker no está disponible, el backend usa SQLite automáticamente
cd backend
source ../venv/bin/activate
uvicorn main:app --reload
```

### 2. Inicializar Base de Datos

```bash
# Aplicar migraciones
cd backend
alembic upgrade head

# O con make
make migrate
```

### 3. Explorar la API

- **API Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Debug Endpoints**: http://localhost:8000/debug/

## 📚 Comandos Disponibles

```bash
make help           # Muestra todos los comandos disponibles
make dev            # Inicia backend y postgres
make api            # Inicia solo el backend en modo reload (local)
make db             # Inicia solo PostgreSQL
make init-db        # Inicializa BD con schema y datos
make migrate        # Aplica migraciones
make migrate-create # Crea nueva migración
make stop           # Detiene todos los servicios
make logs           # Muestra logs
make clean          # Limpia contenedores y cache
make test           # Ejecuta tests
make build          # Reconstruye imágenes Docker
```

## 📁 Estructura del Proyecto

```
stakazo/
├── .devcontainer/          # Configuración Dev Container
│   ├── devcontainer.json   # Python 3.11 + Node 20 + Docker in Docker
│   ├── Dockerfile
│   └── post-create.sh      # Auto-setup en Codespaces
├── backend/                # FastAPI Backend
│   ├── app/
│   │   ├── api/           # Endpoints
│   │   │   ├── upload.py        # POST /upload
│   │   │   ├── jobs.py          # Jobs endpoints
│   │   │   ├── clips.py         # Clips endpoints
│   │   │   ├── campaigns.py     # Campaigns
│   │   │   ├── rules.py         # Platform rules
│   │   │   ├── confirm_publish.py
│   │   │   └── webhooks.py      # Instagram webhooks
│   │   ├── models/
│   │   │   ├── schemas.py       # Pydantic models
│   │   │   └── database.py      # SQLAlchemy models
│   │   ├── core/
│   │   │   ├── config.py        # Settings
│   │   │   └── database.py      # DB connection
│   │   ├── db/
│   │   │   └── init_db.py       # DB initialization
│   │   └── main.py              # FastAPI app
│   ├── alembic/                 # Database migrations
│   ├── main.py                  # Entry point
│   ├── Dockerfile
│   └── requirements.txt
├── clients/                # Generated API clients
│   ├── python/            # Python client
│   └── typescript-axios/  # TypeScript client
├── openapi/               # OpenAPI specification
│   └── orquestador_openapi.yaml
├── docker-compose.yml
├── Makefile
└── README.md
```

## 🔌 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/upload` | Upload video file |
| POST | `/jobs` | Create processing job |
| GET | `/jobs` | List all jobs |
| GET | `/jobs/{id}` | Get job details |
| GET | `/clips` | List clips |
| POST | `/clips/{id}/variants` | Generate clip variants |
| POST | `/confirm_publish` | Confirm publishing |
| POST | `/webhook/instagram` | Instagram webhook |
| POST | `/campaigns` | Create campaign |
| GET | `/campaigns` | List campaigns |
| GET | `/rules` | Get platform rules |
| POST | `/rules` | Propose rule changes |

## 🗄️ Database Schema

### Tablas Principales

- **video_assets**: Videos subidos
- **clips**: Clips extraídos de videos
- **clip_variants**: Variantes optimizadas por plataforma
- **jobs**: Tareas de procesamiento
- **campaigns**: Campañas publicitarias
- **platform_rules**: Reglas específicas por plataforma
- **publications**: Registro de publicaciones

### Relaciones

- `VideoAsset` → muchos `Clips`
- `Clip` → muchas `ClipVariants`
- `Clip` → muchos `Jobs`
- `Clip` → muchas `Campaigns`
- `Clip` → muchas `Publications`

## 🔧 Configuración

### Variables de Entorno

El archivo `.env` se genera automáticamente desde `.env.example`. Las variables principales:

```bash
# Database Configuration
# PostgreSQL (recomendado)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/stakazo_db
# SQLite (fallback para desarrollo sin Docker)
# DATABASE_URL=sqlite+aiosqlite:///./stakazo.db

# Security
SECRET_KEY=dev-secret-key-change-in-production

# Worker Configuration  
WORKER_ENABLED=false
WORKER_POLL_INTERVAL=2
MAX_JOB_RETRIES=3

# Storage
VIDEO_STORAGE_DIR=storage/videos

# Debug (disable in production)
DEBUG_ENDPOINTS_ENABLED=true
```

### Database Connection

El backend detecta automáticamente el entorno:

```python
# Con Docker: Lee DATABASE_URL desde .env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/stakazo_db

# Sin Docker: Fallback a SQLite
DATABASE_URL=sqlite+aiosqlite:///./stakazo.db
```

**Nota**: PostgreSQL requiere Docker. Si Docker no está disponible, el sistema usa SQLite automáticamente.

## 🧪 Testing

```bash
# Ejecutar todos los tests
make test

# Ejecutar tests específicos
cd backend && pytest tests/test_jobs.py -v
```

## 🐳 Docker

### Arquitectura

- **PostgreSQL**: Corre en Docker (puerto 5432)
- **Backend**: Corre localmente para desarrollo rápido
- **pgAdmin**: Opcional, interfaz web para gestionar PostgreSQL (puerto 5050)

### Scripts de Desarrollo

```bash
# Iniciar servicios
./dev-start.sh         # Inicia PostgreSQL + Backend con migraciones

# Detener servicios  
./dev-stop.sh          # Para todos los contenedores
```

### Servicios Docker

```bash
# Ver servicios activos
docker compose ps

# Logs de PostgreSQL
docker compose logs postgres -f

# Acceder a psql
docker compose exec postgres psql -U postgres -d stakazo_db
```

### Volúmenes

- `postgres_data`: Datos persistentes de PostgreSQL
- `pgadmin_data`: Configuración de pgAdmin

## 🔄 Migrations con Alembic

```bash
# Crear nueva migración (auto-detecta cambios)
make migrate-create MSG="add user table"

# Aplicar migraciones
make migrate

# Ver historial
cd backend && alembic history

# Rollback
cd backend && alembic downgrade -1
```

## 🧑‍💻 Desarrollo

### Filosofía de Desarrollo

El proyecto usa un enfoque híbrido:
- **PostgreSQL en Docker**: Base de datos consistente y fácil de gestionar
- **Backend local**: Desarrollo rápido con hot-reload sin overhead de Docker
- **SQLite fallback**: Desarrollo sin dependencias cuando Docker no está disponible

### Setup Inicial

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 2. Instalar dependencias
pip install -r backend/requirements.txt

# 3. Configurar variables de entorno
cd backend
cp .env.example .env

# 4. Iniciar desarrollo
cd ..
./dev-start.sh
```

### Flujo de Trabajo Diario

```bash
# Iniciar servicios
./dev-start.sh

# El script automáticamente:
# 1. Inicia PostgreSQL en Docker (si está disponible)
# 2. Espera a que esté listo
# 3. Ejecuta migraciones
# 4. Inicia backend con hot-reload

# Detener al finalizar
Ctrl+C                    # Para el backend
./dev-stop.sh            # Para PostgreSQL
```

### Dev Container (Codespaces)

El proyecto está configurado con Dev Container que incluye:

- Python 3.11
- Node 20  
- Docker in Docker
- Extensiones VS Code: Python, FastAPI, Docker, YAML
- Auto-instalación de dependencias al crear el Codespace

**Limitación en Codespaces**: Docker puede no estar disponible. El sistema detecta esto y usa SQLite automáticamente.

## 📦 Clientes Generados

### Python Client

```python
from orquestador_api_client import Client
from orquestador_api_client.api.default import post_jobs
from orquestador_api_client.models import JobCreate

client = Client(base_url="http://localhost:8000")

job = post_jobs.sync(
    client=client,
    json_body=JobCreate(
        job_type="process",
        clip_id="uuid-here"
    )
)
```

### TypeScript Client

```typescript
import { DefaultService } from './clients/typescript-axios';

const campaign = await DefaultService.postCampaigns({
  name: "Holiday Campaign",
  clip_id: "uuid-here",
  budget_cents: 100000
});
```

## 🚢 Deployment

### Railway / Render

1. Conectar repositorio
2. Configurar variables de entorno
3. Agregar PostgreSQL addon
4. Deploy automático en cada push a `main`

### Environment Variables para Producción

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
SECRET_KEY=<generate-secure-key>
UPLOAD_DIR=/app/uploads
MAX_UPLOAD_SIZE=524288000
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

## 📝 Licencia

Proyecto privado - Sistema Proyecto Mundial

---

**Desarrollado con** ❤️ **usando FastAPI + PostgreSQL + Docker**


---

## ?? Configuraci�n para Windows

Este proyecto soporta desarrollo en **Windows sin Docker** usando SQLite.

Ver gu�a completa: **[README_WINDOWS.md](README_WINDOWS.md)**

### Inicio R�pido Windows

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-windows.txt
.\run.ps1
```

**Diferencias Windows:**
- Base de datos: SQLite (`stakazo.db`)
- Sin Docker requerido
- Driver: `aiosqlite` (pure Python, sin compilaci�n)
- Dependencias optimizadas en `requirements-windows.txt`

---
