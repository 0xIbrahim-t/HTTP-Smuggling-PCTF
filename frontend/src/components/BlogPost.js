import React from 'react';
import { useNavigate } from 'react-router-dom';
import DOMPurify from 'dompurify';

const BlogPost = ({ post, showFull = false }) => {
  const navigate = useNavigate();

  // Vulnerable: Uses stored nonce from localStorage
  const nonce = localStorage.getItem('lastNonce') || '';

  // Vulnerable: Allows script injection through nonce reuse
  const createMarkup = (content) => {
    const sanitized = DOMPurify.sanitize(content, {
      ALLOWED_TAGS: ['div', 'span', 'p', 'h1', 'h2', 'h3', 'script'],
      ALLOWED_ATTR: ['class', 'id', 'nonce']
    });
    return { __html: sanitized };
  };

  const handleReportClick = async (e) => {
    e.stopPropagation();
    try {
      await fetch(`/api/posts/${post.id}/report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Vulnerable: Sends frontend version in header
          'X-Frontend-Version': 'v1'
        }
      });
      alert('Post reported successfully!');
    } catch (error) {
      console.error('Error reporting post:', error);
    }
  };

  return (
    <div 
      className="bg-white rounded-lg shadow p-6 mb-4 cursor-pointer"
      onClick={() => !showFull && navigate(`/post/${post.id}`)}
    >
      <h2 className="text-2xl font-bold mb-2">{post.title}</h2>
      <div 
        className="prose"
        dangerouslySetInnerHTML={createMarkup(post.content)} // Vulnerable: XSS possible through nonce reuse
      />
      {showFull && (
        <div className="mt-4">
          <button
            onClick={handleReportClick}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Report Post
          </button>
        </div>
      )}
    </div>
  );
};

export default BlogPost;