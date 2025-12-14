import os
import uuid
from sqlmodel import Session, create_engine, select
from backend.models import User
from dotenv import load_dotenv

# Explicitly load .env from the backend folder
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ Error: DATABASE_URL not found!")
    exit(1)

# Fix for Neon DB (postgres:// -> postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def seed():
    try:
        with Session(engine) as session:
            # The specific UUID your backend is looking for
            target_uuid = uuid.UUID("12345678-1234-5678-9012-123456789012")
            
            # Check if user exists
            existing_user = session.get(User, target_uuid)
            if existing_user:
                print(f"✅ User {target_uuid} already exists.")
                return

            # Create the user if missing
            new_user = User(
                id=target_uuid,
                username="testuser",
                email="test@example.com",
                full_name="Test User"
            )
            session.add(new_user)
            session.commit()
            print(f"🎉 Successfully created user: {target_uuid}")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")

if __name__ == "__main__":
    seed()
