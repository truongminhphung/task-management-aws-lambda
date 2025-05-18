import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CreateTask from '../components/tasks/CreateTask';
import TaskItem from '../components/tasks/TaskItem';
import { getTasks, createTask, updateTask, deleteTask, getUserProfile, uploadUserProfileImage } from '../services/api';


const DEFAULT_USER_PROFILE_IMAGE = 'https://www.gravatar.com/avatar/';

const Home = () => {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);
  const [profileImage, setProfileImage] = useState(null);
  const [isDropDownOpen, setIsDropDownOpen] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
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
        console.log('log User Profile:', data);
        if (data.profile_image_url) {
          console.log('data: ', data);
          console.log('log User Profile Image:', data.profile_image_url);
          setProfileImage(data.profile_image_url);
        } else {
          setProfileImage(DEFAULT_USER_PROFILE_IMAGE);
        }
      } catch (err) {
        setError(err.error || 'Failed to fetch user profile');
      }
    };

    fetchTasks();
    fetchUserProfile();
  }, []);

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

  const handleLogout = () => {
    fetch('http://localhost:3000/logout', { method: 'POST', credentials: 'include' })
      .then(() => navigate('/'))
      .catch(err => console.error('Logout failed:', err));
  };

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
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg z-10">
                <div className="py-2">
                  <button
                    onClick={() => fileInputRef.current.click()}
                    className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-blue-100"
                  >
                    Upload Profile Image
                  </button>
                  <button
                    onClick={handleLogout}
                    className="block w-full text-left px-4 py-2 text-red-500 hover:bg-red-100"
                  >
                    Logout
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