const { Pool } = require('pg');

const pool = new Pool({
    connectionString: 'postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.c-3.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require',
    ssl: { rejectUnauthorized: false }
});

async function createTaskTable() {
    const client = await pool.connect();

    try {
        console.log('🔄 Creating Task table...');

        // Create Task table
        await client.query(`
      CREATE TABLE IF NOT EXISTS "Task" (
        "id" TEXT PRIMARY KEY,
        "user_id" TEXT NOT NULL,
        "title" TEXT NOT NULL,
        "description" TEXT,
        "status" TEXT NOT NULL DEFAULT 'pending',
        "priority" TEXT NOT NULL DEFAULT 'medium',
        "due_date" TIMESTAMP,
        "category" TEXT,
        "tags" TEXT,
        "completed_at" TIMESTAMP,
        "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY ("user_id") REFERENCES "user"("id") ON DELETE CASCADE
      );
    `);

        // Create index for faster queries
        await client.query(`
      CREATE INDEX IF NOT EXISTS "idx_task_user_id" ON "Task"("user_id");
      CREATE INDEX IF NOT EXISTS "idx_task_status" ON "Task"("status");
    `);

        console.log('✅ Task table created successfully!');

        // Verify
        const result = await client.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public' 
      AND table_name = 'Task';
    `);

        if (result.rows.length > 0) {
            console.log('✅ Task table verified!');
        }

        console.log('\n🎉 Database setup complete!');
        console.log('All tables ready for use.');

    } catch (error) {
        console.error('❌ Error:', error.message);
        throw error;
    } finally {
        client.release();
        await pool.end();
    }
}

createTaskTable().catch(console.error);
