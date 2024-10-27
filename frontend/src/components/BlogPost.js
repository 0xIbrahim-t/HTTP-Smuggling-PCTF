import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { blog } from '../utils/api';
import ReportButton from './ReportButton';

const BlogPost = () => {
  const { id } = useParams();
  const [post, setPost] = useState(null);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await blog.getPost(id);
        setPost(response.data);
      } catch (error) {
        console.error('Error fetching post:', error);
      }
    };

    fetchPost();
  }, [id]);

  if (!post) return <div>Loading...</div>;

  return (
    <div className="container">
      <h1>{post.title}</h1>
      <p>By {post.author} on {new Date(post.created_at).toLocaleDateString()}</p>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
      <ReportButton postId={post.id} />
    </div>
  );
};

export default BlogPost;