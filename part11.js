// frontend/src/pages/DashboardPage.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function DashboardPage() {
  const [inventoryChanges, setInventoryChanges] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchInventoryChanges = async () => {
      try {
        const response = await axios.get('http://localhost:8000/inventory-changes/');
        setInventoryChanges(response.data);
      } catch (err) {
        console.error('Error fetching inventory changes:', err);
        setError('Failed to load inventory data. Please upload a CSV first.');
      } finally {
        setLoading(false);
      }
    };

    fetchInventoryChanges();
  }, []);

  if (loading) {
    return (
      <div className="text-center text-gray-600 mt-10">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-gray-900 mx-auto mb-4"></div>
        Loading dashboard data...
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-600 mt-10 p-4 bg-red-100 rounded-md">
        <p className="font-semibold text-lg mb-2">Error:</p>
        <p>{error}</p>
        <button
          onClick={() => window.location.href = '/'}
          className="mt-4 bg-blue-600 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-700 transition-colors duration-200"
        >
          Go to Upload Page
        </button>
      </div>
    );
  }

  if (!inventoryChanges) {
    return (
      <div className="text-center text-gray-600 mt-10 p-4 bg-gray-50 rounded-md">
        <p className="font-semibold text-lg mb-2">No inventory data available.</p>
        <p>Please upload your first CSV file to see dashboard insights.</p>
        <button
          onClick={() => window.location.href = '/'}
          className="mt-4 bg-blue-600 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-700 transition-colors duration-200"
        >
          Upload CSV Now
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-3xl font-bold mb-8 text-gray-800 text-center">Inventory Overview</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-blue-50 p-6 rounded-lg shadow-sm text-center">
          <p className="text-sm font-medium text-blue-700">New Items This Month</p>
          <p className="text-4xl font-bold text-blue-900 mt-2">{inventoryChanges.new_items_count}</p>
        </div>
        <div className="bg-red-50 p-6 rounded-lg shadow-sm text-center">
          <p className="text-sm font-medium text-red-700">Sold Items This Month</p>
          <p className="text-4xl font-bold text-red-900 mt-2">{inventoryChanges.sold_items_count}</p>
        </div>
        <div className="bg-yellow-50 p-6 rounded-lg shadow-sm text-center">
          <p className="text-sm font-medium text-yellow-700">Aging Stock (3+ Months)</p>
          <p className="text-4xl font-bold text-yellow-900 mt-2">{inventoryChanges.aging_items_count}</p>
        </div>
        <div className="bg-green-50 p-6 rounded-lg shadow-sm text-center">
          <p className="text-sm font-medium text-green-700">Unchanged Items</p>
          <p className="text-4xl font-bold text-green-900 mt-2">{inventoryChanges.unchanged_items_count}</p>
        </div>
      </div>

      <div className="mt-10">
        <h3 className="text-2xl font-bold mb-4 text-gray-800">Recommendations</h3>
        <div className="bg-gray-50 p-6 rounded-lg shadow-sm">
          <p className="text-gray-700">
            Based on current data, consider reviewing **aging stock** for potential discounts to improve sales velocity.
            Items that are **hot sellers** might be candidates for a price markup if demand continues to rise.
          </p>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;
