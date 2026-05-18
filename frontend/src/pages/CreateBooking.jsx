import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { bookingsAPI } from '../services/api';
import './CreateBooking.scss';

const CreateBooking = ({ onBookingCreated }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [selectedCalamity, setSelectedCalamity] = useState('');

  const calamityTypes = [
    { value: 'pandemic', label: '🦠 Pandemic', description: 'COVID-19, health emergencies' },
    { value: 'war', label: '⚔️ War/Conflict', description: 'Military conflicts, civil unrest' },
    { value: 'natural_disaster', label: '🌪️ Natural Disaster', description: 'Earthquakes, hurricanes, floods' },
    { value: 'flight_cancellation', label: '✈️ Flight Cancellation', description: 'Airline operational issues' },
    { value: 'terrorism', label: '💣 Terrorism', description: 'Security threats, attacks' },
    { value: 'political_instability', label: '🏛️ Political Instability', description: 'Government changes, protests' },
    { value: 'economic_crisis', label: '💰 Economic Crisis', description: 'Currency collapse, sanctions' },
    { value: 'none', label: '✅ No Risk Event', description: 'Normal travel conditions' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(e.target);
    const bookingData = {
      customer_name: formData.get('customer_name'),
      customer_email: formData.get('customer_email'),
      travel_date: new Date(formData.get('travel_date')).toISOString(),
      destination: formData.get('destination'),
      origin: formData.get('origin'),
      components: [
        {
          component_type: 'flight',
          provider_name: formData.get('airline') || 'Air India',
          cost: parseFloat(formData.get('flight_cost')) || 50000,
          is_refundable: true,
          cancellation_fee: 500
        },
        {
          component_type: 'hotel',
          provider_name: formData.get('hotel') || 'Marriott',
          cost: parseFloat(formData.get('hotel_cost')) || 25000,
          is_refundable: true,
          cancellation_fee: 0
        }
      ]
    };

    try {
      const response = await bookingsAPI.create(bookingData);
      onBookingCreated?.(response.data);
      setSuccess(true);
      setTimeout(() => {
        navigate(`/bookings/${response.data.id}`);
      }, 1500);
    } catch (err) {
      setError('Failed to create booking. Please try again.');
      console.error('Booking creation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-booking">
      <div className="page-header">
        <h1>✈️ Create New Booking</h1>
        <p className="subtitle">Enter travel booking details to get refund estimates</p>
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

      {success && (
        <div className="notification success">
          <span className="notification-icon">✅</span>
          <div className="notification-content">
            <strong>Success</strong>
            <p>Booking created successfully! Redirecting...</p>
          </div>
        </div>
      )}

      <form className="booking-form card" onSubmit={handleSubmit}>
        <div className="form-section">
          <h2>👤 Customer Information</h2>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="customer_name">Customer Name *</label>
              <input
                type="text"
                id="customer_name"
                name="customer_name"
                placeholder="Enter customer name"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="customer_email">Customer Email *</label>
              <input
                type="email"
                id="customer_email"
                name="customer_email"
                placeholder="customer@example.com"
                required
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>⚠️ Risk Event Simulation</h2>
          <p className="section-description">Select a calamity type to simulate refund scenarios</p>
          <div className="calamity-selector">
            {calamityTypes.map((calamity) => (
              <div
                key={calamity.value}
                className={`calamity-card ${selectedCalamity === calamity.value ? 'selected' : ''}`}
                onClick={() => setSelectedCalamity(calamity.value)}
              >
                <div className="calamity-header">
                  <span className="calamity-label">{calamity.label}</span>
                  {selectedCalamity === calamity.value && <span className="check-icon">✓</span>}
                </div>
                <p className="calamity-description">{calamity.description}</p>
              </div>
            ))}
          </div>
          <input type="hidden" name="risk_event" value={selectedCalamity} />
        </div>

        <div className="form-section">
          <h2>🌍 Travel Details</h2>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="origin">Origin *</label>
              <input
                type="text"
                id="origin"
                name="origin"
                placeholder="Mumbai"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="destination">Destination *</label>
              <input
                type="text"
                id="destination"
                name="destination"
                placeholder="Paris"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="travel_date">Travel Date *</label>
              <input
                type="date"
                id="travel_date"
                name="travel_date"
                required
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>✈️ Flight Information</h2>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="airline">Airline</label>
              <input
                type="text"
                id="airline"
                name="airline"
                placeholder="Air India"
                defaultValue="Air India"
              />
            </div>
            <div className="form-group">
              <label htmlFor="flight_cost">Flight Cost (₹) *</label>
              <input
                type="number"
                id="flight_cost"
                name="flight_cost"
                placeholder="50000"
                min="0"
                step="100"
                required
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>🏨 Hotel Information</h2>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="hotel">Hotel</label>
              <input
                type="text"
                id="hotel"
                name="hotel"
                placeholder="Marriott"
                defaultValue="Marriott"
              />
            </div>
            <div className="form-group">
              <label htmlFor="hotel_cost">Hotel Cost (₹) *</label>
              <input
                type="number"
                id="hotel_cost"
                name="hotel_cost"
                placeholder="25000"
                min="0"
                step="100"
                required
              />
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button
            type="button"
            className="secondary"
            onClick={() => navigate('/bookings')}
            disabled={loading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="primary"
            disabled={loading}
          >
            {loading ? '⏳ Creating...' : '✨ Create Booking'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateBooking;

// Made with Bob
