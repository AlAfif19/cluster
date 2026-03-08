@echo off
REM KMeans Engine - Development Environment Startup Script
REM This script starts all services (frontend, backend, database) in Docker containers

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

REM Check if .env.local exists, if not create from example
if not exist .env.local (
    echo %YELLOW%.env.local not found. Creating from .env.example...%RESET%
    if exist .env.example (
        copy .env.example .env.local >nul
        echo %GREEN%Created .env.local from .env.example%RESET%
    ) else (
        echo %RED%Error: .env.example not found. Cannot create .env.local%RESET%
        echo %YELLOW%Please create .env.local manually with required environment variables.%RESET%
        exit /b 1
    )
)

echo %GREEN%Starting KMeans Engine Development Environment...%RESET%
echo.

REM Start services using docker-compose with .env.local
docker-compose --env-file .env.local up -d

if %errorlevel% neq 0 (
    echo %RED%Error: Failed to start Docker containers.%RESET%
    echo %YELLOW%Check the error messages above for details.%RESET%
    exit /b 1
)

echo.
echo %GREEN%Waiting for containers to initialize...%RESET%
timeout /t 5 /nobreak >nul

REM Run health check
if exist scripts\docker-healthcheck.ps1 (
    echo.
    powershell -ExecutionPolicy Bypass -File scripts\docker-healthcheck.ps1
)

echo.
echo %CYAN%==================================================%RESET%
echo %GREEN%All services started successfully!%RESET%
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
echo   %CYAN%- Restart:%RESET%      restart.bat
echo.

endlocal
