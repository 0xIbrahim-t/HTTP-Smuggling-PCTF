import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import CreatePost from '../components/CreatePost';

const CreatePostPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  return (
    <div className="max-w-3xl mx-auto mt-10">
      <h1 className="text-3xl font-bold mb-8">Create New Post</h1>
      <div className="bg-white p-8 rounded-lg shadow-md">
        <CreatePost />
      </div>
    </div>
  );
};

export default CreatePostPage;