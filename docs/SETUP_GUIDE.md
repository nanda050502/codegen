# 🚀 AI Code Generator - Easy Setup Guide

## 📋 Prerequisites

Before running this project on a new laptop, ensure you have:

1. **Python 3.10+** installed
   - Download from: https://www.python.org/downloads/
   - ✅ During installation, check "Add Python to PATH"

2. **Ollama** installed with models
   - Download from: https://ollama.ai/
   - After installation, run:
     ```bash
     ollama pull mistral:latest
     ollama pull llama3:latest
     ```

3. **Git** (optional, for cloning)
   - Download from: https://git-scm.com/downloads

---

## 🎯 Quick Start (3 Steps)

### Step 1: Extract/Copy the Project
```bash
# If you have a zip file, extract it
# Or clone from git:
git clone <your-repo-url>
cd gen
```

### Step 2: Install Dependencies
```bash
# Windows (PowerShell)
cd backend
pip install -r requirements.txt

# Linux/Mac
cd backend
pip3 install -r requirements.txt
```

### Step 3: Run the Application
```bash
# Windows (PowerShell)
.\start_system.ps1

# Or manually:
# Terminal 1 - Backend
python run_backend.py

# Terminal 2 - Frontend (in new terminal)
cd frontend\public
python -m http.server 3000
```

---

## 🌐 Access the Application

- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📁 Project Structure

```
gen/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API application
│   ├── requirements.txt    # Python dependencies
│   ├── models/             # Database models
│   ├── services/           # Ollama service
│   ├── database/           # Database connection
│   └── learning/           # Feedback learning engine
├── frontend/
│   └── public/             # React frontend files
│       ├── index.html      # Main HTML
│       ├── App.js          # React application
│       └── styles.css      # Futuristic styling
├── data/                   # SQLite database (auto-created)
├── run_backend.py          # Backend startup script
└── start_system.ps1        # One-click launcher

```

---

## 🔧 Troubleshooting

### Python not found?
```bash
# Check Python installation
python --version
# or
python3 --version

# If not found, add to PATH or reinstall Python
```

### Ollama not running?
```bash
# Check Ollama status
ollama list

# Start Ollama service
ollama serve
```

### Port already in use?
```bash
# Kill processes on ports 8000 or 3000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Dependencies issues?
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install dependencies
pip install -r backend/requirements.txt --upgrade
```

---

## 📦 What's Included

- ✅ FastAPI backend with REST API
- ✅ SQLite database (portable, no setup needed)
- ✅ Ollama AI integration (Mistral & Llama3)
- ✅ React frontend with futuristic UI
- ✅ Feedback learning system
- ✅ Code syntax highlighting
- ✅ Statistics dashboard

---

## 🎨 Features

1. **AI Code Generation** - Natural language to code
2. **Multi-Language Support** - Python, JavaScript, Java, C++, etc.
3. **Rating System** - Rate generated code (1-5 stars)
4. **Feedback Learning** - System learns from your feedback
5. **Statistics Dashboard** - Track usage patterns
6. **Quick Examples** - Pre-made prompts

---

## 💾 Database

- **Type:** SQLite (file-based, portable)
- **Location:** `data/code_generator.db`
- **Auto-created** on first run
- No configuration needed!

---

## 🔐 Security Notes

- Backend runs on localhost only (not exposed to internet)
- No authentication needed for local use
- Database stored locally

---

## 📞 Support

If you encounter issues:
1. Check Python version: `python --version` (need 3.10+)
2. Check Ollama: `ollama list`
3. Check ports: Make sure 8000 and 3000 are free
4. Review error messages in terminal

---

## 🚀 Production Deployment (Optional)

To deploy to a server:
1. Update CORS settings in `backend/main.py`
2. Use a production WSGI server (Gunicorn/Hypercorn)
3. Add authentication/authorization
4. Use PostgreSQL instead of SQLite
5. Deploy frontend to static hosting

---

**Enjoy your AI Code Generator!** 🎉✨
