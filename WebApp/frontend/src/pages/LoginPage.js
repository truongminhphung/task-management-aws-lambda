import React from 'react';
import { useNavigate } from 'react-router-dom';
import Login from '../components/auth/Login';
import { login } from '../services/api';

const LoginPage = () => {
    const navigate = useNavigate();

    const handleLogin = async (username, password) => {
        await login(username, password); // call the login function from api.js
        navigate('/home'); // redirect to home page on successful login
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