# Guía de Configuración para Windows (Sin Docker)# 🚀 Stakazo - Configuración Completa para Windows



Este proyecto está adaptado para funcionar en **Windows sin Docker** usando **SQLite** en lugar de PostgreSQL.## ✅ Resumen de Configuración



## Requisitos**Todo está listo para trabajar en Windows sin Docker ni virtualización.**



- **Python 3.11+** (probado con 3.13)### 📁 Estructura del Proyecto

- **PowerShell 5.1+** o PowerShell Core 7+```

- **Git** para WindowsC:\stakazo/

- **VS Code** (recomendado)├── backend/               # FastAPI backend

│   ├── app/              # Código de la aplicación

## Configuración Inicial│   ├── venv/             # Virtual environment (Python 3.13)

│   ├── requirements.txt  # Dependencias (SQLite, no PostgreSQL)

### 1. Clonar el Repositorio│   ├── run.ps1           # Script de inicio rápido

│   └── stakazo.db        # Base de datos SQLite (se crea automáticamente)

```powershell├── .vscode/

git clone https://github.com/sistemaproyectomunidal/stakazo.git│   └── settings.json     # Configuración VS Code (Windows/Linux)

cd stakazo└── README_WINDOWS.md     # Este archivo

``````



### 2. Crear Entorno Virtual### 🔧 Configuración Actual



```powershell**Base de Datos:** SQLite (archivo local `stakazo.db`)

cd backend- ✅ No requiere PostgreSQL

python -m venv venv- ✅ No requiere Docker

.\venv\Scripts\Activate.ps1- ✅ Funciona directamente en Windows

```

**Dependencias Instaladas:**

### 3. Instalar Dependencias- FastAPI + Uvicorn

- SQLAlchemy + aiosqlite

```powershell- Pydantic >= 2.10.0 (compatible con Python 3.13)

pip install --upgrade pip- Todas las demás dependencias

pip install -r requirements.txt

```### 🚀 Cómo Iniciar el Servidor



### 4. Configurar Base de Datos**Opción 1: Desde PowerShell**

```powershell

El proyecto usa **SQLite** por defecto en Windows (configurado en `backend/app/core/config.py`):cd C:\stakazo\backend

.\venv\Scripts\Activate.ps1

```pythonpython -m uvicorn app.main:app --reload

DATABASE_URL: str = "sqlite+aiosqlite:///./stakazo.db"```

```

**Opción 2: Usar el script de inicio**

No necesitas configurar PostgreSQL ni Docker. La base de datos se creará automáticamente en el primer arranque.```powershell

C:\stakazo\backend\run.ps1

### 5. Iniciar el Servidor```



**Opción A - Script PowerShell:****Opción 3: Desde VS Code**

1. Abre la terminal integrada (Ctrl + `)

```powershell2. Asegúrate de que el venv esté activado (verás `(venv)` en el prompt)

.\run.ps13. Ejecuta: `python -m uvicorn app.main:app --reload`

```

### 🌐 Acceso a la API

**Opción B - Comando directo:**

Una vez iniciado el servidor:

```powershell- **Swagger UI**: http://127.0.0.1:8000/docs

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000- **ReDoc**: http://127.0.0.1:8000/redoc

```- **Health Check**: http://127.0.0.1:8000/health



El servidor estará disponible en: `http://localhost:8000`### 📝 Cambios Realizados



## Documentación API1. **Dependencias**:

   - ❌ Removido `asyncpg` (requiere compilación C en Windows)

- **Swagger UI**: `http://localhost:8000/docs`   - ❌ Removido `psycopg2-binary` (requiere PostgreSQL)

- **ReDoc**: `http://localhost:8000/redoc`   - ✅ Agregado `aiosqlite` (SQLite asíncrono)

   - ✅ Actualizado `pydantic` a versión compatible con Python 3.13

## Estructura del Proyecto

2. **Configuración**:

```   - Base de datos cambiada a SQLite en `app/core/config.py`

stakazo/   - Agregado `.vscode/settings.json` para compatibilidad Windows/Linux

├── backend/   - Configurado EOL a LF universal

│   ├── app/   - Configurado Python path para imports

│   │   ├── api/          # Endpoints REST

│   │   ├── core/         # Configuración3. **Git**:

│   │   ├── models/       # Modelos DB y Pydantic   - ✅ Todos los conflictos de merge resueltos

│   │   ├── services/     # Lógica de negocio   - ✅ Todos los cambios committed

│   │   ├── e2b/          # E2B Sandbox   - ⏳ Listo para push (cuando quieras)

│   │   ├── publishing_engine/      # Motor de publicación

│   │   ├── publishing_integrations/ # Integraciones sociales### 🔄 Migración a PostgreSQL (Futuro)

│   │   └── main.py       # Entry point

│   ├── tests/Cuando quieras usar PostgreSQL en producción:

│   ├── requirements.txt

│   ├── run.ps1           # Script de inicio Windows1. **En `backend/app/core/config.py`**, cambia:

│   └── stakazo.db        # Base de datos SQLite (creado automáticamente)```python

└── README_WINDOWS.md     # Esta guía# Development: SQLite

```# DATABASE_URL: str = "sqlite+aiosqlite:///./stakazo.db"

# Production: PostgreSQL

## Diferencias Windows vs Linux/DockerDATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/stakazo_db"

```

### Base de Datos

2. **En `backend/requirements.txt`**, agrega:

| Entorno | Base de Datos | Configuración |```txt

|---------|--------------|---------------|asyncpg==0.29.0

| **Windows (local)** | SQLite | `sqlite+aiosqlite:///./stakazo.db` |```

| **Linux/Docker** | PostgreSQL | `postgresql+asyncpg://user:pass@host/db` |

3. **Instala PostgreSQL** o usa Docker

### Dependencias

### 🐛 Solución de Problemas

**Windows (sin compilación C/C++):**

- ✅ `aiosqlite` - Pure Python, sin compilación**Error: "ModuleNotFoundError: No module named 'sqlalchemy'"**

- ✅ `pydantic>=2.10.0` - Wheels pre-compilados para Python 3.13- Solución: Activa el virtual environment

- ❌ ~~`asyncpg`~~ - Requiere compilador C (no usado en Windows)  ```powershell

- ❌ ~~`psycopg2-binary`~~ - Requiere librerías PostgreSQL  .\venv\Scripts\Activate.ps1

  ```

### Scripts de Inicio

**Error: "Import 'app.api' could not be resolved"**

**Windows:**- Solución: VS Code necesita saber dónde está el código

```powershell  - Abre la paleta de comandos (Ctrl+Shift+P)

.\run.ps1  - Busca "Python: Select Interpreter"

```  - Selecciona el intérprete de `.\venv\Scripts\python.exe`



**Linux:****El servidor no inicia**

```bash- Verifica que el venv esté activado

./run.sh  # o docker-compose up- Verifica que estés en `C:\stakazo\backend`

```- Ejecuta: `python -m uvicorn app.main:app --reload`



## Troubleshooting### 📦 Próximos Pasos



### Error: "cannot import name 'asyncpg'"1. **Verificar que el servidor inicia correctamente**:

   ```powershell

**Solución:** Asegúrate de estar usando SQLite. En `backend/app/core/config.py`:   cd C:\stakazo\backend

   .\venv\Scripts\Activate.ps1

```python   python -m uvicorn app.main:app --reload

DATABASE_URL: str = "sqlite+aiosqlite:///./stakazo.db"   ```

```

2. **Abrir Swagger UI**: http://127.0.0.1:8000/docs

### Error: "pip install asyncpg failed"

3. **Probar endpoints**:

**Solución:** No necesitas `asyncpg` en Windows. Si está en `requirements.txt`, elimínalo o comenta la línea.   - GET /health

   - POST /upload (con un archivo de video)

### Error: "ModuleNotFoundError: No module named 'app'"   - GET /jobs



**Solución:** Asegúrate de ejecutar uvicorn desde el directorio `backend/`:4. **Implementar lógica de negocio** en:

   - `backend/app/services/` - Servicios de procesamiento

```powershell   - `backend/app/api/` - Handlers de endpoints

cd C:\stakazo\backend

.\venv\Scripts\Activate.ps1### 🔗 Enlaces Útiles

uvicorn app.main:app --reload

```- **Documentación FastAPI**: https://fastapi.tiangolo.com/

- **Documentación SQLAlchemy**: https://docs.sqlalchemy.org/

### Configurar VS Code- **Documentación Pydantic**: https://docs.pydantic.dev/



Crea `.vscode/settings.json`:### ✨ Estado del Proyecto



```json✅ Conflictos de merge resueltos

{✅ Dependencias instaladas

    "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/Scripts/python.exe",✅ Configuración Windows lista

    "python.analysis.extraPaths": ["${workspaceFolder}/backend"],✅ SQLite configurado

    "files.eol": "\n",✅ VS Code configurado

    "terminal.integrated.defaultProfile.windows": "PowerShell"✅ Git limpio (ready to push)

}⏳ Servidor listo para iniciar

```

**¡Todo listo para desarrollo en Windows sin virtualización!** 🎉

## Testing

```powershell
cd backend
pytest tests/ -v
```

## Migración a PostgreSQL (Opcional)

Si más adelante quieres usar PostgreSQL:

1. Instala PostgreSQL localmente o usa Docker
2. Actualiza `backend/app/core/config.py`:
   ```python
   DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/stakazo"
   ```
3. Instala asyncpg:
   ```powershell
   pip install asyncpg
   ```

## Soporte

- **Issues**: https://github.com/sistemaproyectomunidal/stakazo/issues
- **Docs**: `http://localhost:8000/docs`
