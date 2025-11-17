# Orchestrator API

Este servicio recibe acciones estructuradas del Command Interpreter y las ejecuta llamando a los microservicios E2B correspondientes.

- Input: `{ "action": "deploy_service", "params": { ... } }`
- Output: `{ "result": ..., "message": "..." }`

## Ejecución local

```bash
cd services/orchestrator
pip install fastapi uvicorn httpx pydantic
uvicorn main:app --reload --host 0.0.0.0 --port 8100
```

## Extensión
- Agrega más acciones y endpoints en `SERVICE_ENDPOINTS` según crezcas los microservicios.
- El orquestador es el "dispatcher" central del sistema.

---

*Desarrollado como parte de la arquitectura chatbot programador E2B-GPT5-CLAUDE.*
