from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os
from dotenv import load_dotenv
import pathlib

# Load environment variables from backend/.env file
backend_dir = pathlib.Path(__file__).parent
load_dotenv(backend_dir / ".env")

# Use DATABASE_URL from environment variables (should be PostgreSQL connection)
DATABASE_URL = os.getenv("DATABASE_URL")

# Validate that DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create the engine for PostgreSQL
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session."""
    with Session(engine) as session:
        yield session