#!/usr/bin/env python3
"""
Phase 5 Database Migration
Adds missing columns for recurring tasks and reminders.
Works with both SQLite (local) and PostgreSQL (AKS).
"""

from sqlmodel import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment")

print(f"🔧 Phase 5 Database Migration")
print(f"📊 Database: {DATABASE_URL[:50]}...")

engine = create_engine(DATABASE_URL)
is_postgres = "postgresql" in DATABASE_URL

def backup_reminder():
    if not is_postgres:
        print("\n⚠️  IMPORTANT: Backup your database before running this migration!")
        print("   On SQLite: copy todo.db to todo.db.backup")
        print("   On PostgreSQL: use pg_dump")
        response = input("\nHave you backed up your database? (yes/no): ")
        if response.lower() != "yes":
            print("❌ Migration cancelled. Please backup first.")
            exit(1)

def run_migration():
    print("\n🚀 Starting migration...")
    
    with engine.connect() as conn:
        try:
            if is_postgres:
                # PostgreSQL migration
                print("📝 Running PostgreSQL migration...")
                
                # Add remind_at if missing
                conn.execute(text("""
                    ALTER TABLE "Task" 
                    ADD COLUMN IF NOT EXISTS remind_at TIMESTAMP NULL;
                """))
                print("  ✅ remind_at column added/verified")
                
                # Add recurrence if missing
                conn.execute(text("""
                    ALTER TABLE "Task" 
                    ADD COLUMN IF NOT EXISTS recurrence VARCHAR(20) DEFAULT 'NONE';
                """))
                print("  ✅ recurrence column added/verified")
                
                # Add next_occurrence if missing
                conn.execute(text("""
                    ALTER TABLE "Task" 
                    ADD COLUMN IF NOT EXISTS next_occurrence TIMESTAMP NULL;
                """))
                print("  ✅ next_occurrence column added/verified")
                
                conn.commit()
                
            else:
                # SQLite migration
                print("📝 Running SQLite migration...")
                
                # Check which columns are missing
                result = conn.execute(text("PRAGMA table_info(Task);"))
                existing_cols = [row[1] for row in result]
                
                if "remind_at" not in existing_cols:
                    conn.execute(text("ALTER TABLE Task ADD COLUMN remind_at TIMESTAMP NULL;"))
                    print("  ✅ remind_at column added")
                else:
                    print("  ✅ remind_at already exists")
                
                if "recurrence" not in existing_cols:
                    conn.execute(text("ALTER TABLE Task ADD COLUMN recurrence VARCHAR(20) DEFAULT 'NONE';"))
                    print("  ✅ recurrence column added")
                else:
                    print("  ✅ recurrence already exists")
                
                if "next_occurrence" not in existing_cols:
                    conn.execute(text("ALTER TABLE Task ADD COLUMN next_occurrence TIMESTAMP NULL;"))
                    print("  ✅ next_occurrence column added")
                else:
                    print("  ✅ next_occurrence already exists")
                
                conn.commit()
            
            print("\n✅ Migration completed successfully!")
            
            # Verify migration
            print("\n📋 Verifying migration...")
            if is_postgres:
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'Task' 
                    AND column_name IN ('due_date', 'remind_at', 'recurrence', 'next_occurrence')
                    ORDER BY column_name;
                """))
            else:
                result = conn.execute(text("PRAGMA table_info(Task);"))
            
            phase5_columns = ['due_date', 'remind_at', 'recurrence', 'next_occurrence']
            existing = [row[0] if is_postgres else row[1] for row in result]
            
            all_present = all(col in existing for col in phase5_columns)
            
            if all_present:
                print("✅ All Phase 5 columns verified!")
                for col in phase5_columns:
                    print(f"   ✓ {col}")
            else:
                print("⚠️  Some columns may be missing:")
                for col in phase5_columns:
                    status = "✓" if col in existing else "✗"
                    print(f"   {status} {col}")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            print("Rolling back changes...")
            conn.rollback()
            raise

if __name__ == "__main__":
    backup_reminder()
    run_migration()
    print("\n🎉 Phase 5 migration complete! Your database is ready for recurring tasks and reminders.")
