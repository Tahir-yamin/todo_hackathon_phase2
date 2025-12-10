from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel

# Load environment variables from .env file
load_dotenv()

# Use DATABASE_URL from environment variables (should be PostgreSQL connection)
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# Validate that DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create the engine for PostgreSQL
engine = create_engine(DATABASE_URL)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create database tables based on models."""
    SQLModel.metadata.create_all(engine)