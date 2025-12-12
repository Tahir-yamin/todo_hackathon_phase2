// Test Better Auth login
const testLogin = async () => {
    try {
        const response = await fetch('http://localhost:3002/api/auth/sign-in/email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: 'user1765544484420@example.com', // User we just created
                password: 'password123',
            }),
        });

        const data = await response.json();

        console.log('Status:', response.status);
        console.log('Response:', JSON.stringify(data, null, 2));

        if (!response.ok) {
            console.error('❌ Login failed:', data);
        } else {
            console.log('✅ LOGIN SUCCESS!');
            console.log('Token:', data.token);
            console.log('User:', data.user);
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
};

testLogin();
