$npmCmd = "npm" # Default to npm in PATH, the user's manual fix worked last time
# Clean .next cache to ensure fresh build with new paths
if (Test-Path ".next") {
    Remove-Item -Recurse -Force ".next"
}

Write-Host "Starting Frontend Server..."
npm run dev
