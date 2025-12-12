const { Pool } = require('pg');

const pool = new Pool({
    connectionString: 'postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.c-3.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require',
    ssl: { rejectUnauthorized: false }
});

async function addMissingColumn() {
    const client = await pool.connect();

    try {
        console.log('🔄 Adding missing token column to session table...');

        await client.query(`
      ALTER TABLE "session" 
      ADD COLUMN IF NOT EXISTS "token" TEXT;
    `);

        console.log('✅ Token column added successfully!');
        console.log('🎉 Schema is now complete!');
        console.log('\nRestart frontend and test at: http://localhost:3002/auth');

    } catch (error) {
        console.error('❌ Error:', error.message);
        throw error;
    } finally {
        client.release();
        await pool.end();
    }
}

addMissingColumn().catch(console.error);
