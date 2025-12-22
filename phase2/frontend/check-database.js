const { Pool } = require('pg');

const connectionString = 'postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.c-3.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require';

async function checkDatabase() {
    const pool = new Pool({
        connectionString,
        ssl: { rejectUnauthorized: false }
    });

    try {
        console.log('Checking better-auth database...\n');

        // Check if user table exists
        const userTableCheck = await pool.query(`
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'user'
            )
        `);
        console.log('User table exists:', userTableCheck.rows[0].exists);

        // Check if account table exists
        const accountTableCheck = await pool.query(`
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'account'
            )
        `);
        console.log('Account table exists:', accountTableCheck.rows[0].exists);

        // List all users
        const users = await pool.query('SELECT id, email, name, "emailVerified" FROM "user"');
        console.log('\nUsers in database:', users.rowCount);
        users.rows.forEach(user => {
            console.log(`  - ${user.email} (ID: ${user.id}, Verified: ${user.emailVerified})`);
        });

        // List all accounts (where password is stored)
        const accounts = await pool.query(`
            SELECT id, "userId", "providerId", "accountId" 
            FROM "account" 
            WHERE "providerId" = 'credential'
        `);
        console.log('\nAccounts (credential provider):', accounts.rowCount);
        accounts.rows.forEach(account => {
            console.log(`  - User ID: ${account.userId}, Account ID: ${account.accountId}`);
        });

        // Check for apitest@example.com specifically
        const apitestUser = await pool.query(`
            SELECT u.*, a.password IS NOT NULL as has_password
            FROM "user" u
            LEFT JOIN "account" a ON u.id = a."userId" AND a."providerId" = 'credential'
            WHERE u.email = 'apitest@example.com'
        `);

        if (apitestUser.rowCount > 0) {
            console.log('\napitest@example.com found:');
            console.log('  - Has password:', apitestUser.rows[0].has_password);
            console.log('  - Email verified:', apitestUser.rows[0].emailVerified);
        } else {
            console.log('\n❌ apitest@example.com NOT found in database!');
        }

    } catch (error) {
        console.error('❌ Database check failed:', error.message);
        throw error;
    } finally {
        await pool.end();
    }
}

checkDatabase();
