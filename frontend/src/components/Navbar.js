import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-gray-800 text-white">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold">
              CTF Blog
            </Link>
            {user && user.role === 'admin' && (
              <Link to="/create-post" className="ml-8 hover:text-gray-300">
                Create Post
              </Link>
            )}
          </div>
          <div className="flex items-center">
            {user ? (
              <>
                <span className="mr-4">Welcome, {user.username}</span>
                {user.role === 'admin' && (
                  <Link to="/admin" className="mr-4 text-yellow-400 hover:text-yellow-300">
                    Admin Panel
                  </Link>
                )}
                <button
                  onClick={logout}
                  className="bg-red-600 px-4 py-2 rounded hover:bg-red-700"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="mr-4 hover:text-gray-300">
                  Login
                </Link>
                <Link to="/register" className="bg-blue-600 px-4 py-2 rounded hover:bg-blue-700">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;