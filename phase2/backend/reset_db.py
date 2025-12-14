#!/usr/bin/env python3
"""
Script to reset the database and recreate tables with the new schema.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import engine
from models import SQLModel
from sqlmodel import text

def reset_database():
    """Drop and recreate all tables to apply schema changes."""
    print("Resetting database schema...")

    # Drop all tables
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(bind=engine)

    # Recreate all tables
    print("Recreating all tables with new schema...")
    SQLModel.metadata.create_all(bind=engine)

    print("Database reset complete!")

if __name__ == "__main__":
    reset_database()