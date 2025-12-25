import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import prisma from "./prisma";
import { Resend } from 'resend';

export const auth = betterAuth({
    database: prismaAdapter(prisma, {
        provider: "postgresql",
    }),
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3002",

    emailAndPassword: {
        enabled: true,
        requireEmailVerification: true, // 🔒 MANDATORY: No fake emails allowed!

        async sendVerificationEmail({ user, url, token }) {
            // 🖨️ ALWAYS log to terminal (for testing/debugging)
            console.log("\n👇 ===================================");
            console.log("📧 VERIFICATION EMAIL TO:", user.email);
            console.log("🔗 CLICK THIS LINK TO VERIFY:", url);
            console.log("👆 ===================================\n");

            // 🚀 OPTIONAL: Send real email via Resend (if API key exists)
            if (process.env.RESEND_API_KEY) {
                try {
                    const resend = new Resend(process.env.RESEND_API_KEY);
                    await resend.emails.send({
                        from: process.env.EMAIL_FROM || "onboarding@resend.dev",
                        to: user.email,
                        subject: "Verify your email for Todo App",
                        html: `
                            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                                <h2>Welcome to Todo App!</h2>
                                <p>Click the button below to verify your email address:</p>
                                <a href="${url}" style="display: inline-block; padding: 12px 24px; background-color: #8b5cf6; color: white; text-decoration: none; border-radius: 8px; margin: 20px 0;">
                                    Verify Email
                                </a>
                                <p style="color: #666; font-size: 14px;">If you didn't create an account, you can safely ignore this email.</p>
                            </div>
                        `,
                    });
                    console.log("✅ Real email sent via Resend to:", user.email);
                } catch (e) {
                    console.error("❌ Resend failed (user can still use terminal link):", e);
                }
            }
        },
    },

    socialProviders: {
        google: {
            clientId: process.env.GOOGLE_CLIENT_ID!,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
        },
        github: {
            clientId: process.env.GITHUB_CLIENT_ID!,
            clientSecret: process.env.GITHUB_CLIENT_SECRET!,
        },
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
});

export type Session = typeof auth.$Infer.Session;
