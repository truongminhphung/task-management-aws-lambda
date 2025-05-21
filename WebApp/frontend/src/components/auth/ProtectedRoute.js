import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();
  
  console.log('ProtectedRoute - Auth state:', { isAuthenticated, isLoading, path: location.pathname });

  if (isLoading) {
    console.log('ProtectedRoute - Still loading auth state');
    // You can show a loading spinner here while checking authentication
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (!isAuthenticated) {
    console.log('ProtectedRoute - Not authenticated, redirecting to login');
    // Redirect to login page if not authenticated, preserving the intended destination
    return <Navigate to="/" state={{ from: location }} replace />;
  }

  console.log('ProtectedRoute - Authentication passed, rendering protected content');
  return children;
};

export default ProtectedRoute;