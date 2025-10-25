#!/bin/bash

# ========================================
# AI Code Generator - Linux/Mac Launcher
# ========================================

echo ""
echo "========================================"
echo " AI Code Generator - Starting System"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed!${NC}"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

echo -e "${GREEN}[✓] Python detected: $(python3 --version)${NC}"

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}[WARNING] Ollama is not installed${NC}"
    echo "Please install Ollama from: https://ollama.ai/"
    exit 1
fi

echo -e "${GREEN}[✓] Ollama detected${NC}"

# Check if dependencies are installed
if ! python3 -c "import fastapi" &> /dev/null; then
    echo ""
    echo "[i] Installing dependencies..."
    cd backend
    pip3 install -r requirements.txt
    cd ..
fi

echo -e "${GREEN}[✓] Dependencies ready${NC}"

# Create data directory if it doesn't exist
mkdir -p data

# Start backend in background
echo ""
echo "[i] Starting Backend API on port 8000..."
python3 run_backend.py > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 3

# Start frontend in background
echo "[i] Starting Frontend UI on port 3000..."
cd frontend/public
python3 -m http.server 3000 > ../../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ../..
echo "Frontend PID: $FRONTEND_PID"

# Wait for frontend to start
sleep 2

# Open browser
echo ""
echo "[i] Opening browser..."
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
elif command -v open &> /dev/null; then
    open http://localhost:3000
fi

echo ""
echo "========================================"
echo " System Started Successfully!"
echo "========================================"
echo ""
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "  Backend PID:  $BACKEND_PID"
echo "  Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all servers..."
echo ""

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo ''; echo '[✓] All servers stopped'; exit" INT

# Keep script running
wait
