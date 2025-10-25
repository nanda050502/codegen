@echo off
REM ========================================
REM AI Code Generator - Windows Batch Launcher
REM ========================================

echo.
echo ========================================
echo  AI Code Generator - Starting System
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [✓] Python detected

REM Check Ollama
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Ollama might not be running
    echo Please ensure Ollama is installed and running
    echo Download from: https://ollama.ai/
    pause
)

echo [✓] Ollama detected

REM Install dependencies if needed
echo.
echo Checking dependencies...
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo [i] Installing dependencies...
    cd backend
    pip install -r requirements.txt
    cd ..
)

echo [✓] Dependencies ready

REM Start backend
echo.
echo [i] Starting Backend API on port 8000...
start "AI Code Generator - Backend" cmd /k "python run_backend.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo [i] Starting Frontend UI on port 3000...
start "AI Code Generator - Frontend" cmd /k "cd frontend\public && python -m http.server 3000"

REM Wait for frontend to start
timeout /t 2 /nobreak >nul

REM Open browser
echo [i] Opening browser...
start http://localhost:3000

echo.
echo ========================================
echo  System Started Successfully!
echo ========================================
echo.
echo  Frontend: http://localhost:3000
echo  Backend:  http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop all servers...
pause >nul

REM Stop servers
taskkill /FI "WINDOWTITLE eq AI Code Generator - Backend" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq AI Code Generator - Frontend" /F >nul 2>&1

echo.
echo [✓] All servers stopped
echo.
pause
