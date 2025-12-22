import { createAuthClient } from "better-auth/react";

// BetterAuth API routes are hosted in THIS Next.js app at /api/auth/*
// NOT on the Python backend - so baseURL should point to the frontend
export const authClient = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3002",
});

export const { signIn, signUp, signOut, useSession } = authClient;
