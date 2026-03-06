# KMeans Engine - Docker Health Check Script
# This script checks the status of all Docker containers

param(
    [switch]$Quiet
)

# Color configuration
$colors = @{
    Green = "Green"
    Yellow = "Yellow"
    Red = "Red"
    Cyan = "Cyan"
    White = "White"
}

if (-not $Quiet) {
    Write-Host ""
    Write-Host "==================================================" -ForegroundColor $colors.Cyan
    Write-Host "  KMeans Engine - Service Health Check" -ForegroundColor $colors.Cyan
    Write-Host "==================================================" -ForegroundColor $colors.Cyan
    Write-Host ""
    Write-Host "Checking service health..." -ForegroundColor $colors.White
}

# Check if Docker is running
try {
    $dockerInfo = docker info 2>&1 | Out-String
    if ($LASTEXITCODE -neq 0) {
        Write-Host "Error: Docker is not running" -ForegroundColor $colors.Red
        exit 1
    }
} catch {
    Write-Host "Error: Docker is not installed or not accessible" -ForegroundColor $colors.Red
    exit 1
}

# Get container status
$containerStatus = docker-compose ps --format json 2>&1 | ConvertFrom-Json

# Check if we got valid output
if (-not $containerStatus) {
    Write-Host "Warning: No containers found. Services may not be running." -ForegroundColor $colors.Yellow
    exit 1
}

# Expected services
$expectedServices = @(
    @{Name = "db"; DisplayName = "Database"; Port = "3306"}
    @{Name = "backend"; DisplayName = "Backend API"; Port = "8000"}
    @{Name = "frontend"; DisplayName = "Frontend"; Port = "3000"}
)

# Build status table
$statusTable = @()
$allHealthy = $true

foreach ($service in $expectedServices) {
    $container = $containerStatus | Where-Object { $_.Service -eq $service.Name }

    if ($container) {
        $isUp = $container.State -like "*Up*"
        $status = if ($isUp) { "Up" } else { "Down" }
        $ports = $container.Ports

        if (-not $isUp) {
            $allHealthy = $false
        }
    } else {
        $status = "Not Running"
        $ports = "-"
        $allHealthy = $false
    }

    $statusTable += [PSCustomObject]@{
        Service = $service.DisplayName
        Status = $status
        Ports = $ports
    }
}

if (-not $Quiet) {
    # Display status table
    Write-Host ""
    Write-Host "Service Status:" -ForegroundColor $colors.White
    Write-Host ""
    Write-Host ("{0,-20} {1,-15} {2,-20}" -f "Service", "Status", "Ports") -ForegroundColor $colors.Cyan
    Write-Host ("-" * 55) -ForegroundColor $colors.Cyan

    foreach ($row in $statusTable) {
        $statusColor = switch ($row.Status) {
            "Up" { $colors.Green }
            default { $colors.Red }
        }

        Write-Host ("{0,-20} " -f $row.Service) -NoNewline -ForegroundColor $colors.White
        Write-Host ("{0,-15} " -f $row.Status) -NoNewline -ForegroundColor $statusColor
        Write-Host ("{0,-20}" -f $row.Ports) -ForegroundColor $colors.White
    }

    Write-Host ""

    # Overall status
    if ($allHealthy) {
        Write-Host "All services healthy!" -ForegroundColor $colors.Green
        Write-Host ""
    } else {
        Write-Host "Some services are down or not running" -ForegroundColor $colors.Red
        Write-Host ""
        Write-Host "To fix issues:" -ForegroundColor $colors.Yellow
        Write-Host "  - Check logs: docker-compose logs -f" -ForegroundColor $colors.White
        Write-Host "  - Restart services: restart.bat" -ForegroundColor $colors.White
        Write-Host ""
    }

    Write-Host "==================================================" -ForegroundColor $colors.Cyan
    Write-Host ""
}

# Return exit code
if ($allHealthy) {
    exit 0
} else {
    exit 1
}
