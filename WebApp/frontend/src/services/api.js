import axios from 'axios';

// Use the correct URL format that matches your backend
const API_URL = 'http://127.0.0.1:3000/task-management';

const api = axios.create({
    baseURL: API_URL,
    withCredentials: true, // Include cookies (JWT is HTTP-only) => it tells Axios to include cookies when making cross-origin requests.
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a response interceptor to handle authentication errors
api.interceptors.response.use(
    response => response,
    error => {
        // If 401 Unauthorized, the token might have expired
        if (error.response && error.response.status === 401) {
            console.log('Authentication error:', error.response.data);
            // You could redirect to login here if needed
        }
        return Promise.reject(error);
    }
);

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
export const getTasks = async () => {
    try {
        const response = await api.get('/tasks');
        return response.data;
    } catch (error) {
        console.error('Error fetching tasks:', error);
        if (error.response) {
            throw error.response.data;
        }
        throw error;
    }
}

export const createTask = async (task) => {
    try {
        const response = await api.post('/tasks', task);
        return response.data;
    } catch (error) {
        console.error('Error creating task:', error);
        if (error.response) {
            throw error.response.data;
        }
        throw error;
    }
}

export const updateTask = async (taskId, updateTask) => {
    try {
        const response = await api.put(`/tasks/${taskId}`, updateTask);
        return response.data;
    }
    catch (error) {
        console.error('Error updating task:', error);
        if (error.response) {
            throw error.response.data;
        }
        throw error;
    }
}

export const deleteTask = async (taskId) => {
    try {
        const response = await api.delete(`/tasks/${taskId}`);
        return response.data;
    } catch (error) {
        console.error('Error deleting task:', error);
        if (error.response) {
            throw error.response.data;
        }
        throw error;
    }
}

export const getUserProfile = async () => {
    try {
        const response = await api.get('/user/profile');
        return response.data;
    } catch (error) {
        console.error('Error fetching user profile:', error);
        if (error.response) {
            throw error.response.data;
        }
        throw error;
    }
};

export const uploadUserProfileImage = async (imageData) => {
    try {
        const response = await api.post('/user/profile/image', { image: imageData });
        return response.data;
    } catch (error) {
        console.error('Error uploading user profile image:', error);
        if (error.response) {
            throw error.response.data;
        }
        throw error;
    }
}