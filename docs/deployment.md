# 🚀 Deployment Guide - DOCTRINA-STAKAS

## 📋 Pre-requisitos

- Docker & Docker Compose
- Cuenta en Railway, Heroku o AWS
- PostgreSQL 14+
- MinIO (S3-compatible)

## 🐳 Docker Compose (Local)

### Setup

```bash
# 1. Clonar repositorio
git clone https://github.com/sistemaproyectomunidal/doctrina-stakas.git
cd doctrina-stakas

# 2. Copiar variables
cp .env.example .env

# 3. Editar .env con tus valores
nano .env

# 4. Iniciar servicios
docker-compose up --build
```

### Verificar

```bash
# API Gateway
curl http://localhost:8000/health

# E2B Monitor
curl http://localhost:8001/health

# E2B Dashboard
open http://localhost:8501

# PostgreSQL
psql postgresql://user:password@localhost:5432/doctrina
```

## 🚦 Railway (Recomendado)

### 1. Crear proyecto

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Iniciar proyecto
railway init

# Crear proyecto
railway create
```

### 2. Conectar servicios

```bash
# Agregar servicios
railway service

# Conectar DB
railway add postgres

# Conectar Redis
railway add redis
```

### 3. Deploy

```bash
# Push al repositorio
git push origin main

# Railway despliega automáticamente via GitHub
# Ver logs:
railway logs

# Abrir dashboard:
railway open
```

### Environment Variables

En Railway dashboard:

1. Ir a **Project Settings** → **Variables**
2. Agregar variables de `.env`:

```
E2B_API_KEY=your_key_here
DATABASE_URL=postgresql://...
MINIO_ACCESS_KEY=...
SECRET_KEY=...
```

## ☁️ Heroku

### 1. Preparar

```bash
# Instalar Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Crear app
heroku create doctrina-stakas
```

### 2. Agregar variables

```bash
heroku config:set E2B_API_KEY=your_key
heroku config:set DATABASE_URL=postgresql://...
heroku config:set SECRET_KEY=your_secret
```

### 3. Deploy

```bash
# Push a Heroku
git push heroku main

# Ver logs
heroku logs --tail
```

### Dockerfile

El `Dockerfile` debe estar en raíz o especificar en `heroku.yml`:

```yaml
build:
  docker:
    web: Dockerfile
run:
  web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 🌍 AWS (ECS/Fargate)

### 1. Preparar ECR

```bash
# Crear ECR repository
aws ecr create-repository --repository-name doctrina-stakas

# Login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {account_id}.dkr.ecr.us-east-1.amazonaws.com

# Build y push
docker build -t doctrina-stakas .
docker tag doctrina-stakas:latest {account_id}.dkr.ecr.us-east-1.amazonaws.com/doctrina-stakas:latest
docker push {account_id}.dkr.ecr.us-east-1.amazonaws.com/doctrina-stakas:latest
```

### 2. Crear Task Definition

```json
{
  "family": "doctrina-stakas",
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "api-gateway",
      "image": "{account_id}.dkr.ecr.us-east-1.amazonaws.com/doctrina-stakas:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000
        }
      ]
    }
  ]
}
```

### 3. Crear ECS Service

```bash
aws ecs create-service \
  --cluster default \
  --service-name doctrina-stakas \
  --task-definition doctrina-stakas \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

## 🔄 CI/CD (GitHub Actions)

### Workflow

`.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Test
        run: |
          pip install -r requirements.txt
          pytest
      
      - name: Build Docker
        run: docker build -t doctrina-stakas .
      
      - name: Push to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          npm i -g @railway/cli
          railway up
```

## 📊 Load Balancing

### Nginx

```nginx
upstream api_backend {
    server api-gateway:8000;
    server api-gateway-replica:8000;
    server api-gateway-replica-2:8000;
}

upstream e2b_backend {
    server e2b-monitor:8001;
    server e2b-monitor-replica:8001;
}

server {
    listen 80;
    server_name api.example.com;
    
    # API Gateway
    location /api/ {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # E2B Monitor
    location /e2b/ {
        proxy_pass http://e2b_backend;
        proxy_set_header Host $host;
    }
}
```

## 🔐 SSL/TLS

### Let's Encrypt

```bash
# Instalar Certbot
apt-get install certbot python3-certbot-nginx

# Generar certificado
certbot certonly --nginx -d api.example.com

# Auto-renew
systemctl enable certbot.timer
systemctl start certbot.timer
```

## 📈 Monitoring & Logging

### Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'doctrina'
    static_configs:
      - targets: ['localhost:8000', 'localhost:8001']
```

### ELK Stack

```docker
version: '3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.0.0
    ports:
      - "5601:5601"
  
  logstash:
    image: docker.elastic.co/logstash/logstash:8.0.0
```

## 🚨 Alerting

### Uptime Robot

1. Ir a https://uptimerobot.com
2. Create Monitor
3. URL: `https://api.example.com/health`
4. Check Interval: 5 minutes
5. Notification: Email

### PagerDuty

1. Create integration
2. Configure on-call policy
3. Escalate critical issues

## 📋 Pre-deployment Checklist

- [ ] Tests pasando (`pytest`)
- [ ] Docker builds sin errores
- [ ] Variables de entorno configuradas
- [ ] Base de datos migrada
- [ ] SSL/TLS habilitado
- [ ] Rate limiting configurado
- [ ] Backup de BD realizado
- [ ] Monitoring activo
- [ ] Logs centralizados
- [ ] Alertas configuradas
- [ ] Documentación actualizada
- [ ] Security scan pasó

## 📞 Troubleshooting

### "502 Bad Gateway"

```bash
# Verificar estado del servicio
docker-compose ps

# Ver logs
docker-compose logs api-gateway

# Reiniciar
docker-compose restart
```

### "Connection timeout"

Aumentar timeout en Nginx:

```nginx
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
```

### "Database connection refused"

```bash
# Verificar DB está corriendo
docker-compose ps postgres

# Reiniciar DB
docker-compose restart postgres

# Re-migrate
python -m alembic upgrade head
```

---

**Versión:** 1.0.0
**Última actualización:** 2025-11-17
