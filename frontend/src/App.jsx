import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import BookingList from './pages/BookingList';
import CreateBooking from './pages/CreateBooking';
import BookingDetails from './pages/BookingDetails';
import RiskMonitor from './pages/RiskMonitor';
import Analytics from './pages/Analytics';
import RefundComparator from './pages/RefundComparator';
import './App.scss';

function App() {
  const [notifications, setNotifications] = useState([]);

  const pushNotification = (notification) => {
    setNotifications((prev) => [
      {
        id: Date.now(),
        createdAt: new Date().toISOString(),
        ...notification
      },
      ...prev
    ].slice(0, 9));
  };

  const handleRiskEventCreated = (event) => {
    pushNotification({
      type: 'event',
      title: `${event.event_type.replace(/_/g, ' ')} alert`,
      message: `${event.affected_region} marked as ${event.severity} severity`
    });
  };

  const handleBookingCreated = (booking) => {
    pushNotification({
      type: 'booking',
      title: 'New booking created',
      message: `${booking.customer_name} • ${booking.origin} to ${booking.destination}`
    });
  };

  const clearNotifications = () => {
    setNotifications([]);
  };

  return (
    <Router>
      <div className="app">
        <Header
          riskNotifications={notifications}
          onClearRiskNotifications={clearNotifications}
        />
        <main className="app-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/bookings" element={<BookingList />} />
            <Route
              path="/bookings/new"
              element={<CreateBooking onBookingCreated={handleBookingCreated} />}
            />
            <Route path="/bookings/:id" element={<BookingDetails />} />
            <Route path="/refund-comparator" element={<RefundComparator />} />
            <Route
              path="/risk-monitor"
              element={<RiskMonitor onRiskEventCreated={handleRiskEventCreated} />}
            />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

// Made with Bob
