import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { bookingsAPI, riskAPI, historicalAPI } from '../services/api';
import './Dashboard.scss';

const Dashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    totalBookings: 0,
    activeRisks: 0,
    avgRefundRate: 0,
    recentBookings: []
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [bookingsRes, risksRes, statsRes] = await Promise.all([
        bookingsAPI.getAll(0, 10),
        riskAPI.getAll(true),
        historicalAPI.getStatistics()
      ]);

      const avgRefund = statsRes.data.length > 0
        ? statsRes.data.reduce((sum, stat) => sum + stat.average_refund_percentage, 0) / statsRes.data.length
        : 0;

      setStats({
        totalBookings: bookingsRes.data.length,
        activeRisks: risksRes.data.length,
        avgRefundRate: avgRefund.toFixed(1),
        recentBookings: bookingsRes.data.slice(0, 5)
      });
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Travel Refund Uncertainty Estimation</h1>
        <p>AI-powered refund prediction for force majeure events</p>
      </div>

      {error && (
        <div className="notification error">
          <span className="notification-icon">❌</span>
          <div className="notification-content">
            <strong>Error</strong>
            <p>{error}</p>
          </div>
          <button className="notification-close" onClick={() => setError(null)}>×</button>
        </div>
      )}

      {/* Statistics Cards */}
      <div className="stats-grid">
        <div className="stat-card stat-card--success">
          <div className="stat-icon">✅</div>
          <div className="stat-value">{stats.totalBookings}</div>
          <div className="stat-label">Total Bookings</div>
        </div>

        <div className="stat-card stat-card--warning">
          <div className="stat-icon">⚠️</div>
          <div className="stat-value">{stats.activeRisks}</div>
          <div className="stat-label">Active Risk Events</div>
        </div>

        <div className="stat-card stat-card--info">
          <div className="stat-icon">📊</div>
          <div className="stat-value">{stats.avgRefundRate}%</div>
          <div className="stat-label">Avg Refund Rate</div>
        </div>

        <div className="stat-card stat-card--action">
          <button
            className="create-booking-btn"
            onClick={() => navigate('/bookings/new')}
          >
            <span className="btn-icon">➕</span>
            Create New Booking
          </button>
        </div>
      </div>

      {/* Recent Bookings */}
      <div className="card recent-bookings">
        <h3>Recent Bookings</h3>
        {stats.recentBookings.length === 0 ? (
          <p className="no-data">No bookings yet. Create your first booking to get started.</p>
        ) : (
          <div className="bookings-list">
            {stats.recentBookings.map((booking) => (
              <div
                key={booking.id}
                className="booking-item"
                onClick={() => navigate(`/bookings/${booking.id}`)}
              >
                <div className="booking-info">
                  <div className="booking-ref">📋 {booking.booking_reference}</div>
                  <div className="booking-route">
                    {booking.origin} → {booking.destination}
                  </div>
                  <div className="booking-customer">👤 {booking.customer_name}</div>
                </div>
                <div className="booking-cost">
                  ₹{booking.total_cost.toLocaleString('en-IN')}
                </div>
              </div>
            ))}
          </div>
        )}
        <button
          className="view-all-btn"
          onClick={() => navigate('/bookings')}
        >
          View All Bookings →
        </button>
      </div>

      <div className="dashboard-bottom">
        {/* Quick Actions */}
        <div className="card quick-actions">
          <h3>Quick Actions</h3>
          <div className="actions-grid">
            <button
              className="action-btn"
              onClick={() => navigate('/bookings/new')}
            >
              <span className="action-icon">➕</span>
              New Booking
            </button>
            <button
              className="action-btn"
              onClick={() => navigate('/risk-monitor')}
            >
              <span className="action-icon">⚠️</span>
              Risk Monitor
            </button>
            <button
              className="action-btn"
              onClick={() => navigate('/analytics')}
            >
              <span className="action-icon">📈</span>
              View Analytics
            </button>
          </div>
        </div>

        {/* System Info */}
        <div className="card system-info">
          <h3>System Information</h3>
          <div className="info-item">
            <span className="info-label">Version:</span>
            <span className="info-value">1.0.0</span>
          </div>
          <div className="info-item">
            <span className="info-label">ML Model:</span>
            <span className="info-value">✅ Active</span>
          </div>
          <div className="info-item">
            <span className="info-label">Last Updated:</span>
            <span className="info-value">{new Date().toLocaleDateString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

// Made with Bob
