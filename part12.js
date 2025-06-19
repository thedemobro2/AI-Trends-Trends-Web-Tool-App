// frontend/src/components/Header.jsx
import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="bg-gray-800 text-white p-4 shadow-md">
      <nav className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-blue-300 hover:text-blue-100 transition-colors duration-200">
          AI Parts App
        </Link>
        <div>
          <Link to="/" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-md font-medium">
            Upload CSV
          </Link>
          <Link to="/dashboard" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-md font-medium">
            Dashboard
          </Link>
        </div>
      </nav>
    </header>
  );
}

export default Header;
