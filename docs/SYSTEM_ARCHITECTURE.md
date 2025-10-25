# 🚀 AI Code Generator - Full Stack System

## System Architecture

```
┌────────────────────────────┐
│    User Interface (React)   │
│  - Prompt input             │
│  - Language selector        │
│  - Code viewer (Prism.js)   │
│  - Feedback buttons (👍👎)  │
└──────────────┬─────────────┘
               │ HTTP REST API / WebSocket
               ▼
┌────────────────────────────┐
│    FastAPI Backend         │
│  - /api/generate           │
│  - /api/feedback           │
│  - /api/statistics         │
│  - /ws/generate (stream)   │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│    Ollama Engine           │
│  - Mistral model           │
│  - Local inference         │
│  - No cloud required       │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│    SQLite Database         │
│  Tables:                   │
│  - prompts                 │
│  - model_outputs           │
│  - feedback                │
│  - learning_patterns       │
│  - user_profiles           │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│  Feedback Learning Engine  │
│  - Analyze trends          │
│  - Extract patterns        │
│  - Improve prompts         │
└────────────────────────────┘
```

## 📁 Project Structure

```
gen/
├── backend/
│   ├── main.py                 # FastAPI app with all endpoints
│   ├── requirements.txt        # Backend dependencies
│   ├── models/
│   │   └── database_models.py  # SQLAlchemy ORM models
│   ├── database/
│   │   └── connection.py       # Database connection & session
│   ├── services/
│   │   └── ollama_service.py   # Ollama API integration
│   └── learning/
│       └── feedback_engine.py  # Learning and analytics
│
├── frontend/
│   ├── public/
│   │   ├── index.html          # Main HTML file
│   │   └── styles.css          # Modern dark theme styles
│   └── src/
│       └── App.js              # React application (via CDN)
│
├── data/
│   └── code_generator.db       # SQLite database (auto-created)
│
└── app.py                       # Original Gradio app (legacy)
```

## 🛠️ Setup Instructions

### Prerequisites

1. **Python 3.10+**
2. **Ollama installed** - Download from [ollama.ai](https://ollama.ai/)
3. **Mistral model** - Run: `ollama pull mistral`

### Installation

#### Step 1: Install Backend Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

#### Step 2: Start Ollama

```powershell
ollama serve
```

Verify Mistral is available:
```powershell
ollama list
```

#### Step 3: Start the Backend Server

```powershell
# From the gen directory
cd backend
python main.py
```

Or use uvicorn directly:
```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will start at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

#### Step 4: Start the Frontend

Open `frontend/public/index.html` in your browser, or use a simple HTTP server:

```powershell
# Using Python's HTTP server
cd frontend/public
python -m http.server 3000
```

Frontend will be at: **http://localhost:3000**

## 🎯 Features

### ✅ Completed Features

1. **Backend API (FastAPI)**
   - ✅ REST API endpoints for code generation
   - ✅ Database integration with SQLAlchemy
   - ✅ Ollama service integration
   - ✅ Feedback submission system
   - ✅ Statistics and analytics
   - ✅ WebSocket support for streaming
   - ✅ CORS enabled for frontend

2. **Database Layer**
   - ✅ SQLite database with 6 tables
   - ✅ User profiles
   - ✅ Prompts tracking
   - ✅ Model outputs
   - ✅ Feedback with ratings
   - ✅ Learning patterns
   - ✅ System metrics

3. **Ollama Integration**
   - ✅ Multi-model support (Mistral, Llama3, etc.)
   - ✅ Auto model selection
   - ✅ Code extraction from responses
   - ✅ Streaming support
   - ✅ Error handling

4. **Feedback Learning Engine**
   - ✅ Analyze feedback trends
   - ✅ Extract successful patterns
   - ✅ Identify problematic patterns
   - ✅ Generate performance reports
   - ✅ Language-specific suggestions

5. **Frontend (React)**
   - ✅ Modern dark theme UI
   - ✅ Prompt input with auto-detect language
   - ✅ Code output with syntax highlighting (Prism.js)
   - ✅ Star rating system (1-5)
   - ✅ Feedback comments
   - ✅ Quick examples
   - ✅ Real-time statistics
   - ✅ Copy/Clear buttons

## 📡 API Endpoints

### Code Generation
```
POST /api/generate
Body: {
  "prompt": "string",
  "language": "python" | null,
  "temperature": 0.3,
  "max_tokens": 1000
}
Response: {
  "success": true,
  "code": "string",
  "language": "python",
  "model": "mistral:latest",
  "generation_time_ms": 2340,
  "prompt_id": 1,
  "output_id": 1
}
```

### Submit Feedback
```
POST /api/feedback
Body: {
  "output_id": 1,
  "rating": 5,
  "comments": "Great code!"
}
```

### Get Statistics
```
GET /api/statistics
Response: {
  "total_prompts": 42,
  "total_outputs": 42,
  "total_feedback": 30,
  "avg_rating": 4.2,
  "model_performance": [...]
}
```

### Language Detection
```
POST /api/detect-language
Body: { "prompt": "create a function in Python" }
Response: { "detected_language": "python", "confidence": 0.8 }
```

### Learning Patterns
```
GET /api/patterns?language=python&pattern_type=successful
```

### Run Learning Cycle
```
POST /api/learning/run-cycle
```

### WebSocket Streaming
```
WS /ws/generate
Send: { "prompt": "...", "language": "python" }
Receive: Stream of chunks
```

## 🗄️ Database Schema

### Tables

1. **user_profiles** - User information
2. **prompts** - User prompts and metadata
3. **model_outputs** - Generated code and metrics
4. **feedback** - User ratings and comments
5. **learning_patterns** - Learned patterns from feedback
6. **system_metrics** - System-wide performance metrics

### Relationships

```
user_profiles (1) ──> (N) prompts
prompts (1) ──> (N) model_outputs
model_outputs (1) ──> (1) feedback
user_profiles (1) ──> (N) feedback
```

## 🎨 Frontend Features

### Modern UI Components
- Dark theme with gradient accents
- Syntax-highlighted code display
- Responsive design (mobile-friendly)
- Loading states and animations
- Real-time statistics dashboard

### User Experience
- Auto-detect programming language from prompt
- Quick example prompts
- One-click copy to clipboard
- Star rating system (1-5 stars)
- Feedback comments for improvement
- Clear all functionality

## 🧠 Learning Engine

### Capabilities

1. **Trend Analysis**
   - Track average ratings over time
   - Identify high/low performing languages
   - Monitor model performance

2. **Pattern Extraction**
   - Learn from 4-5 star rated code
   - Identify common issues from 1-2 star code
   - Build confidence scores

3. **Suggestions**
   - Provide language-specific tips
   - Warn about common pitfalls
   - Recommend successful patterns

4. **Automatic Learning Cycles**
   - Run periodically (cron job or scheduler)
   - Update learning patterns
   - Generate performance reports

## 📊 Usage Examples

### Example 1: Generate Python Code
```javascript
// Frontend
const response = await fetch('http://localhost:8000/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'Create a binary search function in Python',
    language: 'python'
  })
});
```

### Example 2: Submit Feedback
```javascript
await fetch('http://localhost:8000/api/feedback', {
  method: 'POST',
  body: JSON.stringify({
    output_id: 1,
    rating: 5,
    comments: 'Perfect implementation!'
  })
});
```

### Example 3: Run Learning Cycle (Backend)
```python
from backend.database.connection import get_db_session
from backend.learning.feedback_engine import run_learning_cycle

with get_db_session() as db:
    report = run_learning_cycle(db)
    print(report)
```

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```
DATABASE_URL=sqlite:///./data/code_generator.db
OLLAMA_BASE_URL=http://localhost:11434
API_HOST=0.0.0.0
API_PORT=8000
```

### Backend Settings
- `main.py` - Port, CORS settings
- `connection.py` - Database path
- `ollama_service.py` - Model preferences

## 🚀 Deployment

### Production Checklist

- [ ] Set specific CORS origins
- [ ] Use PostgreSQL instead of SQLite
- [ ] Add authentication/authorization
- [ ] Implement rate limiting
- [ ] Add logging and monitoring
- [ ] Set up automatic backups
- [ ] Configure HTTPS
- [ ] Add caching layer (Redis)
- [ ] Set up CI/CD pipeline

## 📝 Development Roadmap

### Phase 1: ✅ Core System (Completed)
- Backend API
- Database layer
- Ollama integration
- Basic frontend
- Feedback system

### Phase 2: 🚧 Enhancements (In Progress)
- WebSocket real-time streaming
- Advanced learning algorithms
- User authentication
- Code templates library

### Phase 3: 📋 Future Features
- Multiple model selection in UI
- Code diff/comparison
- Export to GitHub Gist
- VSCode extension
- Collaborative coding
- Code review suggestions

## 🐛 Troubleshooting

### Ollama Not Available
```powershell
# Check if Ollama is running
ollama list

# Start Ollama
ollama serve

# Pull Mistral model
ollama pull mistral
```

### Database Issues
```python
# Reset database (WARNING: Deletes all data)
from backend.database.connection import reset_database
reset_database()
```

### CORS Errors
- Ensure backend is running on port 8000
- Check CORS middleware in `main.py`
- Update `API_BASE_URL` in `App.js`

## 📚 Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **Ollama**: https://ollama.ai/
- **React**: https://react.dev/
- **Prism.js**: https://prismjs.com/

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - Feel free to use and modify

## 🎉 Credits

- **Ollama** for local LLM inference
- **Mistral AI** for the model
- **FastAPI** for the backend framework
- **React** for the frontend
- **Prism.js** for syntax highlighting

---

**Status**: ✅ Full System Operational
**Version**: 1.0.0
**Last Updated**: October 15, 2025
