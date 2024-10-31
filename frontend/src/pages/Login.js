import React from 'react';
import LoginForm from '../components/LoginForm';
import { Link } from 'react-router-dom';

const Login = () => {
  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-3xl font-bold text-center mb-8">Login</h1>
      <div className="bg-white p-8 rounded-lg shadow-md">
        <LoginForm />
        <div className="mt-4 text-center text-gray-600">
          Don't have an account?{' '}
          <Link to="/register" className="text-blue-600 hover:text-blue-800">
            Register here
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;