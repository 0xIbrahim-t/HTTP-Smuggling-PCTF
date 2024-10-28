import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { blog } from '../utils/api';

const BlogList = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await blog.getPosts();
        setPosts(response.data);
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    };

    fetchPosts();
  }, []);

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>Blog Posts</h1>
      <div style={{ display: 'grid', gap: '2rem' }}>
        {posts.map(post => (
          <div 
            key={post.id}
            style={{
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '1.5rem',
              background: 'white',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}
          >
            <Link 
              to={`/post/${post.id}`}
              style={{
                textDecoration: 'none',
                color: 'inherit'
              }}
            >
              <h2 style={{ marginBottom: '1rem' }}>{post.title}</h2>
            </Link>
            <div style={{ color: '#666', fontSize: '0.9rem' }}>
              <span>By {post.author}</span>
              <span style={{ margin: '0 0.5rem' }}>•</span>
              <span>{new Date(post.created_at).toLocaleDateString()}</span>
            </div>
            <div 
              style={{ 
                marginTop: '1rem',
                maxHeight: '100px',
                overflow: 'hidden',
                textOverflow: 'ellipsis'
              }}
            >
              {post.content}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BlogList;