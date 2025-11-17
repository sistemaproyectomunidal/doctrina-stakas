# ⚡ START_HERE - Inicia en 30 Segundos

## 🚀 Opción 1: Docker (Recomendado - 30 segundos)

```bash
# 1. Clona el repo (si no lo has hecho)
git clone https://github.com/sistemaproyectomunidal/doctrina-stakas.git
cd doctrina-stakas

# 2. Copia las variables de entorno
cp .env.example .env

# 3. Inicia todo con Docker
docker-compose up --build
```

**Acceso:**
- 🌐 API Gateway: http://localhost:8000
- 📊 E2B Dashboard: http://localhost:8501
- 🔌 E2B Monitor API: http://localhost:8001

## 🚀 Opción 2: Local (Manual - 2 minutos)

```bash
# 1. Configuración
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Inicia PostgreSQL en Docker
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres

# 3. Inicia MinIO en Docker
docker run --name minio -p 9000:9000 -p 9001:9001 -d minio/minio server /data --console-address ":9001"

# 4. Inicia los servicios
cd services/api-gateway && python main.py &
cd ../ml-service && python main.py &
cd ../social-service && python main.py &
cd ../ads-service && python main.py &
```

## 📚 Próximos Pasos

1. **Explora la documentación:** [00-README.md](00-README.md)
2. **Entiende la arquitectura:** [docs/architecture.md](docs/architecture.md)
3. **Usa el Auto-Deployer:** [docs/gpt5-auto-deployer-prompt.md](docs/gpt5-auto-deployer-prompt.md)
4. **Revisa la seguridad:** [docs/security-guide.md](docs/security-guide.md)

## 🧪 Prueba Rápida

```bash
# Una vez que los servicios estén corriendo:
curl http://localhost:8000/health

# Ver documentación interactiva:
# Abre http://localhost:8000/docs
```

## ⚠️ Variables de Entorno Importantes

Edita `.env` con tus valores:

```env
# Base de datos
DATABASE_URL=postgresql://user:password@db:5432/doctrina

# E2B Code Interpreter
E2B_API_KEY=your_e2b_key_here

# Almacenamiento
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# API Keys
OPENAI_API_KEY=your_key_here
```

## 🎯 Ahora Qué?

- **Si quieres experimentar con código:** Ve a [services/e2b-monitor/](services/e2b-monitor/)
- **Si quieres ver datos:** Abre el [Dashboard](http://localhost:8501)
- **Si quieres desplegar:** Lee [docs/deployment.md](docs/deployment.md)
- **Si quieres generar código automático:** Usa el [Auto-Deployer](docs/gpt5-auto-deployer-prompt.md)

---

**¡Listo! Ya tienes todo corriendo. Bienvenido a DOCTRINA-STAKAS.**
