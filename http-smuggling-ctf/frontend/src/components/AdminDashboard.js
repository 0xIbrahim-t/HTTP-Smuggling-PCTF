import React, { useState, useEffect } from 'react';
import { admin } from '../utils/api';

const AdminDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [reports, setReports] = useState([]);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const [dashResponse, reportsResponse] = await Promise.all([
          admin.getDashboard(),
          admin.getReports()
        ]);
        setDashboardData(dashResponse.data);
        setReports(reportsResponse.data);
      } catch (error) {
        console.error('Error fetching admin data:', error);
      }
    };

    fetchDashboard();
  }, []);

  if (!dashboardData) return <div>Loading...</div>;

  return (
    <div className="container">
      <h1>Admin Dashboard</h1>
      <div className="sensitive-info">
        <h2>Server Information</h2>
        <pre>{JSON.stringify(dashboardData, null, 2)}</pre>
      </div>
      
      <h2>Reported Posts</h2>
      {reports.map(post => (
        <div key={post.id} className="reported-post">
          <h3>{post.title}</h3>
          <p>Reports: {post.report_count}</p>
          <div dangerouslySetInnerHTML={{ __html: post.content }} />
        </div>
      ))}
    </div>
  );
};

export default AdminDashboard;