# Command Interpreter API (GPT-5 Trigger)

Este microservicio es el punto de entrada para el flujo de automatización E2B.

- Recibe instrucciones del dashboard (natural o JSON)
- Interpreta (usando GPT-5 si está configurado)
- Devuelve acción estructurada para el orquestador/E2B

## Ejecución local

```bash
cd services/command-interpreter
# Instala dependencias necesarias
pip install fastapi uvicorn pydantic httpx python-dotenv
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints principales

- `POST /api/command` : interpreta instrucciones desde el dashboard.
- `GET /api/health` : devuelve estado del servicio y si las variables esperadas están presentes.

## Configuración de GPT-5 y E2B sandbox

Para activar la interpretación real mediante GPT-5 y trabajar contra el sandbox E2B, crea un archivo `services/command-interpreter/.env` (no lo subas al repo) usando `services/command-interpreter/.env.example` como plantilla y rellena las variables necesarias:

```dotenv
# AI / LLM
GPT5_API_KEY=sk-...your_key_here
GPT5_API_URL=https://api.openai.example/v1/generate

# E2B sandbox
E2B_SANDBOX_KEY=e2b_...your_key_here
E2B_API_URL=https://sandbox.e2b.example/api
```

El script `scripts/run_local.sh` cargará automáticamente `services/command-interpreter/.env` si existe.

Recomendaciones de seguridad:

- Versiona únicamente `.env.example` (placeholders). Nunca comitees el `.env` real.
- Usa un secret manager (HashiCorp Vault, AWS Secrets Manager, k8s Secrets) en producción.
- Restringe permisos del archivo `.env` (por ejemplo `chmod 600 services/command-interpreter/.env`).

Si quieres que active la funcionalidad completa del dashboard contra sandbox ahora, confirma y arrancaré el stack local (`scripts/run_local.sh`) para verificar la integración con las claves que añadiste.

---

*Desarrollado como punto central de la arquitectura onboarding E2B-GPT5.*
