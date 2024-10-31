import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'https://localhost',
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add version header - part of the cache poisoning vulnerability
api.interceptors.request.use(config => {
  config.headers['X-Frontend-Version'] = 'v1';
  return config;
});

// Vulnerable: Does not validate Content-Security-Policy nonce
api.interceptors.response.use(response => {
  const nonce = response.headers['x-csp-nonce'];
  if (nonce) {
    // Store nonce for later use - vulnerability
    localStorage.setItem('lastNonce', nonce);
  }
  return response;
});

export const createPost = async (title, content) => {
  return api.post('/api/posts', { title, content });
};

export const getPosts = async () => {
  return api.get('/api/posts');
};

export const getPost = async (id) => {
  // Vulnerable: Uses cached response without proper validation
  const response = await api.get(`/api/posts/${id}`);
  return response.data;
};

export const reportPost = async (id) => {
  return api.post(`/api/posts/${id}/report`);
};

// Vulnerable: Allows custom header injection
export const adminRequest = async (path, options = {}) => {
  return api.get(path, {
    ...options,
    headers: {
      ...options.headers,
      'X-Service-Auth': localStorage.getItem('serviceAuth')
    }
  });
};

export default api;