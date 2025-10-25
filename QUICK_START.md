# 🚀 Quick Start Guide

## ⚡ Fast Setup (5 Minutes)

### Step 1: Install Dependencies

```powershell
# Navigate to gen directory
cd C:\Users\nnand\Desktop\gen

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### Step 2: Make Sure Ollama is Running

```powershell
# Check if Ollama is running
ollama list

# If not running, start it
ollama serve
```

### Step 3: Start the System

#### Option A: Automatic (Recommended)
```powershell
# Run the startup script
.\start_system.ps1
```

This will:
- ✅ Check Ollama is running
- ✅ Install dependencies
- ✅ Start backend on port 8000
- ✅ Start frontend on port 3000
- ✅ Open browser automatically

#### Option B: Manual

**Terminal 1 - Backend:**
```powershell
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend/public
python -m http.server 3000
```

Then open: http://localhost:3000

---

## 🎯 Using the System

### 1. Generate Code

1. Enter your prompt (e.g., "Create a REST API endpoint in Python")
2. Select language (or use auto-detect)
3. Click "🚀 Generate Code"
4. Code appears in 2-5 seconds

### 2. Rate the Code

1. Click the star rating (1-5 stars)
2. Optionally add comments
3. Click "📤 Submit Feedback"
4. AI learns from your feedback!

### 3. Try Quick Examples

Click any example button to auto-fill prompt and generate code:
- Python REST API
- React Component  
- Binary Search
- Sorting Algorithm
- Database CRUD
- Web Scraper

---

## 🔍 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | React web interface |
| **Backend API** | http://localhost:8000 | FastAPI server |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Ollama** | http://localhost:11434 | Local LLM service |
| **Database** | `data/code_generator.db` | SQLite database file |

---

## 📡 API Testing

### Test with cURL:

```powershell
# Health check
curl http://localhost:8000/health

# Generate code
curl -X POST http://localhost:8000/api/generate `
  -H "Content-Type: application/json" `
  -d '{\"prompt\": \"create hello world in python\", \"language\": \"python\"}'

# Get statistics
curl http://localhost:8000/api/statistics
```

### Test with Browser:

Visit: http://localhost:8000/docs

Interactive Swagger UI where you can test all endpoints!

---

## 🎨 Features Overview

### ✅ What Works Right Now

| Feature | Status | Description |
|---------|--------|-------------|
| Code Generation | ✅ | Generate code in 8+ languages |
| Auto Language Detect | ✅ | Automatically detects language from prompt |
| Syntax Highlighting | ✅ | Beautiful code display with Prism.js |
| Feedback System | ✅ | 5-star rating + comments |
| Learning Engine | ✅ | Learns from feedback patterns |
| Statistics Dashboard | ✅ | Real-time stats display |
| WebSocket Streaming | ✅ | Stream code generation (endpoint ready) |
| Database Tracking | ✅ | All data saved to SQLite |
| API Documentation | ✅ | Auto-generated Swagger docs |
| Quick Examples | ✅ | 6 pre-made prompts |

---

## 📊 System Flow

```
1. User enters prompt → 
2. Frontend sends to /api/generate →
3. Backend saves prompt to database →
4. Backend calls Ollama to generate code →
5. Backend saves output to database →
6. Frontend displays code with syntax highlighting →
7. User rates code →
8. Frontend sends to /api/feedback →
9. Backend saves feedback →
10. Learning engine analyzes feedback →
11. Statistics update in real-time
```

---

## 🛠️ Troubleshooting

### ❌ "Ollama is not running"

**Solution:**
```powershell
ollama serve
```

Keep this terminal open. Ollama must be running!

### ❌ "Connection refused to localhost:8000"

**Solution:** Backend not started. Run:
```powershell
cd backend
python main.py
```

### ❌ "Module not found" errors

**Solution:** Install dependencies:
```powershell
cd backend
pip install -r requirements.txt
```

### ❌ Frontend shows CORS error

**Solution:** Make sure backend is running on port 8000 and update API_BASE_URL in `frontend/src/App.js` if needed.

### ❌ Database errors

**Solution:** Delete and recreate database:
```powershell
Remove-Item data/code_generator.db
# Restart backend (will auto-create new DB)
```

---

## 💡 Tips for Best Results

### Writing Good Prompts

✅ **Good:**
- "Create a REST API endpoint for user login with JWT authentication in Python using FastAPI"
- "Build a React component for a shopping cart with add/remove items functionality"
- "Implement a binary search tree in C++ with insert, delete, and search methods"

❌ **Bad:**
- "make code"
- "function"
- "python thing"

### Providing Useful Feedback

When rating code, mention:
- ✅ Does the code work correctly?
- ✅ Is it efficient?
- ✅ Are there any bugs?
- ✅ Is it well-documented?
- ✅ What could be improved?

---

## 🔥 Advanced Usage

### Run Learning Cycle Manually

```python
# In Python console or script
from backend.database.connection import get_db_session
from backend.learning.feedback_engine import run_learning_cycle

with get_db_session() as db:
    report = run_learning_cycle(db)
    print(report)
```

### Query Database Directly

```python
from backend.database.connection import get_db_session
from backend.models.database_models import Prompt, Feedback

with get_db_session() as db:
    # Get all prompts
    prompts = db.query(Prompt).all()
    
    # Get high-rated feedback
    good_feedback = db.query(Feedback).filter(Feedback.rating >= 4).all()
```

### Check System Stats

```powershell
curl http://localhost:8000/api/statistics | ConvertFrom-Json
```

### View Learning Patterns

```powershell
curl "http://localhost:8000/api/patterns?language=python&pattern_type=successful"
```

---

## 📈 Next Steps

After the system is running:

1. **Generate Some Code** - Try different languages and prompts
2. **Provide Feedback** - Rate at least 10 generations
3. **Check Statistics** - Watch the learning progress
4. **Run Learning Cycle** - Let AI analyze patterns
5. **Review Patterns** - See what the AI learned

---

## 🎉 You're Ready!

The system is now fully operational. Start generating code and watch the AI learn from your feedback!

**Need Help?**
- Check `SYSTEM_ARCHITECTURE.md` for detailed documentation
- Visit http://localhost:8000/docs for API reference
- Look at terminal output for debug information

---

**Happy Coding! 🚀**
