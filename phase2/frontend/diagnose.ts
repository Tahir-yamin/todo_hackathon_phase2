// diagnose.ts
console.log("1. Starting Diagnostic...");

// Manually load env vars (simulating Next.js)
const fs = require('fs');
const path = require('path');
const envPath = path.resolve(__dirname, '.env.local');

if (fs.existsSync(envPath)) {
    console.log("2. Loading .env.local...");
    const envConfig = require('dotenv').parse(fs.readFileSync(envPath));
    for (const k in envConfig) {
        process.env[k] = envConfig[k];
    }
} else {
    console.error("❌ CRITICAL: .env.local file NOT FOUND!");
    process.exit(1);
}

// Check Critical Vars
const required = ['BETTER_AUTH_SECRET', 'DATABASE_URL', 'GOOGLE_CLIENT_ID', 'GITHUB_CLIENT_ID'];
const missing = required.filter(key => !process.env[key]);

if (missing.length > 0) {
    console.error("❌ CRITICAL: Missing ENV Vars:", missing);
    process.exit(1);
}
console.log("3. Env Vars OK.");

// Attempt Import
try {
    console.log("4. Importing Prisma...");
    const { PrismaClient } = require('@prisma/client');
    const prisma = new PrismaClient();

    console.log("5. Importing Auth Config...");
    // We use require to catch the error during load
    const authModule = require('./src/lib/auth');

    console.log("✅ SUCCESS: Auth module loaded without crashing!");
    console.log("Auth Object keys:", Object.keys(authModule.auth));
} catch (error) {
    console.error("\n🔥🔥🔥 DIAGNOSTIC CAUGHT THE ERROR 🔥🔥🔥");
    console.error("----------------------------------------");
    console.error(error);
    console.error("----------------------------------------");
}
