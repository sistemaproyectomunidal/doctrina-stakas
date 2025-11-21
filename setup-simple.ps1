# Simple setup script for Stakazo - Windows PowerShell
param([switch]$Help = $false)

if ($Help) {
    Write-Host "Stakazo Environment Setup Script"
    Write-Host "Usage: .\setup-simple.ps1"
    exit 0
}

$ErrorActionPreference = "Stop"

Write-Host "Setting up Stakazo Environment" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

# Check backend directory
if (-not (Test-Path "backend")) {
    Write-Host "ERROR: backend directory not found" -ForegroundColor Red
    exit 1
}

# Check Python
try {
    $pythonVersion = python --version 2>$null
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found in PATH" -ForegroundColor Red
    exit 1
}

# Create virtual environment
if (-not (Test-Path "backend\venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    Set-Location backend
    python -m venv venv
    Set-Location ..
    Write-Host "Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "Virtual environment already exists" -ForegroundColor Green
}

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
& "backend\venv\Scripts\Activate.ps1"
Set-Location backend

python -m pip install --upgrade pip
pip install -r requirements-windows.txt
pip install uvicorn[standard] gunicorn pytest pytest-asyncio httpx

Set-Location ..

# Create directories
Write-Host "Creating storage directories..." -ForegroundColor Yellow
$directories = @("storage", "storage\videos", "storage\temp", "backend\logs")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Green
    }
}

# Create .env file
if (-not (Test-Path ".env")) {
    $envContent = @"
DATABASE_URL=sqlite+aiosqlite:///stakazo.db
SECRET_KEY=dev-secret-key-$(Get-Random)
DEBUG_ENDPOINTS_ENABLED=true
WORKER_ENABLED=false
VIDEO_STORAGE_DIR=storage/videos
"@
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "Created .env file" -ForegroundColor Green
}

Write-Host ""
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "Run .\dev-start.ps1 to start the development server" -ForegroundColor Cyan
