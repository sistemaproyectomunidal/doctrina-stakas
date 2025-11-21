# Development startup script for Stakazo - Windows PowerShell (Simple version)
param(
    [switch]$UsePostgreSQL = $false,
    [switch]$Help = $false
)

if ($Help) {
    Write-Host "Stakazo Development Environment - Windows PowerShell Edition"
    Write-Host "Usage: .\dev-start-simple.ps1 [options]"
    Write-Host "Options:"
    Write-Host "  -UsePostgreSQL    Use PostgreSQL database (requires local installation)"
    Write-Host "  -Help            Show this help message"
    exit 0
}

$ErrorActionPreference = "Stop"

Write-Host "Starting Stakazo Development Environment" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Check if we're in the correct directory
if (-not (Test-Path "backend")) {
    Write-Host "ERROR: backend directory not found" -ForegroundColor Red
    Write-Host "Please run this script from the stakazo root directory" -ForegroundColor Yellow
    exit 1
}

# Set up Python environment
Write-Host "Setting up Python environment..." -ForegroundColor Cyan

# Activate virtual environment
& "backend\venv\Scripts\Activate.ps1"

# Install/upgrade dependencies
Set-Location backend
pip install -r requirements-windows.txt --quiet

# Set environment variables
$env:PYTHONPATH = "$PWD;$PWD\app"

# Configure database
if ($UsePostgreSQL) {
    Write-Host "Configuring PostgreSQL database..." -ForegroundColor Cyan
    $env:DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/stakazo_db"
} else {
    Write-Host "Using SQLite database (local file)..." -ForegroundColor Cyan
    $env:DATABASE_URL = "sqlite+aiosqlite:///stakazo.db"
}

# Create necessary directories
Write-Host "Creating storage directories..." -ForegroundColor Cyan
if (-not (Test-Path "storage")) { New-Item -ItemType Directory -Path "storage" }
if (-not (Test-Path "storage\videos")) { New-Item -ItemType Directory -Path "storage\videos" }

# Run database migrations
Write-Host "Running database migrations..." -ForegroundColor Cyan
try {
    alembic upgrade head
    Write-Host "Migrations completed successfully" -ForegroundColor Green
} catch {
    Write-Host "Migration warning (may be expected for new setup)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Starting FastAPI backend..." -ForegroundColor Cyan
Write-Host "API: http://localhost:8000" -ForegroundColor White
Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "Debug: http://localhost:8000/debug" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the FastAPI backend
try {
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
} catch {
    Write-Host ""
    Write-Host "Server stopped" -ForegroundColor Red
} finally {
    Set-Location ..
    Write-Host "Deactivating virtual environment..." -ForegroundColor Yellow
}
