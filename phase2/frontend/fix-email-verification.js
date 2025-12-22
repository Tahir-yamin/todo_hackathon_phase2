const { Pool } = require('pg');

const connectionString = 'postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.c-3.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require';

async function fixEmailVerification() {
    const pool = new Pool({
        connectionString,
        ssl: { rejectUnauthorized: false }
    });

    try {
        console.log('Setting emailVerified=true for apitest@example.com...\n');

        const result = await pool.query(`
            UPDATE "user" 
            SET "emailVerified" = true 
            WHERE email = 'apitest@example.com'
            RETURNING id, email, "emailVerified"
        `);

        if (result.rowCount > 0) {
            console.log('✅ Updated successfully:');
            console.log(`   Email: ${result.rows[0].email}`);
            console.log(`   Verified: ${result.rows[0].emailVerified}`);
        } else {
            console.log('❌ No user found with that email');
        }

    } catch (error) {
        console.error('❌ Update failed:', error.message);
        throw error;
    } finally {
        await pool.end();
    }
}

fixEmailVerification();
