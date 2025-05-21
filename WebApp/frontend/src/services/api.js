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

// Add a request interceptor to include the JWT token in all requests
api.interceptors.request.use(
    config => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Add a response interceptor to handle authentication errors
api.interceptors.response.use(
    response => response,
    error => {
        // If 401 Unauthorized, the token might have expired
        if (error.response && error.response.status === 401) {
            console.log('Authentication error:', error.response.data);
            // Clear token and redirect to login
            localStorage.removeItem('authToken');
            window.location.href = '/';
        }
        return Promise.reject(error);
    }
);

export const login = async (username, password) => {
    try {
        console.log('API login call with:', username);
        const response = await api.post('/login', { username, password });
        
        console.log('API login raw response:', response);
        console.log('API login response data:', response.data);
        
        // Try to extract token from various possible locations in the response
        const token = response.data?.token || response.data?.auth_token;
        
        if (token) {
            console.log('Storing token in localStorage:', token);
            localStorage.setItem('authToken', token);
        } else {
            console.warn('⚠️ No token found in API response. Backend may need to be updated.');
            
            // For testing/debugging: Create a temporary fake token if none exists
            // REMOVE THIS IN PRODUCTION
            localStorage.setItem('authToken', 'temp-debug-token');
            
            // Add token to response for consistency
            response.data.token = 'temp-debug-token';
        }
        
        return response.data;
    }
    catch (error) {
        console.error('Login API error:', error);
        if (error.response) {
            // Format the error to ensure it has a message property
            const errorData = error.response.data;
            
            // Make sure we have a proper error object with a message
            if (typeof errorData === 'string') {
                throw new Error(errorData);
            } else if (errorData && (errorData.message || errorData.error)) {
                const errorMessage = errorData.message || errorData.error;
                const err = new Error(errorMessage);
                err.status = error.response.status;
                throw err;
            } else {
                const err = new Error(`Login failed with status ${error.response.status}`);
                err.status = error.response.status;
                throw err;
            }
        }
        throw new Error(error.message || 'An unexpected error occurred');
    }
}

export const logout = async () => {
    try {
        const response = await api.post('/logout');
        
        // Always clear the auth token on logout, even if API call fails
        localStorage.removeItem('authToken');
        
        return response.data;
    } catch (error) {
        console.error('Logout error:', error);
        
        // Still clear token even on error
        localStorage.removeItem('authToken');
        
        if (error.response) {
            throw error.response.data;
        }
        throw error;
    }
};

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