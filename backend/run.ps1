# Script de inicio para Windows# Script to run FastAPI server on Windows

# Activa el entorno virtual y ejecuta el servidor FastAPISet-Location C:\stakazo\backend

.\venv\Scripts\Activate.ps1

Set-Location $PSScriptRootpython -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

& .\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
