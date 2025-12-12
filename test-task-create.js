// Test creating a task with corrected endpoints
const testCreateTask = async () => {
    try {
        // First, get a session token by logging in
        const loginResponse = await fetch('http://localhost:3002/api/auth/sign-in/email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: 'user1765544484420@example.com',
                password: 'password123',
            }),
        });

        const loginData = await loginResponse.json();
        const token = loginData.token;
        const userId = loginData.user.id;

        console.log('✅ Logged in, User ID:', userId);
        console.log('Token:', token);

        // Now try to create a task using CORRECT endpoint
        const createResponse = await fetch(`http://localhost:8002/api/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({
                title: 'Test Task from API',
                description: 'Testing task creation with Better Auth',
                priority: 'high',
                status: 'pending',
            }),
        });

        console.log('\n📝 Create Task Status:', createResponse.status);

        if (createResponse.ok) {
            const createData = await createResponse.json();
            console.log('✅ SUCCESS! Task created');
            console.log('Response:', JSON.stringify(createData, null, 2));

            // Now try to fetch tasks
            const fetchResponse = await fetch(`http://localhost:8002/api/tasks`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });

            console.log('\n📋 Fetch Tasks Status:', fetchResponse.status);
            if (fetchResponse.ok) {
                const fetchData = await fetchResponse.json();
                console.log('✅ Tasks fetched successfully');
                console.log('Tasks:', JSON.stringify(fetchData, null, 2));
            }
        } else {
            const errorData = await createResponse.json();
            console.log('❌ Failed to create task');
            console.log('Error:', JSON.stringify(errorData, null, 2));
        }

    } catch (error) {
        console.error('❌ Error:', error.message);
    }
};

testCreateTask();
