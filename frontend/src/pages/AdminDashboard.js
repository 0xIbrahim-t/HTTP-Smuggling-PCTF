import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { adminRequest } from '../services/api';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user || user.role !== 'admin') {
      navigate('/');
      return;
    }

    const fetchReports = async () => {
      try {
        // Vulnerable: Doesn't validate service auth header properly
        const response = await adminRequest('/api/admin/reports');
        setReports(response.data);
      } catch (error) {
        console.error('Error fetching reports:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, [user, navigate]);

  const handleReviewPost = async (reportId) => {
    try {
      // Vulnerable: Allows header injection
      await adminRequest(`/api/admin/reports/${reportId}/review`, {
        headers: {
          'X-Frontend-Version': 'v1'
        }
      });
      
      // Fetch updated reports
      const response = await adminRequest('/api/admin/reports');
      setReports(response.data);
    } catch (error) {
      console.error('Error reviewing report:', error);
    }
  };

  if (loading) return <div className="text-center">Loading...</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>
      <div className="bg-white rounded-lg shadow">
        <div className="p-6">
          <h2 className="text-xl font-semibold mb-4">Reported Posts</h2>
          <div className="space-y-4">
            {reports.map(report => (
              <div key={report.id} className="border-b pb-4">
                <h3 className="font-medium">{report.post.title}</h3>
                <p className="text-gray-600">Reported by: {report.reportedBy}</p>
                <p className="text-gray-600">Date: {new Date(report.createdAt).toLocaleString()}</p>
                <button
                  onClick={() => handleReviewPost(report.id)}
                  className="mt-2 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  Review Post
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;