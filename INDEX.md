# 📑 INDEX - Tabla de Contenidos Completa

## 📄 Documentación de Inicio Rápido

| Archivo | Descripción | Tiempo |
|---------|-------------|--------|
| [00-README.md](00-README.md) | Guía de navegación principal | 5 min |
| [START_HERE.md](START_HERE.md) | Cómo ejecutar en 30 segundos | 2 min |
| [README.md](README.md) | Descripción completa del proyecto | 10 min |
| [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) | Resumen ejecutivo para stakeholders | 5 min |
| [MEJORAS-V2.md](MEJORAS-V2.md) | Lista de mejoras implementadas | 5 min |

## 🏗️ Documentación Técnica

### Arquitectura y Diseño
| Archivo | Propósito | Audiencia |
|---------|----------|-----------|
| [docs/architecture.md](docs/architecture.md) | Diseño del sistema completo | Arquitectos, Leads |
| [docs/gpt5-prompts.md](docs/gpt5-prompts.md) | Prompts GPT-5 originales | Developers |

### Deployment y Operaciones
| Archivo | Propósito | Audiencia |
|---------|----------|-----------|
| [docs/deployment.md](docs/deployment.md) | Guía de deployment completa | DevOps, Ops |
| [docs/security-guide.md](docs/security-guide.md) | Guía de seguridad | DevOps, Security |

### E2B Command Center (⭐⭐⭐)
| Archivo | Propósito | Audiencia |
|---------|----------|-----------|
| [docs/gpt5-e2b-command-center.md](docs/gpt5-e2b-command-center.md) | Documentación completa | Developers |
| [services/e2b-monitor/](services/e2b-monitor/) | API Implementation | Developers |
| [services/e2b-monitor-dashboard/](services/e2b-monitor-dashboard/) | Dashboard Visual | All Users |

### Auto-Deployer (⭐⭐⭐)
| Archivo | Propósito | Audiencia |
|---------|----------|-----------|
| [docs/gpt5-auto-deployer-prompt.md](docs/gpt5-auto-deployer-prompt.md) | Prompt completo del Auto-Deployer | AI Users, Prompt Engineers |
| [docs/auto-deployment-example.md](docs/auto-deployment-example.md) | Ejemplo completo paso a paso | Developers |
| [docs/implement-auto-deployer.md](docs/implement-auto-deployer.md) | Guía de implementación | Developers |
| [docs/auto-deployer-summary.md](docs/auto-deployer-summary.md) | Resumen ejecutivo | Leads, Stakeholders |

### Dashboard Maestro
| Archivo | Propósito | Audiencia |
|---------|----------|-----------|
| [docs/dashboard-maestro-gpt5.md](docs/dashboard-maestro-gpt5.md) | Concepto y especificaciones | Product, Developers |

## 🔧 Configuración

| Archivo | Propósito |
|---------|----------|
| [.env.example](.env.example) | Variables de entorno de ejemplo |
| [.gitignore](.gitignore) | Archivos ignorados por Git |
| [requirements.txt](requirements.txt) | Dependencias Python principales |
| [docker-compose.yml](docker-compose.yml) | Configuración Docker Compose |

## 🚀 Servicios (services/)

### E2B Command Center (NEW)
```
services/e2b-monitor/
├── main.py                  # API FastAPI (420 líneas)
├── models.py                # Modelos Pydantic
├── config.py                # Configuración
├── requirements.txt         # Dependencias
├── Dockerfile               # Imagen Docker
├── railway.json             # Config Railway
└── .env.example             # Ejemplo de env
```

**Stack:** FastAPI, E2B Code Interpreter, Async Python
**Función:** Ejecutar código Python en sandboxes seguros

### E2B Monitor Dashboard (NEW)
```
services/e2b-monitor-dashboard/
├── app.py                   # Dashboard Streamlit (350 líneas)
├── requirements.txt         # streamlit, plotly, pandas
├── Dockerfile               # Imagen Docker
├── railway.json             # Config Railway
└── .streamlit/
    └── secrets.toml.example
```

**Stack:** Streamlit, Plotly, Pandas
**Función:** Visualizar y controlar ejecuciones en tiempo real

### API Gateway
```
services/api-gateway/
├── main.py                  # FastAPI principal
├── routes/
│   ├── __init__.py
│   ├── e2b.py              # Rutas E2B
│   ├── ml.py               # Rutas ML
│   ├── social.py           # Rutas Social
│   └── ads.py              # Rutas Ads
├── requirements.txt
├── Dockerfile
└── railway.json
```

**Stack:** FastAPI, Security, Rate Limiting
**Función:** Enrutamiento centralizado y seguridad

### ML Service
```
services/ml-service/
├── main.py                  # FastAPI ML
├── models/                  # Modelos pre-entrenados
├── requirements.txt
├── Dockerfile
└── railway.json
```

**Stack:** FastAPI, scikit-learn, TensorFlow
**Función:** Predicciones y análisis

### Social Service
```
services/social-service/
├── main.py                  # FastAPI Social
├── providers/               # Integraciones
├── requirements.txt
├── Dockerfile
└── railway.json
```

**Stack:** FastAPI, Social APIs
**Función:** Gestión de redes sociales

### Ads Service
```
services/ads-service/
├── main.py                  # FastAPI Ads
├── campaigns/               # Gestión de campañas
├── requirements.txt
├── Dockerfile
└── railway.json
```

**Stack:** FastAPI, Ad Services
**Función:** Gestión de publicidad

## 📚 Código Compartido (shared/)

| Carpeta | Contenido |
|---------|-----------|
| shared/database/ | Modelos ORM, migraciones |
| shared/storage/ | Cliente MinIO, utilidades |
| shared/utils/ | Funciones reutilizables |

## 🎯 Templates E2B (e2b-templates/)

| Template | Propósito |
|----------|----------|
| e2b-templates/devops/ | DevOps automation |
| e2b-templates/ml-engine/ | ML pipelines |
| e2b-templates/music-production/ | Producción musical |
| e2b-templates/social-automation/ | Automatización social |

## 🔨 Scripts (scripts/)

| Script | Propósito |
|--------|----------|
| scripts/setup-all.sh | Instalación completa |
| scripts/clean-secrets.sh | Limpieza de secretos |

## 📊 Resumen de Sesiones

| Archivo | Descripción |
|---------|------------|
| [COMPLETE_SESSION_SUMMARY.md](COMPLETE_SESSION_SUMMARY.md) | Resumen técnico completo |

## 🗺️ Mapa de Navegación Recomendada

### 👤 Usuario Nuevo
1. [START_HERE.md](START_HERE.md) (2 min)
2. [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) (5 min)
3. [docs/architecture.md](docs/architecture.md) (15 min)

### 👨‍💻 Desarrollador
1. [docs/architecture.md](docs/architecture.md)
2. [docs/gpt5-auto-deployer-prompt.md](docs/gpt5-auto-deployer-prompt.md)
3. [docs/implement-auto-deployer.md](docs/implement-auto-deployer.md)
4. [services/e2b-monitor/main.py](services/e2b-monitor/main.py)

### 🏗️ Arquitecto
1. [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)
2. [docs/architecture.md](docs/architecture.md)
3. [docs/security-guide.md](docs/security-guide.md)

### 🚀 DevOps/SRE
1. [docs/deployment.md](docs/deployment.md)
2. [docs/security-guide.md](docs/security-guide.md)
3. [docker-compose.yml](docker-compose.yml)

### 📊 Product Manager
1. [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)
2. [MEJORAS-V2.md](MEJORAS-V2.md)
3. [docs/dashboard-maestro-gpt5.md](docs/dashboard-maestro-gpt5.md)

## 📞 Referencias Rápidas

- **API Docs:** http://localhost:8000/docs (una vez ejecutando)
- **Dashboard:** http://localhost:8501
- **E2B Monitor:** http://localhost:8001/docs
- **Código Fuente:** `/workspaces/doctrina-stakas`

---

**Última actualización:** 2025-11-17
**Versión:** 2.0.0
