import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import BlogPost from '../components/BlogPost';
import { getPost } from '../services/api';

const ViewPost = () => {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        // Vulnerable: Uses cached response without proper validation
        const postData = await getPost(id);
        setPost(postData);
      } catch (error) {
        setError('Failed to load post');
        console.error('Error fetching post:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [id]);

  if (loading) return <div className="text-center">Loading...</div>;
  if (error) return <div className="text-red-600 text-center">{error}</div>;
  if (!post) return <div className="text-center">Post not found</div>;

  return (
    <div className="max-w-3xl mx-auto">
      <BlogPost post={post} showFull={true} />
    </div>
  );
};

export default ViewPost;    