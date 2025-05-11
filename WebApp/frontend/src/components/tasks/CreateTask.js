import React, { useState } from 'react';

const CreateTask = ({ onAddTask }) => {
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!description.trim()) return;
    onAddTask({
      description,
      due_date: dueDate || null,
      status: 'pending',
    });
    setDescription('');
    setDueDate('');
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-6 bg-gradient-to-r from-blue-100 to-blue-200 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Add a New Task</h2>
      <div className="mb-4">
        <label className="block text-gray-700 font-medium mb-1">Description</label>
        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description"
          className="w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 font-medium mb-1">Due Date (optional)</label>
        <input
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
      >
        Add Task
      </button>
    </form>
  );
};

export default CreateTask;