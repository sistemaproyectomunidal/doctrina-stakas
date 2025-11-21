# Database setup script for Stakazo - Windows PowerShell
# Configures local database (SQLite or PostgreSQL)

param(
    [switch]$PostgreSQL = $false,
    [switch]$Reset = $false,
    [string]$DatabaseName = "stakazo_db",
    [string]$Username = "postgres",
    [string]$Password = "postgres",
    [string]$Host = "localhost",
    [int]$Port = 5432,
    [switch]$Help = $false
)

if ($Help) {
    Write-Host @"
Stakazo Database Setup Script

Usage: .\setup-database.ps1 [options]

Options:
  -PostgreSQL       Use PostgreSQL instead of SQLite
  -Reset           Reset/recreate the database
  -DatabaseName    PostgreSQL database name (default: stakazo_db)
  -Username        PostgreSQL username (default: postgres)
  -Password        PostgreSQL password (default: postgres)
  -Host            PostgreSQL host (default: localhost)
  -Port            PostgreSQL port (default: 5432)
  -Help            Show this help message

Examples:
  .\setup-database.ps1                    # Setup SQLite (default)
  .\setup-database.ps1 -PostgreSQL       # Setup PostgreSQL
  .\setup-database.ps1 -Reset             # Reset SQLite database
  .\setup-database.ps1 -PostgreSQL -Reset # Reset PostgreSQL database
"@
    exit 0
}

$ErrorActionPreference = "Stop"

Write-Host "🗄️ Stakazo Database Setup" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green
Write-Host ""

# Activate Python environment
if (-not (Test-Path "backend\venv")) {
    Write-Host "❌ Python virtual environment not found" -ForegroundColor Red
    Write-Host "Please run .\setup.ps1 first" -ForegroundColor Yellow
    exit 1
}

& "backend\venv\Scripts\Activate.ps1"
Set-Location backend

# Set environment variables
$env:PYTHONPATH = "$PWD;$PWD\app"

if ($PostgreSQL) {
    Write-Host "🐘 Setting up PostgreSQL database..." -ForegroundColor Cyan

    # Configure PostgreSQL connection
    $connectionString = "postgresql+asyncpg://${Username}:${Password}@${Host}:${Port}/${DatabaseName}"
    $env:DATABASE_URL = $connectionString

    Write-Host "Connection: postgresql://${Username}:***@${Host}:${Port}/${DatabaseName}" -ForegroundColor White

    # Test PostgreSQL connection
    Write-Host "Testing PostgreSQL connection..." -ForegroundColor Yellow
    try {
        $testConnection = psql -h $Host -p $Port -U $Username -d postgres -c "SELECT 1;" 2>$null
        Write-Host "✅ PostgreSQL connection successful" -ForegroundColor Green
    } catch {
        Write-Host "❌ PostgreSQL connection failed" -ForegroundColor Red
        Write-Host "Please ensure PostgreSQL is running and credentials are correct" -ForegroundColor Yellow
        Write-Host "Install PostgreSQL: https://www.postgresql.org/download/windows/" -ForegroundColor White
        Set-Location ..
        exit 1
    }

    # Create database if it doesn't exist
    if ($Reset) {
        Write-Host "🔄 Dropping existing database..." -ForegroundColor Yellow
        try {
            dropdb -h $Host -p $Port -U $Username $DatabaseName 2>$null
            Write-Host "✅ Database dropped" -ForegroundColor Green
        } catch {
            Write-Host "ℹ️ Database didn't exist or couldn't be dropped" -ForegroundColor Gray
        }
    }

    Write-Host "📊 Creating database..." -ForegroundColor Yellow
    try {
        createdb -h $Host -p $Port -U $Username $DatabaseName 2>$null
        Write-Host "✅ Database '$DatabaseName' created" -ForegroundColor Green
    } catch {
        Write-Host "ℹ️ Database '$DatabaseName' already exists" -ForegroundColor Gray
    }

} else {
    Write-Host "📁 Setting up SQLite database..." -ForegroundColor Cyan

    $dbPath = "stakazo.db"
    $env:DATABASE_URL = "sqlite+aiosqlite:///$dbPath"

    if ($Reset -and (Test-Path $dbPath)) {
        Write-Host "🔄 Removing existing SQLite database..." -ForegroundColor Yellow
        Remove-Item $dbPath -Force
        Write-Host "✅ SQLite database removed" -ForegroundColor Green
    }

    Write-Host "Database file: $dbPath" -ForegroundColor White
}

# Initialize Alembic if needed
if (-not (Test-Path "alembic")) {
    Write-Host "🔧 Initializing Alembic..." -ForegroundColor Cyan
    alembic init alembic
    Write-Host "✅ Alembic initialized" -ForegroundColor Green
}

# Update alembic.ini with correct database URL
Write-Host "⚙️ Configuring Alembic..." -ForegroundColor Cyan
if ($PostgreSQL) {
    $alembicUrl = "postgresql+asyncpg://${Username}:${Password}@${Host}:${Port}/${DatabaseName}"
} else {
    $alembicUrl = "sqlite+aiosqlite:///stakazo.db"
}

# Read and update alembic.ini
$alembicConfig = Get-Content "alembic.ini" -Raw
$alembicConfig = $alembicConfig -replace 'sqlalchemy\.url = .*', "sqlalchemy.url = $alembicUrl"
$alembicConfig | Out-File "alembic.ini" -Encoding UTF8
Write-Host "✅ Alembic configured" -ForegroundColor Green

# Run migrations
Write-Host "🔄 Running database migrations..." -ForegroundColor Cyan
try {
    alembic upgrade head
    Write-Host "✅ Database migrations completed" -ForegroundColor Green
} catch {
    Write-Host "❌ Migration failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "This might be expected for a new setup" -ForegroundColor Yellow
}

# Verify database setup
Write-Host "🔍 Verifying database setup..." -ForegroundColor Cyan

$verifyScript = @"
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'app'))

import asyncio
from app.core.database import init_db, engine
from sqlalchemy import text

async def verify_db():
    try:
        # Initialize database
        await init_db()

        # Test connection
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ Database connection verified")

        print("✅ Database setup verification completed")
        return True
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(verify_db())
    sys.exit(0 if success else 1)
"@

$verifyScript | Out-File -FilePath "verify_db.py" -Encoding UTF8

try {
    python verify_db.py
    $verificationPassed = $true
} catch {
    Write-Host "❌ Database verification failed" -ForegroundColor Red
    $verificationPassed = $false
}

Remove-Item "verify_db.py" -ErrorAction SilentlyContinue

Set-Location ..

# Update .env file with database configuration
if (Test-Path ".env") {
    Write-Host "📝 Updating .env file..." -ForegroundColor Cyan

    $envContent = Get-Content ".env" -Raw
    if ($PostgreSQL) {
        $newDbUrl = "DATABASE_URL=postgresql+asyncpg://${Username}:${Password}@${Host}:${Port}/${DatabaseName}"
    } else {
        $newDbUrl = "DATABASE_URL=sqlite+aiosqlite:///stakazo.db"
    }

    if ($envContent -match "DATABASE_URL=.*") {
        $envContent = $envContent -replace "DATABASE_URL=.*", $newDbUrl
    } else {
        $envContent += "`n$newDbUrl"
    }

    $envContent | Out-File ".env" -Encoding UTF8
    Write-Host "✅ .env file updated" -ForegroundColor Green
}

Write-Host ""
if ($verificationPassed) {
    Write-Host "🎉 Database setup completed successfully!" -ForegroundColor Green

    if ($PostgreSQL) {
        Write-Host "📊 PostgreSQL database configured:" -ForegroundColor Cyan
        Write-Host "   Host: $Host:$Port" -ForegroundColor White
        Write-Host "   Database: $DatabaseName" -ForegroundColor White
        Write-Host "   User: $Username" -ForegroundColor White
    } else {
        Write-Host "📁 SQLite database configured:" -ForegroundColor Cyan
        Write-Host "   File: backend/stakazo.db" -ForegroundColor White
    }

    Write-Host ""
    Write-Host "Next: Run .\dev-start.ps1 to start the development server" -ForegroundColor Yellow
} else {
    Write-Host "❌ Database setup encountered issues" -ForegroundColor Red
    Write-Host "Please check the error messages above" -ForegroundColor Yellow
}
