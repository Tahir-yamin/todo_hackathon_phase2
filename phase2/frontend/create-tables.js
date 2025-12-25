const { Pool } = require('pg');

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false }
});

async function createTables() {
    try {
        // Create user table
        await pool.query(`
            CREATE TABLE IF NOT EXISTS "user" (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                email_verified BOOLEAN DEFAULT FALSE NOT NULL,
                image TEXT,
                created_at TIMESTAMP DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP DEFAULT NOW() NOT NULL
            )
        `);
        console.log('✅ User table created');

        // Create session table
        await pool.query(`
            CREATE TABLE IF NOT EXISTS "session" (
                id TEXT PRIMARY KEY,
                expires_at TIMESTAMP NOT NULL,
                token TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP DEFAULT NOW() NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE
            )
        `);
        await pool.query(`CREATE INDEX IF NOT EXISTS session_userId_idx ON "session"(user_id)`);
        console.log('✅ Session table created');

        // Create account table for OAuth
        await pool.query(`
            CREATE TABLE IF NOT EXISTS "account" (
                id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                provider_id TEXT NOT NULL,
                user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                access_token TEXT,
                refresh_token TEXT,
                id_token TEXT,
                access_token_expires_at TIMESTAMP,
                refresh_token_expires_at TIMESTAMP,
                scope TEXT,
                password TEXT,
                created_at TIMESTAMP DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP DEFAULT NOW() NOT NULL
            )
        `);
        await pool.query(`CREATE INDEX IF NOT EXISTS account_userId_idx ON "account"(user_id)`);
        console.log('✅ Account table created (OAuth linking enabled!)');

        // Create verification table
        await pool.query(`
            CREATE TABLE IF NOT EXISTS "verification" (
                id TEXT PRIMARY KEY,
                identifier TEXT NOT NULL,
                value TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP DEFAULT NOW() NOT NULL
            )
        `);
        await pool.query(`CREATE INDEX IF NOT EXISTS verification_identifier_idx ON "verification"(identifier)`);
        console.log('✅ Verification table created');

        console.log('\n🎉 All BetterAuth tables created successfully!');

        const tables = await pool.query(
            'SELECT table_name FROM information_schema.tables WHERE table_schema = $1 ORDER BY table_name',
            ['public']
        );
        console.log('\n📊 Database tables:', tables.rows.map(r => r.table_name).join(', '));
    } catch (error) {
        if (error.message.includes('already exists')) {
            console.log('ℹ️  Tables already exist, skipping creation');
        } else {
            console.error('❌ Error:', error.message);
        }
    } finally {
        await pool.end();
    }
}

createTables();
