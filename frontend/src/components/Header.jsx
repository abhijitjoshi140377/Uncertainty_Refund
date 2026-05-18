import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Header.scss';

const Header = ({ riskNotifications = [], onClearRiskNotifications }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  
  // Mock user data - in a real app, this would come from authentication context
  const [user, setUser] = useState({
    name: 'Abhijit Joshi',
    email: 'abhijit.joshi2@ibm.com',
    role: 'Admin',
    isLoggedIn: true
  });

  const isActive = (path) => location.pathname === path;

  const handleLogout = () => {
    // In a real app, this would clear authentication tokens and redirect to login
    setUser({ ...user, isLoggedIn: false });
    setShowUserMenu(false);
    alert('Logged out successfully!');
  };

  const handleLogin = () => {
    // In a real app, this would redirect to login page
    setUser({
      name: 'Abhijit Joshi',
      email: 'abhijit.joshi2@ibm.com',
      role: 'Admin',
      isLoggedIn: true
    });
    setShowUserMenu(false);
    alert('Logged in successfully!');
  };

  return (
    <header className="app-header">
      <div className="header-container">
        <div className="header-brand" onClick={() => navigate('/')}>
          <div className="brand-icon">✈️</div>
          <div className="brand-text">
            <h1>Refund Intelligence Platform</h1>
            <p>Smarter refund insights and risk visibility</p>
          </div>
        </div>
        
        <nav className="header-nav">
          <button
            className={`nav-item ${isActive('/') ? 'active' : ''}`}
            onClick={() => navigate('/')}
          >
            <span className="nav-icon">📊</span>
            Dashboard
          </button>
          <button
            className={`nav-item ${isActive('/bookings') ? 'active' : ''}`}
            onClick={() => navigate('/bookings')}
          >
            <span className="nav-icon">📋</span>
            Bookings
          </button>
          <button
            className={`nav-item ${isActive('/refund-comparator') ? 'active' : ''}`}
            onClick={() => navigate('/refund-comparator')}
          >
            <span className="nav-icon">🧮</span>
            Comparator
          </button>
          <button
            className={`nav-item ${isActive('/risk-monitor') ? 'active' : ''}`}
            onClick={() => navigate('/risk-monitor')}
          >
            <span className="nav-icon">⚠️</span>
            Risk Monitor
          </button>
          <button
            className={`nav-item ${isActive('/analytics') ? 'active' : ''}`}
            onClick={() => navigate('/analytics')}
          >
            <span className="nav-icon">📈</span>
            Analytics
          </button>
        </nav>

        <div className="header-actions">
          <div className="notifications-wrap">
            <button
              className="action-btn"
              title="Notifications"
              onClick={() => {
                setShowNotifications(!showNotifications);
                setShowUserMenu(false);
              }}
            >
              🔔
              {riskNotifications.length > 0 && (
                <span className="notification-badge">
                  {riskNotifications.length > 9 ? '9+' : riskNotifications.length}
                </span>
              )}
            </button>

            {showNotifications && (
              <div className="notifications-menu">
                <div className="notifications-header">
                  <h4>Event Notifications</h4>
                  {riskNotifications.length > 0 && (
                    <button
                      type="button"
                      className="clear-notifications-btn"
                      onClick={() => onClearRiskNotifications?.()}
                    >
                      Clear
                    </button>
                  )}
                </div>

                {riskNotifications.length === 0 ? (
                  <p className="notifications-empty">No new event notifications.</p>
                ) : (
                  <div className="notifications-list">
                    {riskNotifications.map((notification) => (
                      <div key={notification.id} className="notification-item">
                        <div className="notification-item-icon">⚠️</div>
                        <div className="notification-item-content">
                          <strong>{notification.title}</strong>
                          <span>{notification.message}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
          
          <div className="user-profile">
            <button
              className="action-btn user-btn"
              onClick={() => {
                setShowUserMenu(!showUserMenu);
                setShowNotifications(false);
              }}
              title="User Profile"
            >
              👤
            </button>
            
            {showUserMenu && (
              <div className="user-menu">
                {user.isLoggedIn ? (
                  <>
                    <div className="user-info">
                      <div className="user-avatar">👤</div>
                      <div className="user-details">
                        <div className="user-name">{user.name}</div>
                        <div className="user-email">{user.email}</div>
                        <div className="user-role">{user.role}</div>
                      </div>
                    </div>
                    
                    <div className="menu-divider"></div>
                    
                    <button className="menu-item" onClick={() => setShowUserMenu(false)}>
                      <span className="menu-icon">⚙️</span>
                      Settings
                    </button>
                    <button className="menu-item" onClick={() => setShowUserMenu(false)}>
                      <span className="menu-icon">👤</span>
                      Profile
                    </button>
                    <button className="menu-item" onClick={() => setShowUserMenu(false)}>
                      <span className="menu-icon">🔔</span>
                      Notifications
                    </button>
                    
                    <div className="menu-divider"></div>
                    
                    <button className="menu-item logout" onClick={handleLogout}>
                      <span className="menu-icon">🚪</span>
                      Logout
                    </button>
                  </>
                ) : (
                  <>
                    <div className="user-info">
                      <div className="user-avatar">👤</div>
                      <div className="user-details">
                        <div className="user-name">Guest User</div>
                        <div className="user-email">Not logged in</div>
                      </div>
                    </div>
                    
                    <div className="menu-divider"></div>
                    
                    <button className="menu-item login" onClick={handleLogin}>
                      <span className="menu-icon">🔑</span>
                      Login
                    </button>
                    <button className="menu-item" onClick={() => setShowUserMenu(false)}>
                      <span className="menu-icon">📝</span>
                      Sign Up
                    </button>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Overlay to close menu when clicking outside */}
      {(showUserMenu || showNotifications) && (
        <div
          className="menu-overlay"
          onClick={() => {
            setShowUserMenu(false);
            setShowNotifications(false);
          }}
        ></div>
      )}
    </header>
  );
};

export default Header;

// Made with Bob
