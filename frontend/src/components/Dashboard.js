import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import ItemsList from './ItemsList';
import ItemForm from './ItemForm';
import Stats from './Stats';

function Dashboard() {
  const [activeTab, setActiveTab] = useState('items');
  const [editingItem, setEditingItem] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setShowForm(true);
    setActiveTab('form');
  };

  const handleFormSuccess = () => {
    setShowForm(false);
    setEditingItem(null);
    setActiveTab('items');
    setRefreshKey(prev => prev + 1);
  };

  const handleAddNew = () => {
    setEditingItem(null);
    setShowForm(true);
    setActiveTab('form');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <h1 className="text-2xl font-bold text-gray-900">
              Inventory Management System
            </h1>
            <div className="flex items-center gap-4">
              <span className="text-gray-700">Welcome, {user?.username}</span>
              <button
                onClick={handleLogout}
                className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('stats')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'stats'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setActiveTab('items')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'items'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Items
            </button>
            <button
              onClick={handleAddNew}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'form'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Add Item
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'stats' && <Stats />}
        {activeTab === 'items' && (
          <ItemsList 
            onEdit={handleEdit} 
            refreshKey={refreshKey}
            setRefreshKey={setRefreshKey}
          />
        )}
        {activeTab === 'form' && (
          <ItemForm 
            item={editingItem} 
            onSuccess={handleFormSuccess}
            onCancel={() => {
              setShowForm(false);
              setEditingItem(null);
              setActiveTab('items');
            }}
          />
        )}
      </div>
    </div>
  );
}

export default Dashboard;