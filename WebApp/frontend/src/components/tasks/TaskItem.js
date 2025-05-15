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
    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-3 sm:p-4 bg-white shadow-md rounded-lg hover:shadow-lg transition-shadow">
      <div className="flex-1 mb-3 sm:mb-0">
        <h3 className="text-base sm:text-lg font-semibold text-gray-800">{task.description}</h3>
        <div className="flex flex-col sm:flex-row sm:gap-4 mt-1">
          <p className="text-xs sm:text-sm text-gray-500">
            Due: {task.due_date || 'No due date'}
          </p>
          <p className="text-xs sm:text-sm text-gray-500 flex items-center mt-1 sm:mt-0">
            Status:
            <span 
              className={`ml-1 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                task.status === 'completed' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
              }`}
            >
              {task.status}
            </span>
          </p>
        </div>
      </div>
      <div className="flex flex-wrap gap-2 w-full sm:w-auto">
        <button
          onClick={handleStatusToggle}
          className={`flex-1 sm:flex-initial px-3 py-1 rounded-md text-white text-xs sm:text-sm font-medium transition-colors ${
            task.status === 'pending' ? 'bg-green-500 hover:bg-green-600' : 'bg-yellow-500 hover:bg-yellow-600'
          }`}
        >
          {task.status === 'pending' ? 'Complete' : 'Reopen'}
        </button>
        <button
          onClick={handleDelete}
          className="flex-1 sm:flex-initial px-3 py-1 bg-red-500 text-white rounded-md text-xs sm:text-sm font-medium hover:bg-red-600 transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskItem;