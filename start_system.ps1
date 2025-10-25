# AI Code Generator - Startup Script
# This script starts both the backend API and opens the frontend

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 AI Code Generator - Full Stack System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is running
Write-Host "📡 Checking Ollama..." -ForegroundColor Yellow
try {
    $ollamaCheck = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "✅ Ollama is running!" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama is not running!" -ForegroundColor Red
    Write-Host "   Please start Ollama first: ollama serve" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🗄️  Initializing database..." -ForegroundColor Yellow

# Install backend dependencies if needed
Write-Host "📦 Checking backend dependencies..." -ForegroundColor Yellow
pip install -q -r backend/requirements.txt

Write-Host ""
Write-Host "🚀 Starting Backend API..." -ForegroundColor Green
Write-Host "   API Server: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

# Start backend in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python main.py"

# Wait for backend to start
Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check if backend is up
try {
    $backendCheck = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "✅ Backend API is ready!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend may take a few more seconds to start..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌐 Opening Frontend..." -ForegroundColor Green
Write-Host "   Frontend URL: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""

# Start frontend HTTP server in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend/public; python -m http.server 3000"

# Wait a moment and open browser
Start-Sleep -Seconds 2
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ System is running!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Access Points:" -ForegroundColor Yellow
Write-Host "   • Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "   • Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "   • API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host "   • Ollama:    http://localhost:11434" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Yellow
Write-Host "   • Both backend and frontend will run in separate PowerShell windows" -ForegroundColor White
Write-Host "   • Close those windows to stop the servers" -ForegroundColor White
Write-Host "   • Check backend window for generation logs" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop the servers" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to exit this window (servers will keep running)"
