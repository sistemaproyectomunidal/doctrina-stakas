# Production startup script for Stakazo - Windows PowerShell
# Starts the backend in production mode

param(
    [string]$HostAddress = "0.0.0.0",
    [int]$Port = 8000,
    [int]$Workers = 4,
    [switch]$Help = $false
)

if ($Help) {
    Write-Host @"
Stakazo Production Startup Script

Usage: .\start.ps1 [options]

Options:
  -HostAddress <address>  Host address to bind to (default: 0.0.0.0)
  -Port <number>      Port number to listen on (default: 8000)
  -Workers <number>   Number of worker processes (default: 4)
  -Help              Show this help message

Examples:
  .\start.ps1                           # Default settings
  .\start.ps1 -Port 8080               # Custom port
  .\start.ps1 -HostAddress 127.0.0.1 -Port 9000 -Workers 2  # Custom configuration

Environment Variables:
  DATABASE_URL          Database connection string
  SECRET_KEY           JWT secret key (required in production)
"@
    exit 0
}

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Stakazo Production Server" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

# Validate environment
Write-Host "🔍 Validating production environment..." -ForegroundColor Cyan

# Check if we're in the correct directory
if (-not (Test-Path "backend")) {
    Write-Host "❌ Error: backend directory not found" -ForegroundColor Red
    Write-Host "Please run this script from the stakazo root directory" -ForegroundColor Yellow
    exit 1
}

# Check for virtual environment
if (-not (Test-Path "backend\venv")) {
    Write-Host "❌ Error: Python virtual environment not found" -ForegroundColor Red
    Write-Host "Please run .\setup.ps1 first to create the environment" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "🐍 Activating Python virtual environment..." -ForegroundColor Cyan
& "backend\venv\Scripts\Activate.ps1"

Set-Location backend

# Set production environment variables
$env:PYTHONPATH = "$PWD;$PWD\app"

# Validate required environment variables for production
if (-not $env:SECRET_KEY) {
    Write-Host "⚠️ WARNING: SECRET_KEY not set. Using default (NOT SECURE)" -ForegroundColor Yellow
    $env:SECRET_KEY = "production-secret-key-$(Get-Random)"
}

if (-not $env:DATABASE_URL) {
    Write-Host "⚠️ WARNING: DATABASE_URL not set. Using SQLite (not recommended for production)" -ForegroundColor Yellow
    $env:DATABASE_URL = "sqlite+aiosqlite:///stakazo_production.db"
}

# Set production configuration
$env:DEBUG_ENDPOINTS_ENABLED = "False"
$env:WORKER_ENABLED = "True"

# Create necessary directories
Write-Host "📁 Ensuring storage directories exist..." -ForegroundColor Cyan
if (-not (Test-Path "storage")) { New-Item -ItemType Directory -Path "storage" }
if (-not (Test-Path "storage\videos")) { New-Item -ItemType Directory -Path "storage\videos" }

# Run database migrations
Write-Host "🔄 Running database migrations..." -ForegroundColor Cyan
try {
    alembic upgrade head
    Write-Host "✅ Database migrations completed" -ForegroundColor Green
} catch {
    Write-Host "❌ Database migration failed: $($_.Exception.Message)" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Write-Host ""
Write-Host "✅ Production environment validated" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Starting production server..." -ForegroundColor Cyan
Write-Host "   📍 Host: $HostAddress" -ForegroundColor White
Write-Host "   🔌 Port: $Port" -ForegroundColor White
Write-Host "   👥 Workers: $Workers" -ForegroundColor White
Write-Host "   🗄️ Database: $($env:DATABASE_URL -replace 'password=[^@]*', 'password=***')" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the production server
try {
    gunicorn main:app -w $Workers -k uvicorn.workers.UvicornWorker --bind "${HostAddress}:${Port}"
} catch {
    Write-Host ""
    Write-Host "❌ Production server stopped" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
} finally {
    Set-Location ..
    Write-Host "🔄 Deactivating virtual environment..." -ForegroundColor Yellow
}
