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
    <div className="container">
      <h1>Blog Posts</h1>
      {posts.map(post => (
        <div key={post.id} className="post-preview">
          <Link to={`/post/${post.id}`}>
            <h2>{post.title}</h2>
          </Link>
          <p>By {post.author} on {new Date(post.created_at).toLocaleDateString()}</p>
          <div dangerouslySetInnerHTML={{ __html: post.content.substring(0, 200) + '...' }} />
        </div>
      ))}
    </div>
  );
};

export default BlogList;