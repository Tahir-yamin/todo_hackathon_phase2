const { Pool } = require('pg');

const pool = new Pool({
    connectionString: 'postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.c-3.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require',
    ssl: { rejectUnauthorized: false }
});

async function setupDatabase() {
    console.log('🔄 Setting up BetterAuth database schema...\n');

    try {
        // Drop existing tables that might have wrong schema
        console.log('🗑️  Dropping old tables if they exist...');
        await pool.query('DROP TABLE IF EXISTS "verification" CASCADE');
        await pool.query('DROP TABLE IF EXISTS "account" CASCADE');
        await pool.query('DROP TABLE IF EXISTS "session" CASCADE');
        await pool.query('DROP TABLE IF EXISTS "user" CASCADE');
        console.log('✅ Old tables dropped\n');

        // Create user table
        console.log('📝 Creating user table...');
        await pool.query(`
            CREATE TABLE "user" (
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
        console.log('📝 Creating session table...');
        await pool.query(`
            CREATE TABLE "session" (
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
        await pool.query('CREATE INDEX session_userId_idx ON "session"(user_id)');
        console.log('✅ Session table created');

        // Create account table for OAuth
        console.log('📝 Creating account table...');
        await pool.query(`
            CREATE TABLE "account" (
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
        await pool.query('CREATE INDEX account_userId_idx ON "account"(user_id)');
        console.log('✅ Account table created **OAuth READY!**');

        // Create verification table
        console.log('📝 Creating verification table...');
        await pool.query(`
            CREATE TABLE "verification" (
                id TEXT PRIMARY KEY,
                identifier TEXT NOT NULL,
                value TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT NOW() NOT NULL,
                updated_at TIMESTAMP DEFAULT NOW() NOT NULL
            )
        `);
        await pool.query('CREATE INDEX verification_identifier_idx ON "verification"(identifier)');
        console.log('✅ Verification table created');

        console.log('\n🎉 All BetterAuth tables created successfully!\n');

        // Show all tables
        const result = await pool.query(`
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        `);
        console.log('📊 Database tables:', result.rows.map(r => r.table_name).join(', '));

        console.log('\n✅ Database ready for OAuth & email verification!');
    } catch (error) {
        console.error('\n❌ Error:', error.message);
        console.error('Details:', error);
    } finally {
        await pool.end();
    }
}

setupDatabase();
