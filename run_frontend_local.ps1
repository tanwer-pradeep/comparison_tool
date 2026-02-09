$ErrorActionPreference = "Stop"

Write-Host "Setting up Frontend Environment..."

# Function to find npm
function Get-NpmPath {
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        return "npm"
    }
    
    # Try common install locations
    $nodePath = Get-Command node -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
    if ($nodePath) {
        $npmPath = Join-Path (Split-Path $nodePath) "npm.cmd"
        if (Test-Path $npmPath) {
            return $npmPath
        }
    }
    
    throw "npm not found. Please install Node.js from https://nodejs.org/"
}

$npmCmd = Get-NpmPath
Write-Host "Using npm from: $npmCmd"

cd frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing NPM dependencies..."
    & $npmCmd install
}

Write-Host "Starting Frontend Server on http://localhost:3000..."
& $npmCmd run dev
