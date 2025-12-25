const { Pool } = require('pg');

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false }
});

async function createBetterAuthTables() {
    try {
        // Create account table for OAuth linking
        await pool.query(`
            CREATE TABLE IF NOT EXISTS account (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                provider TEXT NOT NULL,
                provider_account_id TEXT NOT NULL,
                access_token TEXT,
                refresh_token TEXT,
                expires_at BIGINT,
                token_type TEXT,
                scope TEXT,
                id_token TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(provider, provider_account_id)
            );
        `);
        console.log('✅ Account table created/verified');

        // Create verification table for email verification
        await pool.query(`
            CREATE TABLE IF NOT EXISTS verification (
                id TEXT PRIMARY KEY,
                identifier TEXT NOT NULL,
                value TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        `);
        console.log('✅ Verification table created/verified');

        // Check what tables now exist
        const tables = await pool.query(`SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'`);
        console.log('\n📊 Database tables:', tables.rows.map(r => r.table_name).join(', '));

    } catch (error) {
        console.error('❌ Error:', error.message);
    } finally {
        await pool.end();
    }
}

createBetterAuthTables();
