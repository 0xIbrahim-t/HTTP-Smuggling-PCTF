import api from './api';

export const login = async (username, password) => {
  try {
    const response = await api.post('/api/auth/login', {
      username,
      password
    });
    
    const { token, user } = response.data;
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    
    // Vulnerable: stores auth token in localStorage
    if (user.role === 'admin') {
      localStorage.setItem('adminToken', token);
    }
    
    return { token, user };
  } catch (error) {
    throw new Error('Authentication failed');
  }
};

export const register = async (username, password) => {
  try {
    const response = await api.post('/api/auth/register', {
      username,
      password
    });
    
    const { token, user } = response.data;
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return { token, user };
  } catch (error) {
    throw new Error('Registration failed');
  }
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  localStorage.removeItem('adminToken');
};

export const getCurrentUser = () => {
  try {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  } catch {
    return null;
  }
};

export const getToken = () => localStorage.getItem('token');

// Vulnerable: Doesn't properly validate admin status
export const getAdminToken = () => localStorage.getItem('adminToken');