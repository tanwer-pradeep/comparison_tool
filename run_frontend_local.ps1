$ErrorActionPreference = "Stop"

Write-Host "Setting up Frontend Environment..."

cd frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing NPM dependencies..."
    npm install
}

Write-Host "Starting Frontend Server on http://localhost:3000..."
npm run dev
