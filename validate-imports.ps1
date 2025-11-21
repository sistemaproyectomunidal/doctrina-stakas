# Import validation script for Stakazo - Windows PowerShell
# Tests all critical imports to ensure the refactoring works

Write-Host "Validating Stakazo Imports" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green
Write-Host ""

# Activate virtual environment
& "backend\venv\Scripts\Activate.ps1"
Set-Location backend

# Set PYTHONPATH
$env:PYTHONPATH = "$PWD;$PWD\app"

Write-Host "Python environment:" -ForegroundColor Cyan
python --version
Write-Host "PYTHONPATH: $env:PYTHONPATH" -ForegroundColor Cyan
Write-Host ""

# Test core imports
Write-Host "Testing core imports..." -ForegroundColor Yellow

$testScript = @"
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'app'))

print("OK Python path configured")

# Test core FastAPI imports
try:
    import fastapi
    import uvicorn
    import sqlalchemy
    import alembic
    print("OK Core dependencies imported")
except ImportError as e:
    print(f"ERROR Core dependency import failed: {e}")
    sys.exit(1)

# Test app imports
try:
    from app.main import app
    print("OK Main app imported")
except ImportError as e:
    print(f"ERROR Main app import failed: {e}")
    sys.exit(1)

# Test database imports
try:
    from app.core.database import get_db, init_db
    from app.core.config import settings
    print("OK Database and config imported")
except ImportError as e:
    print(f"ERROR Database/config import failed: {e}")
    sys.exit(1)

# Test model imports
try:
    from app.models.database import Job, VideoAsset, Clip
    print("OK Database models imported")
except ImportError as e:
    print(f"ERROR Database models import failed: {e}")
    sys.exit(1)

# Test engine imports
try:
    from app.campaigns_engine import schemas, selector, services
    from app.publishing_engine import router
    from app.rules_engine import RuleEngine
    print("OK Engine modules imported")
except ImportError as e:
    print(f"ERROR Engine modules import failed: {e}")
    sys.exit(1)

# Test API imports
try:
    from app.api import upload, jobs, campaigns, rules
    print("OK API modules imported")
except ImportError as e:
    print(f"ERROR API modules import failed: {e}")
    sys.exit(1)

# Test worker imports
try:
    from app.worker import worker_loop, process_single_job
    print("OK Worker modules imported")
except ImportError as e:
    print(f"ERROR Worker modules import failed: {e}")
    sys.exit(1)

# Test ledger imports
try:
    from app.ledger import log_job_event, log_clip_event
    print("OK Ledger modules imported")
except ImportError as e:
    print(f"ERROR Ledger modules import failed: {e}")
    sys.exit(1)

print("")
print("SUCCESS: All imports validated successfully!")
print("The refactored structure is ready for local development.")
"@

# Save test script temporarily
$testScript | Out-File -FilePath "validate_imports.py" -Encoding UTF8

# Run the validation
try {
    python validate_imports.py
    $validationResult = $true
} catch {
    Write-Host "❌ Import validation failed: $($_.Exception.Message)" -ForegroundColor Red
    $validationResult = $false
}

# Clean up
Remove-Item "validate_imports.py" -ErrorAction SilentlyContinue

Set-Location ..

Write-Host ""
if ($validationResult) {
    Write-Host "SUCCESS: Import validation completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your Stakazo environment is ready!" -ForegroundColor Cyan
    Write-Host "Run .\dev-start.ps1 to start the development server" -ForegroundColor White
} else {
    Write-Host "ERROR: Import validation failed" -ForegroundColor Red
    Write-Host "Please check the error messages above and run .\setup.ps1 if needed" -ForegroundColor Yellow
}
