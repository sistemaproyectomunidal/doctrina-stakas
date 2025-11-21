# Stakazo Development Environment - Windows Setup Guide

This guide covers setting up the Stakazo project on Windows without Docker, using PowerShell scripts.

## 🚀 Quick Start

1. **Initial Setup**
   ```powershell
   .\setup.ps1
   ```

2. **Start Development Server**
   ```powershell
   .\dev-start.ps1
   ```

3. **Visit the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Debug endpoints: http://localhost:8000/debug

## 📋 Prerequisites

- **Python 3.8+** - Download from [python.org](https://python.org)
- **Git** - Download from [git-scm.com](https://git-scm.com)
- **PowerShell 5.1+** (included with Windows)
- **Optional: PostgreSQL** - For production-like database

## 🛠️ Available Scripts

### Main Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup.ps1` | Complete environment setup | `.\setup.ps1` |
| `dev-start.ps1` | Start development server | `.\dev-start.ps1` |
| `dev-stop.ps1` | Stop development server | `.\dev-stop.ps1` |
| `start.ps1` | Start production server | `.\start.ps1 -Port 8080` |

### Utility Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup-database.ps1` | Database configuration | `.\setup-database.ps1 -PostgreSQL` |
| `validate-imports.ps1` | Test Python imports | `.\validate-imports.ps1` |
| `test.ps1` | Run test suite | `.\test.ps1 -Coverage` |
| `reset-db.ps1` | Reset database | `.\reset-db.ps1` |

## 🗄️ Database Options

### SQLite (Default)
- **Pros**: No setup required, portable
- **Cons**: Single-user, limited performance
- **Usage**: Automatic with `.\dev-start.ps1`

### PostgreSQL (Recommended for development)
- **Pros**: Production-like, multi-user, better performance
- **Setup**:
  ```powershell
  .\setup.ps1 -InstallPostgreSQL  # Requires admin
  .\setup-database.ps1 -PostgreSQL
  .\dev-start.ps1 -UsePostgreSQL
  ```

## 📁 Project Structure

```
stakazo/
├── backend/                    # Python FastAPI backend
│   ├── app/                   # Application code
│   │   ├── api/              # API endpoints
│   │   ├── campaigns_engine/ # Campaign orchestration
│   │   ├── core/             # Core configuration
│   │   ├── ledger/           # Event logging
│   │   ├── models/           # Database models
│   │   ├── publishing_engine/# Publishing system
│   │   ├── rules_engine/     # Rules processing
│   │   └── worker/           # Background jobs
│   ├── storage/              # File storage
│   ├── tests/                # Test suite
│   └── venv/                 # Python virtual environment
├── clients/                   # API clients
│   ├── python/               # Python client
│   └── typescript-axios/     # TypeScript client
├── *.ps1                     # PowerShell scripts
└── .env                      # Environment configuration
```

## ⚙️ Environment Configuration

The `.env` file controls application behavior:

```bash
# Database (choose one)
DATABASE_URL=sqlite+aiosqlite:///stakazo.db
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/stakazo_db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
VIDEO_STORAGE_DIR=storage/videos
MAX_UPLOAD_SIZE=524288000

# Development Features
DEBUG_ENDPOINTS_ENABLED=true
WORKER_ENABLED=false

# Logging
LOG_LEVEL=INFO
```

## 🧪 Testing

```powershell
# Run all tests
.\test.ps1

# Run with coverage report
.\test.ps1 -Coverage

# Run specific test file
cd backend
pytest tests/test_campaigns_engine.py -v
```

## 🚨 Troubleshooting

### Common Issues

1. **Import errors**
   ```powershell
   .\validate-imports.ps1  # Check imports
   .\setup.ps1            # Reinstall dependencies
   ```

2. **Database connection issues**
   ```powershell
   .\setup-database.ps1 -Reset  # Reset database
   ```

3. **Port already in use**
   ```powershell
   .\dev-stop.ps1         # Stop any running instances
   .\dev-start.ps1        # Restart
   ```

4. **Permission errors**
   - Run PowerShell as Administrator
   - Check Windows execution policy: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Script Execution Policy

If you get execution policy errors:

```powershell
# Allow local scripts (run once)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run a single script
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

### Python Path Issues

If imports fail, manually set the Python path:

```powershell
cd backend
$env:PYTHONPATH = "$PWD;$PWD\app"
python -c "import app.main; print('Imports OK')"
```

## 🔧 Development Workflow

1. **Make changes** to Python code in `backend/app/`
2. **Server auto-reloads** (when using `.\dev-start.ps1`)
3. **Test changes** at http://localhost:8000/docs
4. **Run tests** with `.\test.ps1`
5. **Debug** using endpoints at http://localhost:8000/debug

## 📦 Adding Dependencies

```powershell
# Activate environment
cd backend
.\venv\Scripts\Activate.ps1

# Install new package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# For Windows-specific packages
pip freeze > requirements-windows.txt
```

## 🌐 Production Deployment

```powershell
# Configure production environment
cp .env .env.production
# Edit .env.production with production settings

# Set environment
$env:ENV_FILE = ".env.production"

# Start production server
.\start.ps1 -Workers 4 -Port 8000
```

## 📚 API Documentation

- **Interactive docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI spec**: http://localhost:8000/openapi.json
- **OpenAPI file**: `openapi/orquestador_openapi.yaml`

## 🤝 Contributing

1. Make changes in a feature branch
2. Run tests: `.\test.ps1`
3. Validate imports: `.\validate-imports.ps1`
4. Test manually with development server
5. Commit and push changes

## 📞 Support

For issues with the Windows setup:
1. Check this README
2. Run `.\validate-imports.ps1` to diagnose
3. Check logs in `backend/logs/`
4. Review PowerShell script help: `.\script-name.ps1 -Help`
