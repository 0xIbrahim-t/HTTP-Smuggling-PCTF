import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import BlogList from './components/BlogList';
import BlogPost from './components/BlogPost';
import AdminDashboard from './components/AdminDashboard';
import UserLogin from './components/UserLogin';
import AdminLogin from './components/AdminLogin';
import { isAdmin } from './utils/auth';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
};

const AdminRoute = ({ children }) => {
  return isAdmin() ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<UserLogin />} />
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route 
            path="/" 
            element={
              <PrivateRoute>
                <BlogList />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/post/:id" 
            element={
              <PrivateRoute>
                <BlogPost />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/admin" 
            element={
              <AdminRoute>
                <AdminDashboard />
              </AdminRoute>
            } 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;