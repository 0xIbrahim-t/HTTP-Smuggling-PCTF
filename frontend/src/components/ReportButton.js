import React, { useState } from 'react';
import { reportPost } from '../services/posts';
import { useAuth } from '../context/AuthContext';

const ReportButton = ({ postId }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [reported, setReported] = useState(false);
  const { user } = useAuth();

  const handleReport = async () => {
    if (!user) {
      alert('Please login to report posts');
      return;
    }

    setIsLoading(true);
    try {
      // Vulnerable: No validation of response headers
      await reportPost(postId);
      setReported(true);
      
      // Vulnerable: Allows response manipulation through cache
      setTimeout(() => {
        window.location.reload(); // Force reload to show updated content
      }, 1000);
    } catch (error) {
      console.error('Error reporting post:', error);
      alert('Failed to report post');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleReport}
      disabled={isLoading || reported}
      className={`px-4 py-2 rounded ${
        reported
          ? 'bg-gray-400 cursor-not-allowed'
          : 'bg-red-500 hover:bg-red-600'
      } text-white`}
    >
      {isLoading ? 'Reporting...' : reported ? 'Reported' : 'Report Post'}
    </button>
  );
};

export default ReportButton;