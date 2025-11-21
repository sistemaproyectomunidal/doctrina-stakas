# Development stop script for Stakazo - Windows PowerShell
# Stops the backend and cleans up processes

param(
    [switch]$Help = $false
)

if ($Help) {
    Write-Host @"
Stakazo Development Environment Stop Script

Usage: .\dev-stop.ps1

This script will:
- Stop any running uvicorn processes
- Deactivate Python virtual environment
- Clean up temporary files
"@
    exit 0
}

Write-Host "🛑 Stopping Stakazo Development Environment" -ForegroundColor Red
Write-Host "===========================================" -ForegroundColor Red
Write-Host ""

# Stop uvicorn processes
Write-Host "🔍 Looking for running uvicorn processes..." -ForegroundColor Cyan
try {
    $uvicornProcesses = Get-Process | Where-Object { $_.ProcessName -like "*uvicorn*" -or $_.CommandLine -like "*uvicorn*" }
    if ($uvicornProcesses) {
        Write-Host "🛑 Stopping uvicorn processes..." -ForegroundColor Yellow
        $uvicornProcesses | Stop-Process -Force
        Write-Host "✅ Uvicorn processes stopped" -ForegroundColor Green
    } else {
        Write-Host "ℹ️ No uvicorn processes found running" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️ Could not check/stop uvicorn processes: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Stop Python processes that might be running our app
Write-Host "🔍 Looking for Python processes running stakazo..." -ForegroundColor Cyan
try {
    $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object { 
        $_.CommandLine -like "*main:app*" -or 
        $_.CommandLine -like "*stakazo*" -or
        $_.CommandLine -like "*8000*"
    }
    if ($pythonProcesses) {
        Write-Host "🛑 Stopping stakazo Python processes..." -ForegroundColor Yellow
        $pythonProcesses | Stop-Process -Force
        Write-Host "✅ Stakazo Python processes stopped" -ForegroundColor Green
    } else {
        Write-Host "ℹ️ No stakazo Python processes found running" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️ Could not check Python processes: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Clean up temporary files
Write-Host "🧹 Cleaning up temporary files..." -ForegroundColor Cyan
try {
    # Remove __pycache__ directories
    Get-ChildItem -Path "." -Recurse -Name "__pycache__" -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    
    # Remove .pyc files
    Get-ChildItem -Path "." -Recurse -Name "*.pyc" -Force | Remove-Item -Force -ErrorAction SilentlyContinue
    
    Write-Host "✅ Temporary files cleaned" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not clean all temporary files: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Show final status
Write-Host ""
Write-Host "✅ Stakazo development environment stopped" -ForegroundColor Green
Write-Host ""
Write-Host "To restart, run: .\dev-start.ps1" -ForegroundColor Cyan