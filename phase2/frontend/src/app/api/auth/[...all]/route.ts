import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";
import { NextRequest } from "next/server";

const handler = toNextJsHandler(auth);

// Wrap with error logging
export async function GET(req: NextRequest) {
    try {
        console.log('🔍 BetterAuth GET request:', req.url);
        return await handler.GET(req);
    } catch (error: any) {
        console.error('❌ BetterAuth GET Error:', error);
        console.error('Stack:', error.stack);
        return new Response(JSON.stringify({ error: error.message }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

export async function POST(req: NextRequest) {
    try {
        console.log('🔍 BetterAuth POST request:', req.url);
        const body = await req.clone().json().catch(() => ({}));
        console.log('📝 Request body:', JSON.stringify(body, null, 2));
        return await handler.POST(req);
    } catch (error: any) {
        console.error('❌ BetterAuth POST Error:', error);
        console.error('Error message:', error.message);
        console.error('Stack:', error.stack);
        return new Response(JSON.stringify({
            error: error.message,
            details: error.toString()
        }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}
