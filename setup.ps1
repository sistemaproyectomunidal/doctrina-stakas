# Setup script for Stakazo - Windows PowerShell
# Prepares the complete development environment

param(
    [switch]$SkipPython = $false,
    [switch]$InstallPostgreSQL = $false,
    [switch]$Help = $false
)

if ($Help) {
    Write-Host @"
Stakazo Environment Setup Script

Usage: .\setup.ps1 [options]

Options:
  -SkipPython           Skip Python virtual environment setup
  -InstallPostgreSQL    Install PostgreSQL (requires admin privileges)
  -Help                Show this help message

This script will:
- Create Python virtual environment
- Install all Python dependencies
- Set up directory structure
- Configure environment files
- Validate installation
"@
    exit 0
}

$ErrorActionPreference = "Stop"

Write-Host "🔧 Stakazo Environment Setup" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green
Write-Host ""

# Check if we're in the correct directory
if (-not (Test-Path "backend")) {
    Write-Host "❌ Error: backend directory not found" -ForegroundColor Red
    Write-Host "Please run this script from the stakazo root directory" -ForegroundColor Yellow
    exit 1
}

# Python Setup
if (-not $SkipPython) {
    Write-Host "🐍 Setting up Python environment..." -ForegroundColor Cyan
    
    # Check Python installation
    try {
        $pythonVersion = python --version 2>$null
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Python not found in PATH" -ForegroundColor Red
        Write-Host "Please install Python 3.8+ and add it to your PATH" -ForegroundColor Yellow
        exit 1
    }
    
    # Create virtual environment
    if (-not (Test-Path "backend\venv")) {
        Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
        Set-Location backend
        python -m venv venv
        Set-Location ..
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
    }
    
    # Activate and install dependencies
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    & "backend\venv\Scripts\Activate.ps1"
    Set-Location backend
    
    # Upgrade pip first
    python -m pip install --upgrade pip
    
    # Install main requirements
    pip install -r requirements.txt
    
    # Install Windows-specific requirements if they exist
    if (Test-Path "requirements-windows.txt") {
        pip install -r requirements-windows.txt
    }
    
    # Install development tools
    pip install uvicorn[standard] gunicorn pytest pytest-asyncio httpx
    
    Set-Location ..
    Write-Host "✅ Python dependencies installed" -ForegroundColor Green
}

# PostgreSQL Setup (optional)
if ($InstallPostgreSQL) {
    Write-Host "🗄️ Installing PostgreSQL..." -ForegroundColor Cyan
    
    # Check if running as administrator
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    
    if (-not $isAdmin) {
        Write-Host "❌ Administrator privileges required for PostgreSQL installation" -ForegroundColor Red
        Write-Host "Please run PowerShell as Administrator and use -InstallPostgreSQL flag" -ForegroundColor Yellow
    } else {
        # Install PostgreSQL using Chocolatey (if available) or provide instructions
        try {
            choco install postgresql --confirm 2>$null
            Write-Host "✅ PostgreSQL installed via Chocolatey" -ForegroundColor Green
        } catch {
            Write-Host "ℹ️ Chocolatey not available. Please install PostgreSQL manually:" -ForegroundColor Yellow
            Write-Host "   1. Download from: https://www.postgresql.org/download/windows/" -ForegroundColor White
            Write-Host "   2. Use default settings (postgres/postgres)" -ForegroundColor White
            Write-Host "   3. Ensure it's added to your PATH" -ForegroundColor White
        }
    }
}

# Directory Structure Setup
Write-Host "📁 Setting up directory structure..." -ForegroundColor Cyan

$directories = @(
    "storage",
    "storage\videos",
    "storage\temp",
    "backend\logs",
    "backend\storage",
    "backend\storage\videos"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    }
}

# Environment File Setup
Write-Host "⚙️ Setting up environment configuration..." -ForegroundColor Cyan

$envContent = @"
# Stakazo Environment Configuration
# Copy this to .env and customize as needed

# Database Configuration
# SQLite (default, no setup required)
DATABASE_URL=sqlite+aiosqlite:///stakazo.db

# PostgreSQL (uncomment to use)
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/stakazo_db

# Security
SECRET_KEY=dev-secret-key-change-in-production-$(Get-Random)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration  
PROJECT_NAME=Orquestador API
VERSION=0.1.0
BACKEND_CORS_ORIGINS=["*"]

# File Storage
VIDEO_STORAGE_DIR=storage/videos
MAX_UPLOAD_SIZE=524288000

# Worker Configuration
WORKER_ENABLED=false
WORKER_POLL_INTERVAL=2
MAX_JOB_RETRIES=3

# Development Configuration
DEBUG_ENDPOINTS_ENABLED=true

# Logging
LOG_LEVEL=INFO
"@

if (-not (Test-Path ".env")) {
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ Created .env file with default configuration" -ForegroundColor Green
} else {
    Write-Host "ℹ️ .env file already exists (not overwritten)" -ForegroundColor Yellow
}

# Windows Service Scripts (optional)
Write-Host "🔧 Creating additional Windows scripts..." -ForegroundColor Cyan

# Test script
$testScript = @"
# Test script for Stakazo - Windows PowerShell
# Runs the test suite

param([switch]$Coverage = `$false)

Write-Host "🧪 Running Stakazo Tests" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green

& "backend\venv\Scripts\Activate.ps1"
Set-Location backend

if (`$Coverage) {
    Write-Host "Running tests with coverage..." -ForegroundColor Cyan
    pytest --cov=app --cov-report=html --cov-report=term tests/
} else {
    Write-Host "Running tests..." -ForegroundColor Cyan
    pytest tests/ -v
}

Set-Location ..
"@

$testScript | Out-File -FilePath "test.ps1" -Encoding UTF8

# Database reset script
$resetDbScript = @"
# Database reset script for Stakazo - Windows PowerShell
# Resets the database and runs migrations

Write-Host "🗄️ Resetting Stakazo Database" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow

& "backend\venv\Scripts\Activate.ps1"
Set-Location backend

# Remove existing database files
Remove-Item "stakazo.db" -ErrorAction SilentlyContinue
Remove-Item "stakazo_production.db" -ErrorAction SilentlyContinue

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Cyan
alembic upgrade head

Write-Host "✅ Database reset completed" -ForegroundColor Green
Set-Location ..
"@

$resetDbScript | Out-File -FilePath "reset-db.ps1" -Encoding UTF8

Write-Host "✅ Additional scripts created" -ForegroundColor Green

# Validation
Write-Host "✅ Validating installation..." -ForegroundColor Cyan

# Test Python environment
try {
    & "backend\venv\Scripts\Activate.ps1"
    Set-Location backend
    python -c "import fastapi, sqlalchemy, alembic; print('✅ Core dependencies imported successfully')"
    Set-Location ..
    Write-Host "✅ Python environment validated" -ForegroundColor Green
} catch {
    Write-Host "❌ Python environment validation failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Final summary
Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review and customize .env file if needed" -ForegroundColor White
Write-Host "  2. Run .\dev-start.ps1 to start development server" -ForegroundColor White
Write-Host "  3. Visit http://localhost:8000/docs for API documentation" -ForegroundColor White
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  .\dev-start.ps1    - Start development server" -ForegroundColor White
Write-Host "  .\dev-stop.ps1     - Stop development server" -ForegroundColor White
Write-Host "  .\start.ps1        - Start production server" -ForegroundColor White
Write-Host "  .\test.ps1         - Run tests" -ForegroundColor White
Write-Host "  .\reset-db.ps1     - Reset database" -ForegroundColor White
Write-Host ""