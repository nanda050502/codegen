"""
FastAPI Backend API
Main API endpoints for code generation, feedback, and statistics
"""

from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import asyncio

from backend.database.connection import get_db, init_database, get_database_stats
from backend.services.openai_service import openai_service
from backend.learning.feedback_engine import FeedbackLearningEngine, run_learning_cycle
from backend.models.database_models import (
    Prompt, ModelOutput, Feedback, UserProfile, LearningPattern
)

# Initialize FastAPI app
app = FastAPI(
    title="AI Code Generator API",
    description="REST API for AI-powered code generation with feedback learning",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# PYDANTIC MODELS (Request/Response schemas)
# ============================================================================

class CodeGenerationRequest(BaseModel):
    prompt: str
    language: Optional[str] = None
    temperature: float = 0.3
    max_tokens: int = 1000
    user_id: Optional[int] = None


class CodeGenerationResponse(BaseModel):
    success: bool
    code: str
    language: str
    model: str
    generation_time_ms: int
    prompt_id: int
    output_id: int


class FeedbackRequest(BaseModel):
    output_id: int
    rating: int  # 1-5
    comments: Optional[str] = None
    user_id: Optional[int] = None


class FeedbackResponse(BaseModel):
    success: bool
    message: str
    feedback_id: int


class LanguageDetectionRequest(BaseModel):
    prompt: str


class LanguageDetectionResponse(BaseModel):
    detected_language: str
    confidence: float


class StatisticsResponse(BaseModel):
    total_prompts: int
    total_outputs: int
    total_feedback: int
    total_users: int
    learning_patterns: int
    avg_rating: float
    model_performance: List[dict]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def detect_language_from_prompt(prompt: str) -> str:
    """Detect programming language from prompt text"""
    prompt_lower = prompt.lower()
    
    language_keywords = {
        'python': ['python', 'django', 'flask', 'pandas', 'numpy', 'fastapi'],
        'javascript': ['javascript', 'js', 'node', 'nodejs', 'react', 'vue', 'angular', 'express'],
        'typescript': ['typescript', 'ts', 'angular', 'nest'],
        'java': ['java', 'spring', 'maven', 'gradle'],
        'cpp': ['c++', 'cpp'],
        'csharp': ['c#', 'csharp', '.net', 'dotnet', 'asp.net'],
        'rust': ['rust', 'cargo'],
        'go': ['go', 'golang'],
        'php': ['php', 'laravel', 'symfony'],
        'ruby': ['ruby', 'rails'],
    }
    
    for language, keywords in language_keywords.items():
        if any(keyword in prompt_lower for keyword in keywords):
            return language
    
    return 'python'  # Default


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database and check OpenAI on startup"""
    print("\n" + "="*60)
    print("🚀 STARTING AI CODE GENERATOR API")
    print("="*60)
    
    # Initialize database
    init_database()
    
    # Check OpenAI
    is_available, models = openai_service.check_availability()
    if is_available:
        print(f"\n✅ OpenAI API is available!")
        if models:
            print(f"📋 Available models: {', '.join(models)}")
        best_model = openai_service.select_best_model()
        print(f"🎯 Selected model: {best_model}")
    else:
        print("\n⚠️ OpenAI API is not available! Check OPENAI_API_KEY.")
    
    print("\n✅ API Server Ready!")
    print("📡 Swagger Docs: http://localhost:8000/docs")
    print("="*60 + "\n")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Code Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    is_available, models = openai_service.check_availability()
    return {
        "status": "healthy",
        "openai_available": is_available,
        "models_available": models,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/detect-language", response_model=LanguageDetectionResponse)
async def detect_language(request: LanguageDetectionRequest):
    """Detect programming language from prompt"""
    detected = detect_language_from_prompt(request.prompt)
    return {
        "detected_language": detected,
        "confidence": 0.8  # Simple keyword-based detection
    }


@app.post("/api/generate", response_model=CodeGenerationResponse)
async def generate_code(
    request: CodeGenerationRequest,
    db: Session = Depends(get_db)
):
    """Generate code from prompt"""
    
    # Detect language if not provided
    if not request.language:
        request.language = detect_language_from_prompt(request.prompt)
    
    # Save prompt to database
    prompt_record = Prompt(
        user_id=request.user_id,
        prompt_text=request.prompt,
        detected_language=request.language,
        created_at=datetime.utcnow()
    )
    db.add(prompt_record)
    db.commit()
    db.refresh(prompt_record)
    
    # Generate code using OpenAI GPT
    result = openai_service.generate_code(
        prompt=request.prompt,
        language=request.language,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    
    # Save output to database
    output_record = ModelOutput(
        prompt_id=prompt_record.id,
        model_name=result['model'] or 'unknown',
        generated_code=result['code'],
        raw_output=result['raw_output'],
        language=request.language,
        generation_time_ms=result['time_ms'],
        temperature=request.temperature,
        created_at=datetime.utcnow(),
        success=result['success'],
        error_message=result['error']
    )
    db.add(output_record)
    db.commit()
    db.refresh(output_record)
    
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['error'])
    
    return {
        "success": True,
        "code": result['code'],
        "language": request.language,
        "model": result['model'],
        "generation_time_ms": result['time_ms'],
        "prompt_id": prompt_record.id,
        "output_id": output_record.id
    }


@app.post("/api/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """Submit feedback for generated code"""
    
    # Validate output exists
    output = db.query(ModelOutput).filter(ModelOutput.id == request.output_id).first()
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")
    
    # Determine feedback type
    feedback_type = "positive" if request.rating >= 4 else "negative" if request.rating <= 2 else "neutral"
    
    # Save feedback
    feedback_record = Feedback(
        output_id=request.output_id,
        user_id=request.user_id,
        rating=request.rating,
        feedback_type=feedback_type,
        comments=request.comments,
        created_at=datetime.utcnow()
    )
    db.add(feedback_record)
    db.commit()
    db.refresh(feedback_record)
    
    return {
        "success": True,
        "message": "Feedback submitted successfully",
        "feedback_id": feedback_record.id
    }


@app.get("/api/statistics", response_model=StatisticsResponse)
async def get_statistics(db: Session = Depends(get_db)):
    """Get system statistics"""
    
    stats = get_database_stats()
    
    # Get average rating
    from sqlalchemy import func
    avg_rating = db.query(func.avg(Feedback.rating)).scalar() or 0.0
    
    # Get model performance
    model_perf = db.query(
        ModelOutput.model_name,
        func.avg(Feedback.rating).label('avg_rating'),
        func.count(ModelOutput.id).label('count')
    ).join(
        Feedback, ModelOutput.id == Feedback.output_id, isouter=True
    ).group_by(
        ModelOutput.model_name
    ).all()
    
    return {
        **stats,
        "avg_rating": float(avg_rating),
        "model_performance": [
            {"model": model, "avg_rating": float(rating or 0), "count": count}
            for model, rating, count in model_perf
        ]
    }


@app.get("/api/suggestions/{language}")
async def get_suggestions(language: str, db: Session = Depends(get_db)):
    """Get AI suggestions for a specific language"""
    
    engine = FeedbackLearningEngine(db)
    suggestions = engine.get_language_suggestions(language)
    
    return {
        "language": language,
        "suggestions": suggestions
    }


@app.post("/api/learning/run-cycle")
async def run_learning_cycle_endpoint(db: Session = Depends(get_db)):
    """Manually trigger a learning cycle"""
    
    report = run_learning_cycle(db)
    return {
        "success": True,
        "report": report
    }


@app.get("/api/patterns")
async def get_learning_patterns(
    language: Optional[str] = None,
    pattern_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get learning patterns"""
    
    query = db.query(LearningPattern)
    
    if language:
        query = query.filter(LearningPattern.language == language)
    if pattern_type:
        query = query.filter(LearningPattern.pattern_type == pattern_type)
    
    patterns = query.all()
    
    return {
        "count": len(patterns),
        "patterns": [
            {
                "id": p.id,
                "language": p.language,
                "pattern_type": p.pattern_type,
                "description": p.pattern_description,
                "avg_rating": p.avg_rating,
                "confidence": p.confidence_score,
                "occurrences": p.occurrence_count
            }
            for p in patterns
        ]
    }


# ============================================================================
# WEBSOCKET FOR STREAMING
# ============================================================================

@app.websocket("/ws/generate")
async def websocket_generate(websocket: WebSocket):
    """WebSocket endpoint for streaming code generation"""
    await websocket.accept()
    
    try:
        while True:
            # Receive request
            data = await websocket.receive_json()
            prompt = data.get('prompt')
            language = data.get('language', 'python')
            
            # Stream generation
            for chunk in openai_service.stream_generate(prompt, language):
                await websocket.send_json(chunk)
                await asyncio.sleep(0.01)  # Small delay for smooth streaming
    
    except WebSocketDisconnect:
        print("WebSocket disconnected")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)