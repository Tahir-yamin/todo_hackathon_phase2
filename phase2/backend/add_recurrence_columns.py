from db import engine
from sqlalchemy import text

print("Adding missing columns to Task table...")

with engine.connect() as conn:
    # Add recurrence column
    try:
        conn.execute(text('ALTER TABLE "Task" ADD COLUMN recurrence VARCHAR DEFAULT \'NONE\''))
        print('✅ Added recurrence column')
    except Exception as e:
        print(f'⚠️ recurrence column: {e}')
    
    # Add next_occurrence column  
    try:
        conn.execute(text('ALTER TABLE "Task" ADD COLUMN next_occurrence TIMESTAMP'))
        print('✅ Added next_occurrence column')
    except Exception as e:
        print(f'⚠️ next_occurrence column: {e}')
    
    conn.commit()
    print('✅ Database schema migration complete!')
