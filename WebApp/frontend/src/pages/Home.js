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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">My Tasks</h1>
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
          >
            Logout
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <p className="text-center text-red-500 mb-4">{error}</p>
        )}

        {/* Add Task Form */}
        <CreateTask onAddTask={handleAddTask} />

        {/* Task List */}
        <div className="space-y-4">
          {tasks.length === 0 ? (
            <p className="text-center text-gray-500">No tasks yet. Add one to get started!</p>
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
  );
};
export default Home;