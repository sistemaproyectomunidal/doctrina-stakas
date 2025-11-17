# 🔒 Security Guide - DOCTRINA-STAKAS

## 🛡️ Introducción

Esta guía cubre las mejores prácticas de seguridad para DOCTRINA-STAKAS.

## 🔐 Secrets Management

### Variables de Entorno

**NUNCA** comitees secretos en Git:

```bash
# ❌ MAL
DATABASE_PASSWORD=my_secure_password

# ✅ BIEN
# En .env (no comiteado)
DATABASE_PASSWORD=${DATABASE_PASSWORD}
```

### .gitignore

El proyecto incluye `.gitignore` que excluye:
```
.env
.env.local
.env.*.local
*.key
*.pem
secrets/
```

### Limpiar Secretos

```bash
bash scripts/clean-secrets.sh
```

## 🔑 API Security

### Authentication

DOCTRINA-STAKAS usa OAuth2 con JWT tokens.

**Setup:**

1. Generar clave secreta:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. Setear en `.env`:
```env
SECRET_KEY=your_generated_key
ALGORITHM=HS256
```

### Rate Limiting

- 60 requests/minuto por defecto
- Configurable por endpoint
- HTTP 429 si se excede

**Configuración:**

```env
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60
```

## 🔄 Transport Security

### TLS/SSL

**En Producción:**

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

**Redirect HTTP a HTTPS:**

```nginx
server {
    listen 80;
    return 301 https://$server_name$request_uri;
}
```

## 📊 CORS Configuration

### Allowed Origins

**Desarrollo:**
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8501,http://localhost:8000
```

**Producción:**
```env
CORS_ORIGINS=https://app.example.com,https://dashboard.example.com
```

## 🐳 Container Security

### Image Scanning

```bash
docker scan e2b-monitor
docker scan e2b-monitor-dashboard
```

### Base Images

Usar imágenes oficiales minimales:

```dockerfile
# ✅ BIEN
FROM python:3.11-slim

# ❌ MAL
FROM python:3.11  # Más grande, más vulnerabilidades
```

### Non-root User

```dockerfile
RUN useradd -m appuser
USER appuser
```

## 🗄️ Database Security

### Connection

**NUNCA** hardcodees credenciales:

```python
# ❌ MAL
DATABASE_URL = "postgresql://user:password@db:5432/mydb"

# ✅ BIEN
DATABASE_URL = os.getenv("DATABASE_URL")
```

### Queries

Siempre usar parameterized queries:

```python
# ✅ BIEN
await db.execute(
    "SELECT * FROM users WHERE email = ?",
    (email,)
)

# ❌ MAL
await db.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

## 🔍 Input Validation

### Pydantic Strict Mode

```python
from pydantic import BaseModel, Field

class ExecutionRequest(BaseModel):
    code: str = Field(..., max_length=10000)
    timeout: int = Field(..., ge=1, le=300)
    
    class Config:
        # Modo estricto
        validate_assignment = True
        use_enum_values = True
```

### File Upload

```python
# Validar tipo de archivo
ALLOWED_EXTENSIONS = {'py', 'txt', 'json'}

def validate_file(filename: str):
    if '.' not in filename:
        raise ValueError("Invalid file")
    ext = filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extension {ext} not allowed")
```

## 🛡️ Code Execution Security

### E2B Sandboxing

```python
# Ejecutar en sandbox seguro
result = await e2b_client.execute(code)

# Características:
# - Filesystem aislado
# - Sin acceso a red
# - Timeout automático
# - Limpieza de recursos
```

### Whitelist de Módulos

```python
ALLOWED_MODULES = {
    'math',
    'json',
    'random',
    'datetime',
    'collections',
}

def validate_imports(code: str):
    for module in ALLOWED_MODULES:
        if f'import {module}' not in code:
            raise ValueError(f"Module {module} not allowed")
```

## 📋 Audit Logging

### Logging de Acciones

```python
import logging

logger = logging.getLogger("audit")

# Log de ejecución
logger.info(
    "Code executed",
    extra={
        "user_id": user_id,
        "execution_id": execution_id,
        "duration": duration
    }
)
```

### ELK Stack Integration

```yaml
# logstash.conf
input {
  file {
    path => "/app/logs/*.log"
    codec => json
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "doctrina-%{+YYYY.MM.dd}"
  }
}
```

## 🔐 Compliance

### GDPR

- ✅ Datos eliminados después de 30 días
- ✅ Derecho al olvido implementado
- ✅ Privacy policy en lugar

### OWASP Top 10

- ✅ A01:2021 - Broken Access Control (JWT)
- ✅ A02:2021 - Cryptographic Failures (TLS 1.3)
- ✅ A03:2021 - Injection (Pydantic validation)
- ✅ A04:2021 - Insecure Design (Security-first)
- ✅ A05:2021 - Security Misconfiguration (.env)
- ✅ A06:2021 - Vulnerable Components (pip audit)
- ✅ A07:2021 - Authentication Failures (OAuth2)
- ✅ A08:2021 - Software and Data Integrity (checksums)
- ✅ A09:2021 - Logging & Monitoring (ELK)
- ✅ A10:2021 - SSRF (input validation)

## 🧪 Security Testing

### SAST (Static Analysis)

```bash
pip install bandit
bandit -r services/
```

### DAST (Dynamic Analysis)

```bash
pip install safety
safety check
```

### Dependency Check

```bash
pip install pip-audit
pip-audit
```

## 📞 Reporting Vulnerabilities

Para reportar vulnerabilidades de seguridad:

1. **NO** abras un issue público
2. Envía email a: security@sistemaproyectomunidal.com
3. Incluye: descripción, pasos para reproducir, impacto

## ✅ Checklist de Seguridad

- [ ] Todas las variables sensibles en `.env`
- [ ] `.env` en `.gitignore`
- [ ] TLS/SSL en producción
- [ ] Rate limiting habilitado
- [ ] CORS configurado correctamente
- [ ] Input validation en todos los endpoints
- [ ] Logs de auditoría activos
- [ ] Contraseñas hasheadas (bcrypt)
- [ ] API keys rotadas cada 90 días
- [ ] Dependencias actualizadas
- [ ] Tests de seguridad pasando
- [ ] Documentación de seguridad leída

---

**Versión:** 1.0.0
**Última actualización:** 2025-11-17
