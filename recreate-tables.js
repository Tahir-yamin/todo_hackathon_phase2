const { Pool } = require('pg');

const pool = new Pool({
    connectionString: 'postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.c-3.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require',
    ssl: { rejectUnauthorized: false }
});

async function recreateTables() {
    const client = await pool.connect();

    try {
        console.log('🔄 Dropping existing tables...');

        // Drop existing tables
        await client.query(`
      DROP TABLE IF EXISTS "verification" CASCADE;
      DROP TABLE IF EXISTS "session" CASCADE;
      DROP TABLE IF EXISTS "account" CASCADE;
      DROP TABLE IF EXISTS "user" CASCADE;
    `);

        console.log('✅ Tables dropped');
        console.log('🔄 Creating Better Auth tables with correct schema...');

        // Create user table with ALL required columns
        await client.query(`
      CREATE TABLE "user" (
        "id" TEXT PRIMARY KEY,
        "email" TEXT NOT NULL UNIQUE,
        "emailVerified" BOOLEAN NOT NULL DEFAULT false,
        "name" TEXT,
        "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        "image" TEXT,
        "twoFactorEnabled" BOOLEAN DEFAULT false
      );
    `);

        // Create session table
        await client.query(`
      CREATE TABLE "session" (
        "id" TEXT PRIMARY KEY,
        "userId" TEXT NOT NULL,
        "expiresAt" TIMESTAMP NOT NULL,
        "ipAddress" TEXT,
        "userAgent" TEXT,
        "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY ("userId") REFERENCES "user"("id") ON DELETE CASCADE
      );
    `);

        // Create account table
        await client.query(`
      CREATE TABLE "account" (
        "id" TEXT PRIMARY KEY,
        "userId" TEXT NOT NULL,
        "accountId" TEXT NOT NULL,
        "providerId" TEXT NOT NULL,
        "accessToken" TEXT,
        "refreshToken" TEXT,
        "idToken" TEXT,
        "expiresAt" TIMESTAMP,
        "password" TEXT,
        "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY ("userId") REFERENCES "user"("id") ON DELETE CASCADE
      );
    `);

        // Create verification table
        await client.query(`
      CREATE TABLE "verification" (
        "id" TEXT PRIMARY KEY,
        "identifier" TEXT NOT NULL,
        "value" TEXT NOT NULL,
        "expiresAt" TIMESTAMP NOT NULL,
        "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
    `);

        // Create indexes
        await client.query(`
      CREATE INDEX "idx_session_userId" ON "session"("userId");
      CREATE INDEX "idx_account_userId" ON "account"("userId");
      CREATE INDEX "idx_verification_identifier" ON "verification"("identifier");
    `);

        console.log('✅ All tables created successfully!');

        // Verify
        const result = await client.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public' 
      AND table_name IN ('user', 'session', 'account', 'verification')
      ORDER BY table_name;
    `);

        console.log('\n📋 Tables created:');
        result.rows.forEach(row => {
            console.log(`   ✓ ${row.table_name}`);
        });

        console.log('\n🎉 Database setup complete!');
        console.log('Restart the frontend and test at: http://localhost:3002/auth');

    } catch (error) {
        console.error('❌ Error:', error.message);
        throw error;
    } finally {
        client.release();
        await pool.end();
    }
}

recreateTables().catch(console.error);
