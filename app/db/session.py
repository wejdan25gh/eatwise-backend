from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Create a database connection engine using the link in .env
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Database sessions (we use them within endpoints/services)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy models
class Base(DeclarativeBase):
    pass