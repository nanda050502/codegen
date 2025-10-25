"""
Database Connection and Session Management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
import os
from pathlib import Path

from backend.models.database_models import Base

# Database configuration
DATABASE_DIR = Path(__file__).parent.parent.parent / "data"
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DATABASE_DIR}/code_generator.db"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    poolclass=StaticPool,
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_database():
    """Initialize database - create all tables"""
    print("🗄️  Initializing database...")
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized at: {DATABASE_URL}")
    print(f"📊 Tables created: {', '.join(Base.metadata.tables.keys())}")


def get_db() -> Session:
    """
    Dependency for FastAPI to get database session
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    """
    Context manager for database session
    Usage: 
        with get_db_session() as db:
            # do database operations
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def reset_database():
    """Drop all tables and recreate - USE WITH CAUTION"""
    print("⚠️  Resetting database - all data will be lost!")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database reset complete")


def get_database_stats():
    """Get database statistics"""
    with get_db_session() as db:
        from backend.models.database_models import (
            Prompt, ModelOutput, Feedback, UserProfile, LearningPattern
        )
        
        stats = {
            "total_prompts": db.query(Prompt).count(),
            "total_outputs": db.query(ModelOutput).count(),
            "total_feedback": db.query(Feedback).count(),
            "total_users": db.query(UserProfile).count(),
            "learning_patterns": db.query(LearningPattern).count(),
        }
        
        return stats


if __name__ == "__main__":
    # Test database initialization
    init_database()
    print("\n📊 Database Stats:")
    stats = get_database_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
