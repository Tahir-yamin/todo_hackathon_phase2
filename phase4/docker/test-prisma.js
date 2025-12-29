const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();
console.log('Attempting to connect...');
prisma.$connect()
    .then(() => {
        console.log('Successfully connected to the database');
        process.exit(0);
    })
    .catch(err => {
        console.log('---ERROR_START---');
        console.log('Message:', err.message);
        console.log('Stack:', err.stack);
        console.log('---ERROR_END---');
        process.exit(1);
    });
