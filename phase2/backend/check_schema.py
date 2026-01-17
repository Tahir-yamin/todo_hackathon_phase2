#!/usr/bin/env python3
"""Check current database schema for Task table."""

from sqlmodel import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"📊 Checking schema for database: {DATABASE_URL[:50]}...")

engine = create_engine(DATABASE_URL)
is_postgres = "postgresql" in DATABASE_URL

with engine.connect() as conn:
    if is_postgres:
        # PostgreSQL query
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'Task'
            ORDER BY ordinal_position;
        """))
    else:
        # SQLite query
        result = conn.execute(text("PRAGMA table_info(Task);"))
    
    print("\n✅ Current Task table schema:\n")
    
    if is_postgres:
        print(f"{'Column Name':<20} {'Data Type':<20} {'Nullable':<10} {'Default':<30}")
        print("=" * 80)
        for row in result:
            print(f"{row[0]:<20} {row[1]:<20} {row[2]:<10} {str(row[3] or ''):<30}")
    else:
        print(f"{'CID':<5} {'Column Name':<20} {'Type':<15} {'NotNull':<10} {'Default':<20}")
        print("=" * 80)
        for row in result:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]:<10} {str(row[4] or ''):<20}")
    
    # Check if Phase 5 columns exist
    phase5_columns = ['due_date', 'remind_at', 'recurrence', 'next_occurrence']
    
    if is_postgres:
        result2 = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'Task' AND column_name IN ('due_date', 'remind_at', 'recurrence', 'next_occurrence');
        """))
    else:
        result2 = conn.execute(text("PRAGMA table_info(Task);"))
    
    existing_cols = [row[0] if is_postgres else row[1] for row in result2]
    
    print("\n📋 Phase 5 Columns Status:")
    for col in phase5_columns:
        status = "✅ EXISTS" if col in existing_cols else "❌ MISSING"
        print(f"  {col:<20} {status}")

print("\n✨ Schema check complete!")
