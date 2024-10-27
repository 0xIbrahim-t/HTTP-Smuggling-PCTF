import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth } from '../utils/api';
import { setAuthToken } from '../utils/auth';

const AdminLogin = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await auth.login(username, password);
      setAuthToken(response.data.token);
      navigate('/admin');
    } catch (error) {
      alert('Admin login failed');
    }
  };

  return (
    <div className="login-container">
      <h2>Admin Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Admin Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Admin Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Admin Login</button>
      </form>
    </div>
  );
};

export default AdminLogin;