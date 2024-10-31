import api from './api';

export const getAllPosts = async () => {
  // Vulnerable: Doesn't validate response cache headers
  const response = await api.get('/api/posts', {
    headers: {
      'X-Frontend-Version': 'v1'
    }
  });
  return response.data;
};

export const getPost = async (id) => {
  // Vulnerable: Cache poisoning possible
  const response = await api.get(`/api/posts/${id}`, {
    headers: {
      'X-Frontend-Version': 'v1'
    }
  });
  return response.data;
};

export const createPost = async (title, content) => {
  // Vulnerable: No content sanitization
  const response = await api.post('/api/posts', {
    title,
    content
  });
  return response.data;
};

export const reportPost = async (id) => {
  // Vulnerable: Sends predictable headers that affect caching
  const response = await api.post(`/api/posts/${id}/report`, null, {
    headers: {
      'X-Frontend-Version': 'v1'
    }
  });
  return response.data;
};

// Vulnerable: No validation of post content before submission
export const editPost = async (id, title, content) => {
  const response = await api.put(`/api/posts/${id}`, {
    title,
    content
  });
  return response.data;
};

export const deletePost = async (id) => {
  await api.delete(`/api/posts/${id}`);
};