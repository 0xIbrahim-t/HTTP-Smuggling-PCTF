import React from 'react';
import { blog } from '../utils/api';

const ReportButton = ({ postId }) => {
  const handleReport = async () => {
    try {
      await blog.reportPost(postId);
      alert('Post reported successfully');
    } catch (error) {
      console.error('Error reporting post:', error);
      alert('Error reporting post');
    }
  };

  return (
    <button 
      onClick={handleReport}
      className="report-button"
    >
      Report Post
    </button>
  );
};

export default ReportButton;