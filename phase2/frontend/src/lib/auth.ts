import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Create PostgreSQL connection pool for Neon
const pool = new Pool({
    connectionString: process.env.DATABASE_URL!,
    ssl: {
        rejectUnauthorized: false
    }
});

export const auth = betterAuth({
    database: pool,
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3002",
    emailAndPassword: {
        enabled: true,
        requireEmailVerification: false,
        minPasswordLength: 6,
        maxPasswordLength: 128,
    },
    secret: process.env.BETTER_AUTH_SECRET!,
    trustedOrigins: [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        process.env.NEXT_PUBLIC_APP_URL || "",
    ],
    session: {
        expiresIn: 60 * 60 * 24 * 7, // 7 days
        updateAge: 60 * 60 * 24, // 1 day
        cookieCache: {
            enabled: true,
            maxAge: 60 * 5 // 5 minutes
        }
    },
    advanced: {
        cookiePrefix: "better-auth",
        generateId: () => {
            return crypto.randomUUID();
        }
    }
});

export type Session = typeof auth.$Infer.Session;
