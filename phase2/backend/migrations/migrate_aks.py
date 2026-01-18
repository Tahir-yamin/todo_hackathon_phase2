#!/usr/bin/env python3
"""
Phase 5 Database Migration - Non-Interactive Version for AKS
Adds Phase 5 columns without user prompts (safe with IF NOT EXISTS).
"""

from sqlmodel import create_engine, text
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")

print(f"🔧 Phase 5 Database Migration (Non-Interactive)")
print(f"📊 Database: {DATABASE_URL[:50]}...")

engine = create_engine(DATABASE_URL)
is_postgres = "postgresql" in DATABASE_URL

print("\n🚀 Starting migration...")

with engine.connect() as conn:
    try:
        if is_postgres:
            print("📝 Running PostgreSQL migration...")
           
            # Add all Phase 5 columns (idempotent with IF NOT EXISTS)
            conn.execute(text('ALTER TABLE "Task" ADD COLUMN IF NOT EXISTS remind_at TIMESTAMP NULL;'))
            print("  ✅ remind_at")
            
            conn.execute(text('ALTER TABLE "Task" ADD COLUMN IF NOT EXISTS recurrence VARCHAR(20) DEFAULT \'NONE\';'))
            print("  ✅ recurrence")
            
            conn.execute(text('ALTER TABLE "Task" ADD COLUMN IF NOT EXISTS next_occurrence TIMESTAMP NULL;'))
            print("  ✅ next_occurrence")
            
            conn.commit()
            print("\n✅ PostgreSQL migration completed!")
        else:
            print("❌ This script is for PostgreSQL only (AKS)")
            exit(1)
        
        # Verify
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'Task' AND column_name IN ('due_date', 'remind_at', 'recurrence', 'next_occurrence')
            ORDER BY column_name;
        """))
        
        existing = [row[0] for row in result]
        phase5_cols =  ['due_date', 'remind_at', 'recurrence', 'next_occurrence']
        
        print("\n📋 Verification:")
        for col in phase5_cols:
            status = "✓" if col in existing else "✗"
            print(f"   {status} {col}")
        
        if all(col in existing for col in phase5_cols):
            print("\n🎉 All Phase 5 columns ready!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        conn.rollback()
        raise

print("\n✨ Migration complete!")
