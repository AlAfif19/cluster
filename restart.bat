@echo off
REM KMeans Engine - Development Environment Restart Script
REM This script restarts all services in Docker containers

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
    echo %RED%Error: Docker is not running. Please start Docker Desktop and try again.%RESET%
    exit /b 1
)

REM Check if docker-compose exists
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%Error: docker-compose is not installed or not in PATH.%RESET%
    echo %YELLOW%Please install Docker Compose and try again.%RESET%
    exit /b 1
)

echo %YELLOW%Restarting KMeans Engine Development Environment...%RESET%
echo.

REM Restart containers
docker-compose restart

if %errorlevel% neq 0 (
    echo %RED%Error: Failed to restart Docker containers.%RESET%
    echo %YELLOW%Check the error messages above for details.%RESET%
    exit /b 1
)

echo.
echo %GREEN%Waiting for containers to reinitialize...%RESET%
timeout /t 5 /nobreak >nul

REM Run health check
if exist scripts\docker-healthcheck.ps1 (
    echo.
    powershell -ExecutionPolicy Bypass -File scripts\docker-healthcheck.ps1
)

echo.
echo %CYAN%==================================================%RESET%
echo %GREEN%All services restarted successfully!%RESET%
echo %CYAN%==================================================%RESET%
echo.
echo %YELLOW%Access your services:%RESET%
echo   %CYAN%- Frontend:%RESET%     http://localhost:3000
echo   %CYAN%- Backend API:%RESET%  http://localhost:8000
echo   %CYAN%- API Docs:%RESET%     http://localhost:8000/docs
echo.
echo %YELLOW%Useful commands:%RESET%
echo   %CYAN%- View logs:%RESET%    docker-compose logs -f
echo   %CYAN%- Stop services:%RESET% stop.bat
echo.

endlocal
