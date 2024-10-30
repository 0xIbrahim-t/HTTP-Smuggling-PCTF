import axios from 'axios';
import MD5 from 'crypto-js/md5';

const API_URL = window.location.protocol + '//' + window.location.host;

const api = axios.create({
    baseURL: API_URL,
    withCredentials: false,
    headers: {
        'Content-Type': 'application/json',
    }
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Function to generate service auth
const generateServiceAuth = (token, timestamp) => {
    const secret = 'very_secret_key_456';  // From backend config
    const raw = `${token}${timestamp}${secret}`;
    return MD5(raw).toString();
};

export const auth = {
    login: (username, password) => {
        console.log('Attempting login with:', { username, password });
        return api.post('/api/auth/login', { 
            username: username,
            password: password 
        });
    }
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
        const token = localStorage.getItem('token');
        const serviceAuth = generateServiceAuth(token, timestamp);
        
        console.log('Generating admin headers:', {
            token,
            timestamp,
            serviceAuth
        });

        return api.get('/api/admin/dashboard', {
            headers: {
                'X-Service-Auth': serviceAuth,
                'X-Timestamp': timestamp.toString()
            }
        });
    },
    getReports: () => api.get('/api/admin/reports'),
};

export default api;