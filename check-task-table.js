const { Pool } = require('pg');

const pool = new Pool({
    connectionString: 'postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.c-3.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require',
    ssl: { rejectUnauthorized: false }
});

async function checkTaskTable() {
    const client = await pool.connect();

    try {
        console.log('📋 Checking Task table columns...\n');

        const result = await client.query(`
      SELECT column_name, data_type, is_nullable
      FROM information_schema.columns 
      WHERE table_name = 'Task' 
      ORDER BY ordinal_position
    `);

        console.log('Task table columns:');
        console.table(result.rows);

        // Check if there are any tasks
        const countResult = await client.query('SELECT COUNT(*) FROM "Task"');
        console.log('\nNumber of tasks:', countResult.rows[0].count);

    } catch (error) {
        console.error('Error:', error.message);
    } finally {
        client.release();
        await pool.end();
    }
}

checkTaskTable();
