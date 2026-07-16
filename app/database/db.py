"""
Database Configuration

This module is responsible for:

1. Creating the SQLAlchemy Engine
2. Creating Database Sessions
3. Creating Base Model
4. Initializing the Database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings


# ------------------------------------------------------------------
# SQLAlchemy Base
# ------------------------------------------------------------------
class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """
    pass


# ------------------------------------------------------------------
# Database Engine
# ------------------------------------------------------------------
engine = create_engine(
    settings.database_url,
    echo=False,
    future=True,
)


# ------------------------------------------------------------------
# Session Factory
# ------------------------------------------------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# ------------------------------------------------------------------
# Dependency
# ------------------------------------------------------------------
def get_db():
    """
    Provides a database session.

    Used inside FastAPI Dependency Injection.

    Example:
        db: Session = Depends(get_db)
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ------------------------------------------------------------------
# Database Initialization
# ------------------------------------------------------------------
def init_db():
    """
    Creates all database tables.
    """

    Base.metadata.create_all(bind=engine)