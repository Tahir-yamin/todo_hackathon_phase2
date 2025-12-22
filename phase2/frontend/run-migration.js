const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

const connectionString = 'postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.c-3.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require';

async function runMigration() {
    const pool = new Pool({
        connectionString,
        ssl: { rejectUnauthorized: false }
    });

    try {
        const sql = fs.readFileSync(path.join(__dirname, 'better-auth-schema.sql'), 'utf8');

        console.log('Running better-auth schema migration...');
        await pool.query(sql);
        console.log('✅ Migration completed successfully!');

        // Verify tables were created
        const result = await pool.query(`
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('user', 'session', 'account', 'verification')
            ORDER BY table_name
        `);

        console.log('Created tables:');
        result.rows.forEach(row => console.log(`  - ${row.table_name}`));

    } catch (error) {
        console.error('❌ Migration failed:', error.message);
        throw error;
    } finally {
        await pool.end();
    }
}

runMigration();
