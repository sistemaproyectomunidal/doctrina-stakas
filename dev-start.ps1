# Development startup script for Stakazo - Windows PowerShell
# Starts backend locally with SQLite database (no Docker required)

param(
    [switch]$UsePostgreSQL = $false,
    [switch]$Help = $false
)

# Display help
if ($Help) {
    Write-Host @"
Stakazo Development Environment - Windows PowerShell Edition

Usage: .\dev-start.ps1 [options]

Options:
  -UsePostgreSQL    Use PostgreSQL database (requires local installation)
  -Help            Show this help message

Examples:
  .\dev-start.ps1                    # Start with SQLite (default)
  .\dev-start.ps1 -UsePostgreSQL     # Start with PostgreSQL
"@
    exit 0
}

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Stakazo Development Environment" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

# Check if we're in the correct directory
if (-not (Test-Path "backend")) {
    Write-Host "❌ Error: backend directory not found" -ForegroundColor Red
    Write-Host "Please run this script from the stakazo root directory" -ForegroundColor Yellow
    exit 1
}

# Set up Python environment
Write-Host "🐍 Setting up Python environment..." -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "backend\venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    Set-Location backend
    python -m venv venv
    Set-Location ..
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "backend\venv\Scripts\Activate.ps1"

# Install/upgrade dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Set-Location backend
pip install -r requirements.txt
if (Test-Path "requirements-windows.txt") {
    pip install -r requirements-windows.txt
}

# Set environment variables
$env:PYTHONPATH = "$PWD;$PWD\app"

# Configure database
if ($UsePostgreSQL) {
    Write-Host "🗄️ Configuring PostgreSQL database..." -ForegroundColor Cyan
    $env:DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/stakazo_db"

    # Check if PostgreSQL is running
    try {
        $pgResult = psql -U postgres -d postgres -c "SELECT 1;" 2>$null
        Write-Host "✅ PostgreSQL connection verified" -ForegroundColor Green
    } catch {
        Write-Host "❌ PostgreSQL not available. Please ensure PostgreSQL is installed and running." -ForegroundColor Red
        Write-Host "   Alternative: Run without -UsePostgreSQL flag to use SQLite" -ForegroundColor Yellow
        Set-Location ..
        exit 1
    }

    # Create database if it doesn't exist
    try {
        createdb -U postgres stakazo_db 2>$null
        Write-Host "📊 Database 'stakazo_db' created" -ForegroundColor Green
    } catch {
        Write-Host "📊 Database 'stakazo_db' already exists or accessible" -ForegroundColor Yellow
    }
} else {
    Write-Host "🗄️ Using SQLite database (local file)..." -ForegroundColor Cyan
    $env:DATABASE_URL = "sqlite+aiosqlite:///stakazo.db"
}

# Create necessary directories
Write-Host "📁 Creating storage directories..." -ForegroundColor Cyan
if (-not (Test-Path "storage")) { New-Item -ItemType Directory -Path "storage" }
if (-not (Test-Path "storage\videos")) { New-Item -ItemType Directory -Path "storage\videos" }

# Run database migrations
Write-Host "🔄 Running database migrations..." -ForegroundColor Cyan
try {
    alembic upgrade head
    Write-Host "✅ Migrations completed successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Migration warning (may be expected for new setup): $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Starting FastAPI backend..." -ForegroundColor Cyan
Write-Host "   📍 API: http://localhost:8000" -ForegroundColor White
Write-Host "   📚 Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "   🔍 Debug: http://localhost:8000/debug" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the FastAPI backend
try {
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
} catch {
    Write-Host ""
    Write-Host "❌ Server stopped" -ForegroundColor Red
} finally {
    Set-Location ..
    Write-Host "🔄 Deactivating virtual environment..." -ForegroundColor Yellow
}
