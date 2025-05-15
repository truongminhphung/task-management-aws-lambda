import React from 'react';

const TaskItem = ({ task, onUpdate, onDelete }) => {
  const handleStatusToggle = () => {
    // Only send the status field that's changing, not the entire task object
    onUpdate(task.task_id, { status: task.status === 'pending' ? 'completed' : 'pending' });
  };

  const handleDelete = () => {
    onDelete(task.task_id);
  };

  return (
    <div className="flex items-center justify-between p-4 bg-white shadow-md rounded-lg mb-4 hover:shadow-lg transition-shadow">
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-800">{task.description}</h3>
        <p className="text-sm text-gray-500">Due: {task.due_date || 'No due date'}</p>
        <p className="text-sm text-gray-500">Status: 
          <span className={`ml-1 ${task.status === 'completed' ? 'text-green-600' : 'text-yellow-600'}`}>
            {task.status}
          </span>
        </p>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={handleStatusToggle}
          className={`px-3 py-1 rounded-full text-white text-sm font-medium transition-colors ${
            task.status === 'pending' ? 'bg-green-500 hover:bg-green-600' : 'bg-yellow-500 hover:bg-yellow-600'
          }`}
        >
          {task.status === 'pending' ? 'Mark as Done' : 'Mark as Pending'}
        </button>
        <button
          onClick={handleDelete}
          className="px-3 py-1 bg-red-500 text-white rounded-full text-sm font-medium hover:bg-red-600 transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskItem;