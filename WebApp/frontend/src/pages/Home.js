import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CreateTask from '../components/tasks/CreateTask';
import TaskItem from '../components/tasks/TaskItem';
import { getTasks, createTask, updateTask, deleteTask, getUserProfile, uploadUserProfileImage, logout as apiLogout } from '../services/api';
import { useAuth } from '../context/AuthContext';


const DEFAULT_USER_PROFILE_IMAGE = '/default_userprofile.png'; // Default image URL

const Home = () => {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);
  const [profileImage, setProfileImage] = useState(null);
  const [userEmail, setUserEmail] = useState(null);
  const [userName, setUserName] = useState(null);
  const [isDropDownOpen, setIsDropDownOpen] = useState(false);
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const { isAuthenticated } = useAuth();
  
  useEffect(() => {
    // Make sure the user is authenticated
    if (!isAuthenticated) {
      navigate('/');
      return;
    }
    
    // Fetch tasks on component mount
    const fetchTasks = async () => {
      try {
        const data = await getTasks();
        setTasks(data.tasks || []);
      } catch (err) {
        setError(err.error || 'Failed to fetch tasks');
      }
    };

    // Fetch user profile image data.profile && data.profile.profile_image_url
    const fetchUserProfile = async () => {
      try {
        const data = await getUserProfile();
        if (data.profile_image_url) {
          setProfileImage(data.profile_image_url);
        } else {
          setProfileImage(DEFAULT_USER_PROFILE_IMAGE);
        }
        setUserEmail(data.email)
        setUserName(data.username)
      } catch (err) {
        setError(err.error || 'Failed to fetch user profile');
      }
    };

    fetchTasks();
    fetchUserProfile();
  }, [isAuthenticated, navigate]);

  const handleAddTask = async (newTask) => {
    try {
      const response = await createTask(newTask);
      setTasks([...tasks, response.task]);
    } catch (err) {
      setError(err.error || 'Failed to create task');
    }
  };

  const handleUpdateTask = async (taskId, updatedTask) => {
    try {
      await updateTask(taskId, updatedTask);
      setTasks(tasks.map(task => (task.task_id === taskId ? { ...task, ...updatedTask } : task)));
    } catch (err) {
      setError(err.error || 'Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await deleteTask(taskId);
      setTasks(tasks.filter(task => task.task_id !== taskId));
    } catch (err) {
      setError(err.error || 'Failed to delete task');
    }
  };

  // const handleLogout = () => {
  //   fetch('http://localhost:3000/logout', { method: 'POST', credentials: 'include' })
  //     .then(() => navigate('/'))
  //     .catch(err => console.error('Logout failed:', err));
  // };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // convert image to base64
    const reader = new FileReader();
    reader.onloadend = async () => {
      const base64String = reader.result;
      try {
        const response = await uploadUserProfileImage(base64String);
        setProfileImage(response.profile_image_url);
        setIsDropDownOpen(false);
      } catch (err) {
        setError(err.error || 'Failed to upload image');
      }
    };
    reader.readAsDataURL(file);
  }

  const { logout } = useAuth();
  
  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      // Call the API logout endpoint
      await apiLogout();
      // Update auth state using the context
      logout();
      // Navigate to login page
      navigate('/');
    } catch (err) {
      setError(err.error || 'Failed to logout');
      setIsLoggingOut(false);
    }
  }

return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100 p-3 sm:p-4 md:p-6">
      {/* Responsive container with reasonable max-width but fills available space */}
      <div className="w-full max-w-7xl mx-auto px-2 sm:px-4 md:px-6">
        {/* Header - responsive text size and padding */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4 sm:mb-6 md:mb-8">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-800">My Tasks</h1>
          <div className="relative">
            <img src={profileImage} 
            alt="Profile" 
            className="w-10 h-10 rounded-full cursor-pointer border-2 border-blue-500 hover:border-blue-600 transition-colors"
            onClick={() => setIsDropDownOpen(!isDropDownOpen)}
            />
            {isDropDownOpen && (
              <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl z-10 overflow-hidden border border-gray-200">
                {/* User info section with profile image */}
                <div className="bg-blue-50 px-4 py-3 border-b border-gray-200">
                  <div className="flex items-center space-x-3">
                    <img src={profileImage} alt="Profile" className="w-12 h-12 rounded-full border-2 border-blue-500" />
                    <div>
                      <p className="font-medium text-gray-900">{userName || 'testuser'}</p>
                      <p className="text-sm text-gray-600">{userEmail || 'testuser@gmail.com'}</p>
                    </div>
                  </div>
                </div>
                
                {/* Menu options */}
                <div className="py-1">
                  <button
                    onClick={() => fileInputRef.current.click()}
                    className="flex items-center w-full text-left px-4 py-2 text-gray-700 hover:bg-blue-50 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-3 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Upload Profile Image
                  </button>
                </div>
                
                {/* Logout section with separator */}
                <div className="border-t border-gray-200">
                  <button
                    onClick={handleLogout}
                    className="flex items-center w-full text-left px-4 py-2 text-red-600 hover:bg-red-50 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    {isLoggingOut ? 'Logging out...' : 'Logout'}
                  </button>
                </div>
              </div>
            )}
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
              ref={fileInputRef}
            />
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-3 mb-4 rounded">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* Layout grid for larger screens */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 md:gap-6">
          {/* Add Task Form - takes full width on mobile, sidebar on desktop */}
          <div className="lg:col-span-4 lg:sticky lg:top-4 lg:self-start">
            <CreateTask onAddTask={handleAddTask} />
          </div>

          {/* Task List - takes full width on mobile, main content on desktop */}
          <div className="lg:col-span-8">
            <div className="space-y-3 sm:space-y-4">
              <h2 className="text-xl font-semibold text-gray-700 mb-2 lg:mt-0">Your Tasks</h2>
              {tasks.length === 0 ? (
                <div className="bg-white p-6 rounded-lg shadow text-center">
                  <p className="text-gray-500">No tasks yet. Add one to get started!</p>
                </div>
              ) : (
                tasks.map(task => (
                  <TaskItem
                    key={task.task_id}
                    task={task}
                    onUpdate={handleUpdateTask}
                    onDelete={handleDeleteTask}
                  />
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Home;