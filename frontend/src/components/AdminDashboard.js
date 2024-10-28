import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { admin, blog } from '../utils/api';

const AdminDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [posts, setPosts] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [dashResponse, postsResponse] = await Promise.all([
        admin.getDashboard(),
        blog.getPosts()
      ]);
      setDashboardData(dashResponse.data);
      setPosts(postsResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Admin Dashboard</h1>
        <button
          onClick={() => navigate('/admin/create-blog')}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Create New Blog
        </button>
      </div>

      <div style={{ marginBottom: '2rem' }}>
        <h2>Server Information</h2>
        <pre style={{ 
          background: '#f5f5f5', 
          padding: '1rem', 
          borderRadius: '4px' 
        }}>
          {JSON.stringify(dashboardData, null, 2)}
        </pre>
      </div>

      <div>
        <h2>Blog Posts</h2>
        <div style={{ display: 'grid', gap: '1rem' }}>
          {posts.map(post => (
            <div 
              key={post.id} 
              style={{
                border: '1px solid #ddd',
                borderRadius: '4px',
                padding: '1rem'
              }}
            >
              <h3>{post.title}</h3>
              <p>Created on: {new Date(post.created_at).toLocaleDateString()}</p>
              <p>By: {post.author}</p>
              {post.is_reported && (
                <span style={{ 
                  color: 'red', 
                  fontWeight: 'bold' 
                }}>
                  Reported {post.report_count} times
                </span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;