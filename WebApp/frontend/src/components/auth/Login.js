import React, { useState } from 'react';

/**
 * Login component for user authentication
 * 
 * @component
 * @param {Object} props - Component props
 * @param {Function} props.onLogin - Function to handle login authentication
 *                                   Expected to accept username and password parameters
 *                                   and throw an error with 'error' property if authentication fails
 * @returns {JSX.Element} A login form with username and password inputs
 * 
 * @example
 * const handleLogin = async (username, password) => {
 *   // Authentication logic
 * };
 * 
 * <Login onLogin={handleLogin} />
 */
const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors
    try {
      await onLogin(username, password);
    } catch (err) {
      setError(err.error || 'An error occurred during login');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', margin: '8px 0' }}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', margin: '8px 0' }}
          />
        </div>
        <button type="submit" style={{ padding: '10px 20px', background: '#007bff', color: 'white', border: 'none' }}>
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;