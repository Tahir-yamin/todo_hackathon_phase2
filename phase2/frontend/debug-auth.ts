// debug-auth.ts
const { PrismaClient } = require('@prisma/client');

async function test() {
  console.log("1. Initializing Prisma...");
  try {
    const prisma = new PrismaClient({
      datasourceUrl: process.env.DATABASE_URL,
    });
    await prisma.$connect();
    console.log("✅ Prisma Connection SUCCESS");
    await prisma.$disconnect();
  } catch (e) {
    console.error("❌ Prisma CRASHED:", e);
  }
}

test();
