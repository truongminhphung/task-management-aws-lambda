import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CreateTask from '../components/tasks/CreateTask';
import TaskItem from '../components/tasks/TaskItem';
import { getTasks, createTask, updateTask, deleteTask } from '../services/api';


// const mockTasks = [
//   {
//     task_id: 1,
//     description: "Buy groceries",
//     due_date: "2025-04-15",
//     status: "pending",
//     created_at: "2025-04-01T10:00:00Z",
//     updated_at: "2025-04-01T10:00:00Z",
//   },
//   {
//     task_id: 2,
//     description: "Finish project report",
//     due_date: "2025-04-20",
//     status: "pending",
//     created_at: "2025-04-02T12:00:00Z",
//     updated_at: "2025-04-02T12:00:00Z",
//   },
//   {
//     task_id: 3,
//     description: "Call dentist",
//     due_date: "2025-04-10",
//     status: "completed",
//     created_at: "2025-03-30T09:00:00Z",
//     updated_at: "2025-04-01T14:00:00Z",
//   },
// ];

const Home = () => {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);
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
    fetchTasks();
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

return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100 p-3 sm:p-4 md:p-6">
      {/* Responsive container with reasonable max-width but fills available space */}
      <div className="w-full max-w-7xl mx-auto px-2 sm:px-4 md:px-6">
        {/* Header - responsive text size and padding */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4 sm:mb-6 md:mb-8">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-800">My Tasks</h1>
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-3 py-1.5 sm:px-4 sm:py-2 rounded-lg hover:bg-red-600 transition-colors text-sm sm:text-base"
          >
            Logout
          </button>
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