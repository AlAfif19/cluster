@echo off
REM KMeans Engine - Development Environment Stop Script
REM This script stops all services and removes Docker containers

setlocal enabledelayedexpansion

REM ANSI color codes for Windows 10+
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "RED=%ESC%[91m"
set "CYAN=%ESC%[96m"
set "RESET=%ESC%[0m"

echo.
echo %CYAN%==================================================%RESET%
echo %CYAN%  KMeans Engine Development Environment%RESET%
echo %CYAN%==================================================%RESET%
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%Error: Docker is not running.%RESET%
    exit /b 1
)

REM Check if docker-compose exists
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%Error: docker-compose is not installed or not in PATH.%RESET%
    exit /b 1
)

echo %YELLOW%Stopping KMeans Engine Development Environment...%RESET%
echo.

REM Stop and remove containers
docker-compose down

if %errorlevel% neq 0 (
    echo %RED%Error: Failed to stop Docker containers.%RESET%
    echo %YELLOW%Check the error messages above for details.%RESET%
    exit /b 1
)

echo.
echo %GREEN%All services stopped successfully!%RESET%
echo.

REM Optionally offer to remove volumes
set /p REMOVE_VOLUMES="Remove Docker volumes? This will delete all database data. (y/N): "
if /i "%REMOVE_VOLUMES%"=="y" (
    echo.
    echo %YELLOW%Removing Docker volumes...%RESET%
    docker-compose down -v
    echo %GREEN%Volumes removed.%RESET%
) else (
    echo %CYAN%Volumes preserved. Data will persist when you restart.%RESET%
)

echo.
echo %YELLOW%To start services again, run:%RESET% %CYAN%start.bat%RESET%
echo.

endlocal
