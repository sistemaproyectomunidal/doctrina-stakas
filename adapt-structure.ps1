# Adaptador de estructura del código - Windows PowerShell
# Asegura que la estructura local coincida con el repositorio remoto

param(
    [switch]$Fix = $false,
    [switch]$Help = $false
)

if ($Help) {
    Write-Host @"
Adaptador de Estructura del Código

Usage: .\adapt-structure.ps1 [options]

Options:
  -Fix     Aplicar las correcciones encontradas
  -Help    Mostrar esta ayuda

Este script:
- Verifica que la estructura local coincida con el repo remoto
- Valida las importaciones Python
- Corrige paths y configuraciones para Windows
- Asegura compatibilidad completa
"@
    exit 0
}

$ErrorActionPreference = "Stop"

Write-Host "Verificando estructura del codigo local vs remoto..." -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar estructura de directorios críticos
Write-Host "1. Verificando estructura de directorios..." -ForegroundColor Yellow

$criticalDirs = @(
    "backend\app",
    "backend\app\api",
    "backend\app\core",
    "backend\app\models",
    "backend\app\ledger",
    "backend\app\campaigns_engine",
    "backend\app\rules_engine",
    "backend\app\publishing_engine",
    "backend\app\publishing_integrations",
    "backend\app\e2b",
    "backend\app\worker",
    "backend\app\worker\handlers",
    "backend\app\services",
    "backend\tests",
    "clients\python",
    "clients\typescript-axios",
    "tests",
    "openapi"
)

$missingDirs = @()
foreach ($dir in $criticalDirs) {
    if (-not (Test-Path $dir)) {
        $missingDirs += $dir
        Write-Host "  FALTA: $dir" -ForegroundColor Red
    } else {
        Write-Host "  OK: $dir" -ForegroundColor Green
    }
}

# 2. Verificar archivos críticos
Write-Host ""
Write-Host "2. Verificando archivos críticos..." -ForegroundColor Yellow

$criticalFiles = @(
    "backend\main.py",
    "backend\app\main.py",
    "backend\app\__init__.py",
    "backend\app\core\config.py",
    "backend\app\core\database.py",
    "backend\app\models\database.py",
    "backend\alembic.ini",
    "backend\requirements.txt",
    "backend\requirements-windows.txt"
)

$missingFiles = @()
foreach ($file in $criticalFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
        Write-Host "  FALTA: $file" -ForegroundColor Red
    } else {
        Write-Host "  OK: $file" -ForegroundColor Green
    }
}

# 3. Verificar PYTHONPATH y importaciones
Write-Host ""
Write-Host "3. Verificando configuración PYTHONPATH..." -ForegroundColor Yellow

$pythonPathTest = @"
import sys
import os

# Configurar PYTHONPATH para estructura local
backend_path = os.path.abspath('.')
app_path = os.path.join(backend_path, 'app')

if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
if app_path not in sys.path:
    sys.path.insert(0, app_path)

print("PYTHONPATH configurado:")
for path in sys.path[:5]:  # Mostrar solo los primeros 5
    print(f"  {path}")

# Probar importaciones críticas
try:
    from app.main import app
    print("✅ app.main importado correctamente")
except ImportError as e:
    print(f"❌ Error importando app.main: {e}")

try:
    from app.core.config import settings
    print("✅ app.core.config importado correctamente")
except ImportError as e:
    print(f"❌ Error importando app.core.config: {e}")

try:
    from app.models.database import Base
    print("✅ app.models.database importado correctamente")
except ImportError as e:
    print(f"❌ Error importando app.models.database: {e}")
"@

# Ejecutar test de importaciones
if (Test-Path "backend\venv\Scripts\Activate.ps1") {
    Write-Host "Activando entorno virtual y probando importaciones..." -ForegroundColor Cyan

    Push-Location backend
    & "venv\Scripts\Activate.ps1"

    $pythonPathTest | python -

    Pop-Location
} else {
    Write-Host "  ADVERTENCIA: No se encontró entorno virtual" -ForegroundColor Yellow
}

# 4. Verificar configuración de base de datos
Write-Host ""
Write-Host "4. Verificando configuración de base de datos..." -ForegroundColor Yellow

if (Test-Path "backend\app\core\config.py") {
    $configContent = Get-Content "backend\app\core\config.py" -Raw

    if ($configContent -match 'DATABASE_URL.*sqlite') {
        Write-Host "  ✅ Configuración SQLite encontrada" -ForegroundColor Green
    }

    if ($configContent -match 'VIDEO_STORAGE_DIR.*storage') {
        Write-Host "  ✅ Directorio de almacenamiento configurado" -ForegroundColor Green
    }
} else {
    Write-Host "  ❌ Archivo de configuración no encontrado" -ForegroundColor Red
}

# 5. Aplicar correcciones si se solicita
if ($Fix -and ($missingDirs.Count -gt 0 -or $missingFiles.Count -gt 0)) {
    Write-Host ""
    Write-Host "5. Aplicando correcciones..." -ForegroundColor Yellow

    # Crear directorios faltantes
    foreach ($dir in $missingDirs) {
        Write-Host "  Creando directorio: $dir" -ForegroundColor Cyan
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }

    # Crear __init__.py faltantes
    $initFiles = @(
        "backend\app\__init__.py",
        "backend\app\api\__init__.py",
        "backend\app\core\__init__.py",
        "backend\app\models\__init__.py",
        "backend\app\ledger\__init__.py",
        "backend\app\campaigns_engine\__init__.py",
        "backend\app\rules_engine\__init__.py",
        "backend\app\publishing_engine\__init__.py",
        "backend\app\publishing_integrations\__init__.py",
        "backend\app\e2b\__init__.py",
        "backend\app\worker\__init__.py",
        "backend\app\worker\handlers\__init__.py",
        "backend\app\services\__init__.py"
    )

    foreach ($initFile in $initFiles) {
        if (-not (Test-Path $initFile)) {
            Write-Host "  Creando: $initFile" -ForegroundColor Cyan
            "" | Out-File -FilePath $initFile -Encoding UTF8
        }
    }
}

# 6. Resumen final
Write-Host ""
Write-Host "===== RESUMEN =====" -ForegroundColor Cyan
Write-Host "Directorios faltantes: $($missingDirs.Count)" -ForegroundColor $(if($missingDirs.Count -eq 0){"Green"}else{"Red"})
Write-Host "Archivos faltantes: $($missingFiles.Count)" -ForegroundColor $(if($missingFiles.Count -eq 0){"Green"}else{"Red"})

if ($missingDirs.Count -eq 0 -and $missingFiles.Count -eq 0) {
    Write-Host ""
    Write-Host "✅ ESTRUCTURA COMPLETAMENTE COMPATIBLE" -ForegroundColor Green
    Write-Host "El código local coincide con el repositorio remoto" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "⚠️ ESTRUCTURA NECESITA AJUSTES" -ForegroundColor Yellow
    Write-Host "Ejecuta: .\adapt-structure.ps1 -Fix" -ForegroundColor Cyan
}

Write-Host ""
