const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

// Read the SQL file
const sqlFile = path.join(__dirname, 'better-auth-schema.sql');
const sql = fs.readFileSync(sqlFile, 'utf8');

// Create connection pool
const pool = new Pool({
    connectionString: 'postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.c-3.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require',
    ssl: {
        rejectUnauthorized: false
    }
});

async function createTables() {
    const client = await pool.connect();

    try {
        console.log('🔄 Connecting to Neon database...');

        // Execute the SQL script
        await client.query(sql);

        console.log('✅ Better Auth tables created successfully!');

        // Verify tables were created
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
        console.log('You can now test Better Auth at: http://localhost:3002/auth');

    } catch (error) {
        console.error('❌ Error creating tables:', error.message);
        throw error;
    } finally {
        client.release();
        await pool.end();
    }
}

createTables().catch(console.error);
