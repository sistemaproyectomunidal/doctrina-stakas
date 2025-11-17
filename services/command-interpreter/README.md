# Command Interpreter API (GPT-5 Trigger)

Este microservicio es el punto de entrada para el flujo de automatización E2B.

- Recibe instrucciones del dashboard (natural o JSON)
- Interpreta (simulado, luego GPT-5/Claude real)
- Devuelve acción estructurada para el orquestador/E2B

## Ejecución local

```bash
cd services/command-interpreter
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoint principal

- `POST /api/command`  
  Input: `{ "input": "deploy ml-engine en prod" }`  
  Output: `{ "action": "deploy_service", "params": { ... }, "message": "..." }`

## Extensión
 - En siguientes fases, conecta aquí la API real de GPT-5/Claude.
 - Este endpoint será el trigger para el orquestador y el resto de microservicios E2B.
 - Para integrar GPT-5 real, configura las variables de entorno `GPT5_API_URL` y `GPT5_API_KEY`.
   Puedes usar el archivo `.env.example` como plantilla o crear un archivo `services/command-interpreter/.env` con:

```
GPT5_API_URL=https://api.yourprovider.com/v1/generate
GPT5_API_KEY=sk_...your_key_here...
```

 - El script `scripts/run_local.sh` cargará automáticamente `services/command-interpreter/.env` si existe.
 - Si prefieres no usar `.env`, exporta las variables en tu entorno antes de ejecutar `run_local.sh`.
 - Nota de seguridad: no subas tu `.env` con claves privadas al repositorio.

---

*Desarrollado como punto central de la arquitectura onboarding E2B-GPT5-CLAUDE.*
