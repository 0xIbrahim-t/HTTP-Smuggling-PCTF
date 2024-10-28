import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import BlogList from './components/BlogList';
import BlogPost from './components/BlogPost';
import AdminDashboard from './components/AdminDashboard';
import BlogCreate from './components/BlogCreate';
import UserLogin from './components/UserLogin';
import AdminLogin from './components/AdminLogin';
import { isAdmin } from './utils/auth';

// Landing Page Component
const LandingPage = () => {
  return (
    <div style={{
      textAlign: 'center',
      padding: '4rem 2rem',
      maxWidth: '800px',
      margin: '0 auto'
    }}>
      <h1 style={{ fontSize: '2.5rem', marginBottom: '2rem' }}>Welcome to the Blog Platform</h1>
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '2rem',
        marginTop: '2rem'
      }}>
        <Link to="/login" style={{
          padding: '1rem 2rem',
          background: '#28a745',
          color: 'white',
          textDecoration: 'none',
          borderRadius: '4px',
          fontWeight: 'bold'
        }}>
          User Login
        </Link>
        <Link to="/admin/login" style={{
          padding: '1rem 2rem',
          background: '#007bff',
          color: 'white',
          textDecoration: 'none',
          borderRadius: '4px',
          fontWeight: 'bold'
        }}>
          Admin Login
        </Link>
      </div>
    </div>
  );
};

// Navigation component (only shows when logged in)
const Navigation = () => {
  const token = localStorage.getItem('token');
  const adminStatus = isAdmin();
  
  if (!token) return null; // Don't show nav if not logged in

  return (
    <nav style={{ 
      padding: '1rem', 
      background: '#f8f9fa',
      borderBottom: '1px solid #dee2e6'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center'
      }}>
        <Link to="/blogs" style={{ marginRight: '1rem', textDecoration: 'none', color: '#333' }}>Blogs</Link>
        {adminStatus && (
          <>
            <Link to="/admin" style={{ marginRight: '1rem', textDecoration: 'none', color: '#333' }}>Admin Dashboard</Link>
            <Link to="/admin/create-blog" style={{ textDecoration: 'none', color: '#333' }}>Create Blog</Link>
          </>
        )}
        <button 
          onClick={() => {
            localStorage.removeItem('token');
            window.location.href = '/';
          }}
          style={{
            marginLeft: 'auto',
            padding: '0.5rem 1rem',
            background: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Logout
        </button>
      </div>
    </nav>
  );
};

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <div style={{ padding: '2rem' }}>
          <Routes>
            {/* Landing Page */}
            <Route path="/" element={
              localStorage.getItem('token') ? <Navigate to="/blogs" /> : <LandingPage />
            } />

            {/* Auth Routes */}
            <Route path="/login" element={<UserLogin />} />
            <Route path="/admin/login" element={<AdminLogin />} />

            {/* Protected Routes */}
            <Route path="/blogs" element={
              <ProtectedRoute>
                <BlogList />
              </ProtectedRoute>
            } />
            <Route path="/post/:id" element={
              <ProtectedRoute>
                <BlogPost />
              </ProtectedRoute>
            } />

            {/* Admin Routes */}
            <Route path="/admin" element={
              <ProtectedRoute adminOnly={true}>
                <AdminDashboard />
              </ProtectedRoute>
            } />
            <Route path="/admin/create-blog" element={
              <ProtectedRoute adminOnly={true}>
                <BlogCreate />
              </ProtectedRoute>
            } />

            {/* Catch all */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

// Protected Route Component
const ProtectedRoute = ({ children, adminOnly = false }) => {
  const token = localStorage.getItem('token');
  if (!token) return <Navigate to="/" />;
  if (adminOnly && !isAdmin()) return <Navigate to="/blogs" />;
  return children;
};

export default App;