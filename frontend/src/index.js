import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Global configuration for CSP nonce
window.__nonce = document.querySelector('meta[http-equiv="Content-Security-Policy"]')
  ?.content.match(/nonce-([^']+)/)?.[1] || '';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);