import { useEffect, useMemo, useState } from 'react';
import { bookingsAPI, estimationAPI } from '../services/api';
import './RefundComparator.scss';

const modelOptions = [
  { value: 'auto', label: 'Auto Ensemble' },
  { value: 'random_forest', label: 'Random Forest' },
  { value: 'gradient_boosting', label: 'Gradient Boosting' },
  { value: 'rule_based', label: 'Rule Based' }
];

const calamityOptions = [
  { value: 'auto', label: 'Auto Detect from Active Risks' },
  { value: 'pandemic', label: 'Pandemic' },
  { value: 'war', label: 'War / Conflict' },
  { value: 'natural_disaster', label: 'Natural Disaster' },
  { value: 'flight_cancellation', label: 'Flight Cancellation' },
  { value: 'terrorism', label: 'Terrorism' },
  { value: 'political_instability', label: 'Political Instability' },
  { value: 'economic_crisis', label: 'Economic Crisis' },
  { value: 'civil_unrest', label: 'Civil Unrest' },
  { value: 'none', label: 'No Calamity / Baseline' }
];

const severityOptions = ['low', 'medium', 'high', 'critical'];

const RefundComparator = () => {
  const [bookings, setBookings] = useState([]);
  const [selectedBookingId, setSelectedBookingId] = useState('');
  const [selectedModel, setSelectedModel] = useState('auto');
  const [selectedCalamity, setSelectedCalamity] = useState('auto');
  const [selectedSeverity, setSelectedSeverity] = useState('high');
  const [estimate, setEstimate] = useState(null);
  const [loadingBookings, setLoadingBookings] = useState(true);
  const [estimating, setEstimating] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadBookings();
  }, []);

  const loadBookings = async () => {
    try {
      setLoadingBookings(true);
      const response = await bookingsAPI.getAll(0, 200);
      setBookings(response.data);
      if (response.data.length > 0) {
        setSelectedBookingId(String(response.data[0].id));
      }
    } catch (err) {
      console.error(err);
      setError('Failed to load existing bookings.');
    } finally {
      setLoadingBookings(false);
    }
  };

  const selectedBooking = useMemo(
    () => bookings.find((booking) => String(booking.id) === String(selectedBookingId)),
    [bookings, selectedBookingId]
  );

  const handleEstimate = async (e) => {
    e.preventDefault();
    if (!selectedBookingId) {
      setError('Please select an existing booking.');
      return;
    }

    try {
      setEstimating(true);
      setError(null);

      const response = await estimationAPI.estimateRefund(selectedBookingId, {
        selected_model: selectedModel,
        calamity_type: selectedCalamity,
        severity: selectedSeverity
      });

      setEstimate(response.data);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail
          ? `Failed to estimate refund: ${JSON.stringify(err.response.data.detail)}`
          : 'Failed to estimate refund.'
      );
    } finally {
      setEstimating(false);
    }
  };

  return (
    <div className="refund-comparator">
      <div className="page-header">
        <div>
          <h1>Refund Model Comparator</h1>
          <p>Choose an existing booking, calamity type, and prediction model to compare refund outcomes.</p>
        </div>
      </div>

      {error && (
        <div className="notification error">
          <span className="notification-icon">❌</span>
          <div className="notification-content">
            <strong>Error</strong>
            <p>{error}</p>
          </div>
        </div>
      )}

      <div className="comparator-layout">
        <form className="card comparator-form" onSubmit={handleEstimate}>
          <div className="form-section">
            <h3>1. Select Existing Customer Booking</h3>
            <label htmlFor="booking-select">Booking</label>
            <select
              id="booking-select"
              value={selectedBookingId}
              onChange={(e) => setSelectedBookingId(e.target.value)}
              disabled={loadingBookings || bookings.length === 0}
            >
              {bookings.length === 0 && <option value="">No bookings available</option>}
              {bookings.map((booking) => (
                <option key={booking.id} value={booking.id}>
                  {booking.customer_name} — {booking.booking_reference} — {booking.origin} to {booking.destination}
                </option>
              ))}
            </select>
          </div>

          <div className="form-section">
            <h3>2. Select Prediction Model</h3>
            <div className="option-grid">
              {modelOptions.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  className={`option-card ${selectedModel === option.value ? 'selected' : ''}`}
                  onClick={() => setSelectedModel(option.value)}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>

          <div className="form-section">
            <h3>3. Select Calamity Type</h3>
            <label htmlFor="calamity-select">Calamity</label>
            <select
              id="calamity-select"
              value={selectedCalamity}
              onChange={(e) => setSelectedCalamity(e.target.value)}
            >
              {calamityOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>

            <label htmlFor="severity-select">Severity</label>
            <select
              id="severity-select"
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              disabled={selectedCalamity === 'auto'}
            >
              {severityOptions.map((severity) => (
                <option key={severity} value={severity}>
                  {severity.charAt(0).toUpperCase() + severity.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div className="form-actions">
            <button type="submit" disabled={estimating || !selectedBookingId}>
              {estimating ? 'Calculating...' : 'Calculate Refund'}
            </button>
          </div>
        </form>

        <div className="results-panel">
          <div className="card booking-summary">
            <h3>Selected Booking</h3>
            {!selectedBooking ? (
              <p>No booking selected.</p>
            ) : (
              <div className="summary-grid">
                <div><span>Customer</span><strong>{selectedBooking.customer_name}</strong></div>
                <div><span>Email</span><strong>{selectedBooking.customer_email}</strong></div>
                <div><span>Route</span><strong>{selectedBooking.origin} → {selectedBooking.destination}</strong></div>
                <div><span>Total Cost</span><strong>₹{selectedBooking.total_cost.toLocaleString('en-IN')}</strong></div>
              </div>
            )}
          </div>

          <div className="card estimate-panel">
            <h3>Estimated Refund Result</h3>
            {!estimate ? (
              <p className="placeholder">Run a calculation to compare the selected model against the chosen calamity scenario.</p>
            ) : (
              <div className="estimate-content">
                <div className="hero-metric">
                  <span className="metric-label">Expected Refund</span>
                  <strong>₹{estimate.expected_refund_amount.toLocaleString('en-IN')}</strong>
                  <span className="metric-subtitle">{estimate.expected_refund_percentage.toFixed(1)}% of booking value</span>
                </div>

                <div className="estimate-grid">
                  <div><span>Risk Level</span><strong>{estimate.current_risk_level}</strong></div>
                  <div><span>Risk Score</span><strong>{estimate.risk_score}/100</strong></div>
                  <div><span>Confidence Range</span><strong>₹{estimate.confidence_lower.toLocaleString('en-IN')} - ₹{estimate.confidence_upper.toLocaleString('en-IN')}</strong></div>
                  <div><span>Prediction Confidence</span><strong>{estimate.prediction_confidence}%</strong></div>
                  <div><span>Best Case</span><strong>₹{estimate.best_case_refund.toLocaleString('en-IN')}</strong></div>
                  <div><span>Worst Case</span><strong>₹{estimate.worst_case_refund.toLocaleString('en-IN')}</strong></div>
                  <div><span>Most Likely</span><strong>₹{estimate.most_likely_refund.toLocaleString('en-IN')}</strong></div>
                  <div><span>Model Metadata</span><strong>{estimate.model_version}</strong></div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RefundComparator;

// Made with Bob