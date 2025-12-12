// Test Better Auth signup with a new email
const testSignup = async () => {
    const randomEmail = `user${Date.now()}@example.com`;

    try {
        const response = await fetch('http://localhost:3002/api/auth/sign-up/email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: randomEmail,
                password: 'password123',
                name: 'Test User',
            }),
        });

        const data = await response.json();

        console.log('Status:', response.status);
        console.log('Email used:', randomEmail);
        console.log('Response:', JSON.stringify(data, null, 2));

        if (!response.ok) {
            console.error('❌ Error:', data);
        } else {
            console.log('✅ SUCCESS! User created:', data);
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
};

testSignup();
