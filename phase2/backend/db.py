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

# Create the engine for PostgreSQL with NeonDB optimizations
# Note: sslmode is only supported by psycopg2, not asyncpg or other drivers
engine = None
try:
    # Try with sslmode for psycopg2 (production with NeonDB)
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"sslmode": "require"}
    )
    # Test connection to verify it works
    with engine.connect() as conn:
        pass
except TypeError:
    # Fallback without sslmode for other drivers (local testing)
    print("⚠️ sslmode not supported by driver, using fallback")
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )
except Exception as e:
    # If DATABASE_URL connection fails, still create engine (might work later)
    print(f"⚠️ Database connection test failed: {e}")
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session."""
    with Session(engine) as session:
        yield session