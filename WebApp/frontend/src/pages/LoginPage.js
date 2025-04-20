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
    return <Login onLogin={handleLogin} />;
}

export default LoginPage;