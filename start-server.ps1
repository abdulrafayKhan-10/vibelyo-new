# Helper script to start Hugo server
# Handles path issues with Winget installation

$ErrorActionPreference = "Stop"

# Possible paths for Hugo executable
$possiblePaths = @(
    "hugo",                                                                                                   # System path
    "$env:LOCALAPPDATA\Microsoft\WinGet\Links\hugo.exe",                                                      # Winget links
    "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe" # Direct package path
)

$hugoExe = $null

foreach ($path in $possiblePaths) {
    if ($path -eq "hugo") {
        if (Get-Command hugo -ErrorAction SilentlyContinue) {
            $hugoExe = "hugo"
            break
        }
    } elseif (Test-Path $path) {
        $hugoExe = $path
        break
    }
}

if ($hugoExe) {
    Write-Host "Starting Hugo Server using: $hugoExe" -ForegroundColor Green
    Write-Host "Open http://localhost:1313 in your browser" -ForegroundColor Cyan
    & $hugoExe server -D
} else {
    Write-Error "Hugo executable not found. Please restart your terminal or reinstall Hugo."
    Write-Host "Try running: winget install Hugo.Hugo.Extended" -ForegroundColor Yellow
}
