# 🛠️ Implementar Auto-Deployer

## Opción 1: Usar el Prompt Directamente

### 1. Abrir ChatGPT/Claude

https://chat.openai.com o https://claude.ai

### 2. Copiar el Prompt

```
[Ver: docs/gpt5-auto-deployer-prompt.md]
```

### 3. Describe tu Servicio

```
Crea un microservicio FastAPI que:
- [Tu descripción aquí]
```

### 4. Copiar Código Generado

Copiar toda la respuesta.

### 5. Crear Estructura

```bash
mkdir -p services/mi-servicio
cd services/mi-servicio
```

### 6. Crear Archivos

Pegar cada sección en su archivo:
- `main.py`
- `models.py`
- `routes.py`
- `Dockerfile`
- `requirements.txt`
- `railway.json`
- `test_main.py`
- `.github/workflows/deploy.yml`

### 7. Configurar Railway

```bash
pip install -g @railway/cli
railway login
railway link
railway up
```

## Opción 2: Usar CLI Tool (Próximamente)

```bash
doctrina generate --prompt "tu descripción aquí"
```

## Opción 3: Usar API

```bash
curl -X POST http://localhost:8001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "tu descripción"}'
```

## Checklist de Implementación

- [ ] Prompt copiado correctamente
- [ ] GPT-5 generó código
- [ ] Código pegado en archivos
- [ ] `requirements.txt` actualizado
- [ ] Dockerfile funciona: `docker build .`
- [ ] Tests pasan: `pytest test_main.py`
- [ ] Railway configurado
- [ ] Git push completado
- [ ] GitHub Actions ejecutándose
- [ ] API funcionando en production

## Troubleshooting

### "Imports not found"

```bash
pip install -r requirements.txt
```

### "Dockerfile fails"

```bash
docker build . --no-cache
```

### "Tests failing"

```bash
pytest test_main.py -v
```

### "Railway deployment stuck"

```bash
railway logs
railway restart
```

---

**Guía completada:** 2025-11-17
