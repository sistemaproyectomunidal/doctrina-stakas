# E2B Intelligent Dashboard

Este dashboard es la interfaz central para interactuar con el sistema E2B, el Command Interpreter (GPT-5/Claude) y el orquestador.

## Características
- Input de instrucciones en lenguaje natural o JSON
- Visualización de resultados y métricas
- Preparado para integración con IA y microservicios E2B

## Ejecución local

```bash
cd dashboard
pip install streamlit requests
streamlit run app.py
```

Por defecto, el dashboard espera un backend en `http://localhost:8000/api/command` (puedes simularlo con un mock o conectar el Command Interpreter real).

## Estructura
- `app.py`: Código principal del dashboard (Streamlit)
- `README.md`: Esta documentación

## Extensión
- Conecta los endpoints reales de métricas, logs y acciones en siguientes fases.
- Integra la lógica de interpretación GPT-5/Claude en el backend.

---

*Desarrollado como parte de la arquitectura onboarding E2B-GPT5-CLAUDE.*
