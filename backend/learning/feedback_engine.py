"""
Feedback Learning Engine
Analyzes feedback trends and improves code generation
"""

from typing import Dict, List, Optional
from sqlalchemy import func, and_, desc
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from backend.models.database_models import (
    Feedback, ModelOutput, Prompt, LearningPattern
)


class FeedbackLearningEngine:
    """Background service to analyze feedback and improve generation"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def analyze_feedback_trends(self, days: int = 30) -> Dict:
        """Analyze feedback trends over the past N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get feedback statistics
        feedback_stats = self.db.query(
            func.avg(Feedback.rating).label('avg_rating'),
            func.count(Feedback.id).label('total_feedback'),
            func.sum(func.cast(Feedback.rating >= 4, type_=func.Integer)).label('positive_count'),
            func.sum(func.cast(Feedback.rating <= 2, type_=func.Integer)).label('negative_count')
        ).filter(
            Feedback.created_at >= cutoff_date
        ).first()
        
        # Get language-specific performance
        language_stats = self.db.query(
            ModelOutput.language,
            func.avg(Feedback.rating).label('avg_rating'),
            func.count(Feedback.id).label('count')
        ).join(
            Feedback, ModelOutput.id == Feedback.output_id
        ).filter(
            Feedback.created_at >= cutoff_date
        ).group_by(
            ModelOutput.language
        ).all()
        
        # Get model performance
        model_stats = self.db.query(
            ModelOutput.model_name,
            func.avg(Feedback.rating).label('avg_rating'),
            func.count(Feedback.id).label('count')
        ).join(
            Feedback, ModelOutput.id == Feedback.output_id
        ).filter(
            Feedback.created_at >= cutoff_date
        ).group_by(
            ModelOutput.model_name
        ).all()
        
        return {
            "overall": {
                "avg_rating": float(feedback_stats.avg_rating or 0),
                "total_feedback": feedback_stats.total_feedback or 0,
                "positive_count": feedback_stats.positive_count or 0,
                "negative_count": feedback_stats.negative_count or 0
            },
            "by_language": [
                {
                    "language": lang,
                    "avg_rating": float(avg_rating),
                    "count": count
                }
                for lang, avg_rating, count in language_stats
            ],
            "by_model": [
                {
                    "model": model,
                    "avg_rating": float(avg_rating),
                    "count": count
                }
                for model, avg_rating, count in model_stats
            ]
        }
    
    def extract_successful_patterns(self, min_rating: int = 4) -> List[Dict]:
        """Extract patterns from highly-rated code"""
        successful_outputs = self.db.query(
            ModelOutput, Feedback, Prompt
        ).join(
            Feedback, ModelOutput.id == Feedback.output_id
        ).join(
            Prompt, ModelOutput.prompt_id == Prompt.id
        ).filter(
            Feedback.rating >= min_rating
        ).order_by(
            desc(Feedback.rating)
        ).limit(100).all()
        
        patterns = []
        for output, feedback, prompt in successful_outputs:
            pattern = {
                "language": output.language,
                "prompt": prompt.prompt_text,
                "code_snippet": output.generated_code[:500],  # First 500 chars
                "rating": feedback.rating,
                "model": output.model_name
            }
            patterns.append(pattern)
        
        return patterns
    
    def extract_problematic_patterns(self, max_rating: int = 2) -> List[Dict]:
        """Extract patterns from poorly-rated code"""
        problematic_outputs = self.db.query(
            ModelOutput, Feedback, Prompt
        ).join(
            Feedback, ModelOutput.id == Feedback.output_id
        ).join(
            Prompt, ModelOutput.prompt_id == Prompt.id
        ).filter(
            Feedback.rating <= max_rating
        ).order_by(
            Feedback.rating
        ).limit(100).all()
        
        patterns = []
        for output, feedback, prompt in problematic_outputs:
            pattern = {
                "language": output.language,
                "prompt": prompt.prompt_text,
                "code_snippet": output.generated_code[:500],
                "rating": feedback.rating,
                "comments": feedback.comments,
                "model": output.model_name
            }
            patterns.append(pattern)
        
        return patterns
    
    def update_learning_patterns(self):
        """Update learning patterns based on feedback analysis"""
        print("📚 Updating learning patterns...")
        
        # Get successful patterns
        successful = self.extract_successful_patterns()
        
        for pattern_data in successful:
            # Check if pattern exists
            existing = self.db.query(LearningPattern).filter(
                and_(
                    LearningPattern.language == pattern_data['language'],
                    LearningPattern.pattern_type == 'successful'
                )
            ).first()
            
            if existing:
                existing.occurrence_count += 1
                existing.last_updated = datetime.utcnow()
                existing.confidence_score = min(existing.confidence_score + 0.05, 1.0)
            else:
                new_pattern = LearningPattern(
                    language=pattern_data['language'],
                    pattern_type='successful',
                    pattern_description=f"High-rated {pattern_data['language']} code pattern",
                    prompt_keywords=pattern_data['prompt'][:200],
                    code_snippet=pattern_data['code_snippet'],
                    avg_rating=pattern_data['rating'],
                    confidence_score=0.6
                )
                self.db.add(new_pattern)
        
        # Get problematic patterns
        problematic = self.extract_problematic_patterns()
        
        for pattern_data in problematic:
            new_pattern = LearningPattern(
                language=pattern_data['language'],
                pattern_type='failed',
                pattern_description=f"Low-rated pattern: {pattern_data.get('comments', 'No comment')[:100]}",
                prompt_keywords=pattern_data['prompt'][:200],
                code_snippet=pattern_data['code_snippet'],
                avg_rating=pattern_data['rating'],
                confidence_score=0.7
            )
            self.db.add(new_pattern)
        
        self.db.commit()
        print(f"✅ Updated learning patterns: {len(successful)} successful, {len(problematic)} problematic")
    
    def get_language_suggestions(self, language: str) -> List[str]:
        """Get suggestions for improving code in a specific language"""
        # Get successful patterns for this language
        patterns = self.db.query(LearningPattern).filter(
            and_(
                LearningPattern.language == language,
                LearningPattern.pattern_type == 'successful',
                LearningPattern.confidence_score >= 0.6
            )
        ).order_by(
            desc(LearningPattern.confidence_score)
        ).limit(5).all()
        
        suggestions = []
        for pattern in patterns:
            suggestions.append(
                f"✨ Based on {pattern.occurrence_count} successful generations, "
                f"consider patterns similar to: {pattern.pattern_description}"
            )
        
        # Get common issues
        issues = self.db.query(LearningPattern).filter(
            and_(
                LearningPattern.language == language,
                LearningPattern.pattern_type == 'failed'
            )
        ).order_by(
            desc(LearningPattern.last_updated)
        ).limit(3).all()
        
        for issue in issues:
            suggestions.append(
                f"⚠️ Avoid: {issue.pattern_description}"
            )
        
        return suggestions
    
    def get_performance_report(self) -> Dict:
        """Generate comprehensive performance report"""
        trends = self.analyze_feedback_trends(days=30)
        
        # Get improvement suggestions
        languages_needing_improvement = [
            lang_stat for lang_stat in trends['by_language']
            if lang_stat['avg_rating'] < 3.5 and lang_stat['count'] > 5
        ]
        
        return {
            "trends": trends,
            "needs_improvement": languages_needing_improvement,
            "total_patterns_learned": self.db.query(LearningPattern).count(),
            "generated_at": datetime.utcnow().isoformat()
        }


def run_learning_cycle(db_session: Session):
    """Run a complete learning cycle - call this periodically"""
    print("\n" + "="*60)
    print("🧠 STARTING FEEDBACK LEARNING CYCLE")
    print("="*60)
    
    engine = FeedbackLearningEngine(db_session)
    
    # Analyze trends
    trends = engine.analyze_feedback_trends()
    print(f"\n📊 Overall Performance:")
    print(f"   Average Rating: {trends['overall']['avg_rating']:.2f}/5.0")
    print(f"   Total Feedback: {trends['overall']['total_feedback']}")
    print(f"   Positive: {trends['overall']['positive_count']}")
    print(f"   Negative: {trends['overall']['negative_count']}")
    
    # Update patterns
    engine.update_learning_patterns()
    
    # Generate report
    report = engine.get_performance_report()
    
    print("\n✅ Learning cycle complete!")
    print("="*60 + "\n")
    
    return report
