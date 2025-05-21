import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  
  console.log('AuthProvider initialized');
  
  useEffect(() => {
    // Check authentication status on mount
    const checkAuthStatus = async () => {
      try {
        console.log('Checking authentication status...');
        const token = localStorage.getItem('authToken');
        console.log('Token found in storage:', !!token);
        
        // If token exists, set authenticated to true
        if (token) {
          console.log('Setting authenticated to true');
          setIsAuthenticated(true);
        } else {
          console.log('Setting authenticated to false');
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        setIsAuthenticated(false);
      } finally {
        console.log('Finished auth check, setting loading to false');
        setIsLoading(false);
      }
    };
    
    checkAuthStatus();
  }, []);

  const login = (token) => {
    console.log('AuthContext login called with token:', token);
    localStorage.setItem('authToken', token);
    setIsAuthenticated(true);
    console.log('Authentication state updated to:', true);
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};