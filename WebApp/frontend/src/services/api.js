import axios from 'axios';

// Use the correct URL format that matches your backend
const API_URL = 'http://127.0.0.1:3000/task-management';

const api = axios.create({
    baseURL: API_URL,
    withCredentials: true, // Include cookies (JWT is HTTP-only)
    headers: {
        'Content-Type': 'application/json',
    },
});

export const login = async (username, password) => {
    try {
        const response = await api.post('/login', { username, password });
        return response.data;
    }
    catch (error) {
        console.error('Login error:', error);
        if (error.response) {
            throw error.response.data;
        }
        throw error;
    }
}