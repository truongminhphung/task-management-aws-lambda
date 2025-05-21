import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Login from '../components/auth/Login';
import { login } from '../services/api';
import { useAuth } from '../context/AuthContext';

const LoginPage = () => {
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const location = useLocation();
    const { login: authLogin } = useAuth();

    // Get the intended destination (if redirected from protected route)
    const from = location.state?.from?.pathname || "/home";

    const handleLogin = async (username, password) => {
        if (!username || !password) {
            setError('Username and password are required');
            return;
        }

        try {
            const response = await login(username, password);
            
            // Check various possible token locations based on API response structure
            const token = response?.token || response?.data?.token || response?.auth_token;
            
            if (token) {
                authLogin(token);
                setError(null); // Clear any previous errors
                
                // Use setTimeout to ensure state updates before navigation
                setTimeout(() => {
                    window.location.href = '/home'; // Direct browser navigation as fallback
                }, 100);
            } else {
                console.error('No token in response:', response);
                setError('Login successful but no token received. Please check server response format.');
            }
        } catch (err) {
            console.error('Login error:', err);
            // Extract the error message from whatever structure it comes in
            let errorMessage = 'Login failed. Please check your credentials.';
            
            if (typeof err === 'string') {
                errorMessage = err;
            } else if (err && err.message) {
                errorMessage = err.message;
            } else if (err && err.error) {
                errorMessage = err.error;
            }
            
            setError(errorMessage);
        }
    };

    return (
        <div className="bg-gray-50 min-h-screen flex flex-col">
            <header className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8 text-indigo-600">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M6 6.878V6a2.25 2.25 0 0 1 2.25-2.25h7.5A2.25 2.25 0 0 1 18 6v.878m-12 0c.235-.083.487-.128.75-.128h10.5c.263 0 .515.045.75.128m-12 0A2.25 2.25 0 0 0 4.5 9v.878m13.5-3A2.25 2.25 0 0 1 19.5 9v.878m0 0A2.25 2.25 0 0 0 18 13.5h-1.5m-15 0A2.25 2.25 0 0 1 4.5 12m0 0V8.375c0-.621.504-1.125 1.125-1.125h9.75c.621 0 1.125.504 1.125 1.125V12m-8.25 0h3.75m-6.75 3.75h9" />
                            </svg>
                            <h1 className="text-xl font-semibold text-gray-900">Task Management System</h1>
                        </div>
                    </div>
                </div>
            </header>

            <main className="flex-grow">
                {/* Display the error at the page level for better visibility */}
                {error && (
                    <div className="max-w-md mx-auto mt-4 rounded-md bg-red-50 p-4">
                        <div className="flex">
                            <div className="flex-shrink-0">
                                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clipRule="evenodd" />
                                </svg>
                            </div>
                            <div className="ml-3">
                                <p className="text-sm font-medium text-red-800">{error}</p>
                            </div>
                        </div>
                    </div>
                )}
                <Login onLogin={handleLogin} />
            </main>

            <footer className="bg-white border-t border-gray-200 py-4">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <p className="text-center text-sm text-gray-500">
                        © {new Date().getFullYear()} Task Management System. All rights reserved.
                    </p>
                </div>
            </footer>
        </div>
    );
}

export default LoginPage;