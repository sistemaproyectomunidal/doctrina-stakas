# 🎯 DOCTRINA-STAKAS - Guía de Navegación

Bienvenido a DOCTRINA-STAKAS, una plataforma de automatización inteligente construida con FastAPI, E2B Code Interpreter y Machine Learning.

## ⚡ Quick Start (30 segundos)

👉 **[START_HERE.md](START_HERE.md)** - Cómo ejecutar el proyecto en 30 segundos.

## 📚 Documentación Principal

- **[README.md](README.md)** - Descripción general del proyecto (v2.0)
- **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** - Resumen ejecutivo para stakeholders
- **[INDEX.md](INDEX.md)** - Índice completo y tabla de contenidos
- **[COMPLETE_SESSION_SUMMARY.md](COMPLETE_SESSION_SUMMARY.md)** - Resumen de la sesión de desarrollo
- **[MEJORAS-V2.md](MEJORAS-V2.md)** - Lista de mejoras implementadas v2.0

## 🏗️ Arquitectura y Técnica

- **[docs/architecture.md](docs/architecture.md)** - Arquitectura del sistema
- **[docs/security-guide.md](docs/security-guide.md)** - Guía de seguridad
- **[docs/deployment.md](docs/deployment.md)** - Guía de deployment
- **[docs/gpt5-prompts.md](docs/gpt5-prompts.md)** - Prompts originales

## ⭐ E2B Command Center (NEW)

- **[docs/gpt5-e2b-command-center.md](docs/gpt5-e2b-command-center.md)** - Documentación E2B Command Center
- **[services/e2b-monitor/](services/e2b-monitor/)** - API de monitoreo E2B (FastAPI, 420 líneas)
- **[services/e2b-monitor-dashboard/](services/e2b-monitor-dashboard/)** - Dashboard visual (Streamlit)

## 🤖 Auto-Deployer (NEW - ⭐⭐⭐ Recomendado)

- **[docs/gpt5-auto-deployer-prompt.md](docs/gpt5-auto-deployer-prompt.md)** - Prompt del Auto-Deployer completo
- **[docs/auto-deployment-example.md](docs/auto-deployment-example.md)** - Ejemplo completo de uso
- **[docs/implement-auto-deployer.md](docs/implement-auto-deployer.md)** - Guía de implementación
- **[docs/auto-deployer-summary.md](docs/auto-deployer-summary.md)** - Resumen ejecutivo

## 📊 Dashboard Maestro

- **[docs/dashboard-maestro-gpt5.md](docs/dashboard-maestro-gpt5.md)** - Concepto del Dashboard Maestro

## 🚀 Microservicios

- **[services/e2b-monitor/](services/e2b-monitor/)** - E2B Command Center API
- **[services/e2b-monitor-dashboard/](services/e2b-monitor-dashboard/)** - Dashboard Visual
- **[services/api-gateway/](services/api-gateway/)** - API Gateway principal
- **[services/ml-service/](services/ml-service/)** - Servicio de ML
- **[services/social-service/](services/social-service/)** - Servicio Social
- **[services/ads-service/](services/ads-service/)** - Servicio de Ads

## 📁 Estructura del Proyecto

```
doctrina-stakas/
├── docs/                                    # Documentación técnica
├── services/                                # Microservicios
│   ├── e2b-monitor/                        # ⭐ E2B Command Center
│   ├── e2b-monitor-dashboard/              # ⭐ Dashboard visual
│   ├── api-gateway/                        # API principal
│   ├── ml-service/                         # Servicio ML
│   ├── social-service/                     # Servicio Social
│   └── ads-service/                        # Servicio Ads
├── shared/                                  # Código compartido
├── e2b-templates/                          # Templates E2B
├── scripts/                                # Scripts útiles
└── [archivos de configuración]
```

## 🔧 Configuración Rápida

1. **Copia .env.example a .env:**
   ```bash
   cp .env.example .env
   ```

2. **Instala dependencias:**
   ```bash
   bash scripts/setup-all.sh
   ```

3. **Inicia con Docker:**
   ```bash
   docker-compose up --build
   ```

## 📖 Recomendaciones de Lectura

**Para nuevos usuarios:**
1. Empieza con [START_HERE.md](START_HERE.md)
2. Lee [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)
3. Explora [docs/architecture.md](docs/architecture.md)

**Para desarrolladores:**
1. [docs/gpt5-auto-deployer-prompt.md](docs/gpt5-auto-deployer-prompt.md)
2. [docs/implement-auto-deployer.md](docs/implement-auto-deployer.md)
3. [docs/architecture.md](docs/architecture.md)
4. [docs/security-guide.md](docs/security-guide.md)

**Para DevOps/Deployment:**
1. [docs/deployment.md](docs/deployment.md)
2. [docs/security-guide.md](docs/security-guide.md)

## 🤝 Contribuir

Por favor, revisa [MEJORAS-V2.md](MEJORAS-V2.md) para ver las áreas donde puedes contribuir.

## 📞 Soporte

Para preguntas o problemas, consulta la sección de Issues del repositorio.

---

**Última actualización:** 2025-11-17
