const { Pool } = require('pg');

const pool = new Pool({
    connectionString: 'postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.c-3.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require',
    ssl: { rejectUnauthorized: false }
});

async function comprehensiveCheck() {
    const client = await pool.connect();

    try {
        console.log('🔍 COMPREHENSIVE DATABASE CHECK\n');
        console.log('='.repeat(60));

        // 1. List all tables
        console.log('\n📋 ALL TABLES IN DATABASE:');
        const tablesResult = await client.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public' 
      ORDER BY table_name
    `);
        console.table(tablesResult.rows);

        // 2. Check user table structure
        console.log('\n👤 USER TABLE STRUCTURE:');
        const userColumns = await client.query(`
      SELECT column_name, data_type, is_nullable, column_default
      FROM information_schema.columns 
      WHERE table_name = 'user' 
      ORDER BY ordinal_position
    `);
        console.table(userColumns.rows);

        // 3. Check Task table structure
        console.log('\n📝 TASK TABLE STRUCTURE:');
        const taskColumns = await client.query(`
      SELECT column_name, data_type, is_nullable, column_default
      FROM information_schema.columns 
      WHERE table_name = 'Task' 
      ORDER BY ordinal_position
    `);
        console.table(taskColumns.rows);

        // 4. Check for any users
        console.log('\n👥 USERS IN DATABASE:');
        const usersResult = await client.query('SELECT id, email, name FROM "user" LIMIT 5');
        console.table(usersResult.rows);

        // 5. Check for any tasks
        console.log('\n📋 TASKS IN DATABASE:');
        const tasksResult = await client.query('SELECT * FROM "Task" LIMIT 5');
        console.log('Total tasks:', tasksResult.rows.length);
        if (tasksResult.rows.length > 0) {
            console.table(tasksResult.rows);
        } else {
            console.log('No tasks found');
        }

        // 6. Check foreign key constraints
        console.log('\n🔗 FOREIGN KEY CONSTRAINTS:');
        const fkResult = await client.query(`
      SELECT
        tc.table_name, 
        kcu.column_name, 
        ccu.table_name AS foreign_table_name,
        ccu.column_name AS foreign_column_name 
      FROM information_schema.table_constraints AS tc 
      JOIN information_schema.key_column_usage AS kcu
        ON tc.constraint_name = kcu.constraint_name
        AND tc.table_schema = kcu.table_schema
      JOIN information_schema.constraint_column_usage AS ccu
        ON ccu.constraint_name = tc.constraint_name
        AND ccu.table_schema = tc.table_schema
      WHERE tc.constraint_type = 'FOREIGN KEY'
      AND tc.table_schema = 'public'
    `);
        console.table(fkResult.rows);

        console.log('\n' + '='.repeat(60));
        console.log('✅ CHECK COMPLETE\n');

    } catch (error) {
        console.error('❌ Error:', error.message);
    } finally {
        client.release();
        await pool.end();
    }
}

comprehensiveCheck();
