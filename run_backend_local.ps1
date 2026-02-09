$ErrorActionPreference = "Stop"

Write-Host "Setting up Python Backend Environment..."

cd backend

if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    py -m venv venv
}

Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..."
pip install -r requirements.txt
playwright install chromium

# Set Environment Variables for Local Dev (No Docker)
$env:SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///./visual_qa.db"
$env:CELERY_TASK_ALWAYS_EAGER = "True"
$env:CELERY_BROKER_URL = "memory://"
$env:CELERY_RESULT_BACKEND = "db+sqlite:///celery_results.sqlite"

# Check if migrations exist, create if not
$migrations = Get-ChildItem -Path "alembic/versions" -Filter "*.py"
if ($migrations.Count -eq 0) {
    Write-Host "Creating initial database migration..."
    alembic revision --autogenerate -m "Initial_migration"
}

Write-Host "Running Database Migrations..."
alembic upgrade head


Write-Host "Starting Backend Server on http://localhost:8000..."
uvicorn app.main:app --reload --port 8000
