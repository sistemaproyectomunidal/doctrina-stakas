# 🤖 Auto-Deployer Prompt - GPT-5

## Sistema de Prompts para Generación Automática de Microservicios

**Propósito:** Generar servicios FastAPI completos y desplegables automáticamente.

### Prompt Principal (Usar en ChatGPT/Claude)

```
ERES UN EXPERTO EN DESARROLLO DE MICROSERVICIOS CON FASTAPI.

INSTRUCCIONES:
1. Leer descripción del servicio
2. Generar código FastAPI COMPLETO y FUNCIONAL
3. Incluir models.py, routes.py, main.py
4. Generar Dockerfile optimizado
5. Crear railway.json para deployment
6. Escribir tests con pytest
7. Crear GitHub Actions workflow
8. Agregar documentación OpenAPI

TECNOLOGÍAS:
- FastAPI 0.104+
- Python 3.11+
- Pydantic v2
- SQLAlchemy (si necesita DB)
- pytest para tests
- Docker + Docker Compose

REQUISITOS OBLIGATORIOS:
✅ Código producción-ready
✅ Type hints en todas las funciones
✅ Docstrings en español/inglés
✅ Error handling robusto
✅ CORS configurado
✅ Logging integrado
✅ Tests >80% coverage
✅ OpenAPI docs en /docs
✅ Health endpoint en /health

ESTRUCTURA DE RESPUESTA:
1. Descripción general
2. Endpoints principales
3. Código (main.py, models.py, routes.py)
4. Dockerfile
5. railway.json
6. requirements.txt
7. Tests (test_main.py)
8. Workflow (deploy.yml)
9. README.md

---

DESCRIPCIÓN DEL SERVICIO:
[INSERTA AQUÍ LA DESCRIPCIÓN]

---

COMENZAR GENERACIÓN:
```

### Prompt para Modelos

```
GENERA LOS MODELOS PYDANTIC PARA:
- Request models
- Response models
- Database models
- Error responses

Incluir:
- Field descriptions
- Validators
- JSON schema examples
- Documentación
```

### Prompt para Tests

```
GENERA TESTS PYTEST PARA ESTOS ENDPOINTS:
[LISTA DE ENDPOINTS]

Incluir:
- Unit tests
- Integration tests
- Error cases
- Edge cases
- 100% coverage
```

### Prompt para Deployment

```
GENERA CONFIGURACIÓN DE DEPLOYMENT PARA:
- Railway
- GitHub Actions
- SSL/TLS
- Health checks
- Monitoring
```

## 📋 Ejemplos de Prompts Específicos

### Ejemplo 1: API de Predicción ML

```
Crea un microservicio FastAPI que:
1. Acepte datos JSON con features
2. Use un modelo pre-entrenado de sklearn
3. Retorne predicciones
4. Almacene histórico en PostgreSQL
5. Incluya rate limiting
```

### Ejemplo 2: API de Processamiento de Archivos

```
Crea un microservicio que:
1. Acepte uploads de archivos PDF
2. Extraiga texto con pytesseract
3. Almacene en MinIO
4. Retorne análisis de sentimiento
5. Tenga WebSocket para tracking
```

### Ejemplo 3: API de Integración Social

```
Crea un microservicio que:
1. Conecte a Twitter/X API
2. Publique tweets programados
3. Trackee métricas de engagement
4. Almacene en base de datos
5. Tenga dashboard de analytics
```

## 🔄 Workflow de Uso

1. **Describo el servicio** en lenguaje natural
2. **GPT-5 genera** código completo
3. **Copio archivos** al directorio del servicio
4. **Ejecuto** `docker-compose up`
5. **Hago push** a GitHub
6. **GitHub Actions** ejecuta tests
7. **Railway** deploya automáticamente

## 📊 Parámetros de Calidad

- Type coverage: 100%
- Test coverage: >85%
- Documentation: Completa
- Performance: <200ms latencia
- Uptime: 99.9%
- Code quality: A+ (Codacy)

## 🚀 Resultado Esperado

Un servicio listo para producción con:
- ✅ Código funcional y testeado
- ✅ Dockerfile optimizado
- ✅ CI/CD automático
- ✅ Documentación completa
- ✅ Health checks
- ✅ Logging y monitoring
- ✅ Security best practices

## 📞 Próximos Pasos

1. Lee [auto-deployment-example.md](auto-deployment-example.md)
2. Usa el prompt principal
3. Implementa en [implement-auto-deployer.md](implement-auto-deployer.md)

---

**Versión:** 1.0.0
**Última actualización:** 2025-11-17
