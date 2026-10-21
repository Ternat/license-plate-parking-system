@echo off
setlocal enabledelayedexpansion

echo ==============================================
echo Automatic Setup ^& Run - LPR Parking System
echo ==============================================
echo.

set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%backend"
set "FRONTEND_DIR=%SCRIPT_DIR%frontend"

echo [1/4] Installing backend dependencies...
cd /d "%BACKEND_DIR%"
pip install -r requirements.txt -q
if errorlevel 1 (
    echo Error: Failed to install backend dependencies.
    pause
    exit /b 1
)
echo Backend dependencies installed.
echo.

echo [2/4] Starting backend server...
start "Backend Server" cmd /k "cd /d "%BACKEND_DIR%" && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul
echo Backend started on http://localhost:8000
echo.

echo [3/4] Installing frontend dependencies...
cd /d "%FRONTEND_DIR%"
if not exist node_modules (
    npm install
    if errorlevel 1 (
        echo Warning: npm install failed, will try to start frontend anyway.
    )
) else (
    echo Frontend dependencies already installed.
)
echo.

echo [4/4] Starting frontend server...
start "Frontend Server" cmd /k "cd /d "%FRONTEND_DIR%" && npm run dev"
timeout /t 3 /nobreak >nul
echo.
echo ==============================================
echo System started successfully!
echo Frontend: http://localhost:3001
echo Backend:  http://localhost:8000
echo ==============================================
pause
