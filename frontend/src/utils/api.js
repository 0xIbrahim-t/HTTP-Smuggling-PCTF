import axios from 'axios';

const API_URL = 'http://localhost';

const api = axios.create({
  baseURL: API_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  login: (username, password) => 
    api.post('/api/auth/login', { username, password }),
  register: (username, password) => 
    api.post('/api/auth/register', { username, password }),
};

export const blog = {
  getPosts: () => api.get('/api/blog/posts'),
  getPost: (id) => api.get(`/api/blog/post/${id}`),
  createPost: (title, content) => 
    api.post('/api/blog/post', { title, content }),
  reportPost: (postId) => 
    api.post('/api/blog/report', { postId }),
};

export const admin = {
  getDashboard: () => {
    const timestamp = Math.floor(Date.now() / 1000);
    // Vulnerable X-Service-Auth generation
    const token = localStorage.getItem('token');
    const serviceAuth = generateServiceAuth(token, timestamp);
    
    return api.get('/api/admin/dashboard', {
      headers: {
        'X-Service-Auth': serviceAuth,
        'X-Timestamp': timestamp
      }
    });
  },
  getReports: () => api.get('/api/admin/reports'),
};

export default api;