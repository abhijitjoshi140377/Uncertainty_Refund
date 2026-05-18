import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Grid,
  Column,
  Tile,
  Button,
  Loading,
  InlineNotification,
  ProgressBar
} from '@carbon/react';
import { ArrowLeft, Calculator } from '@carbon/icons-react';
import { bookingsAPI, estimationAPI } from '../services/api';
import { format } from 'date-fns';
import './BookingDetails.scss';

const BookingDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [booking, setBooking] = useState(null);
  const [estimate, setEstimate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [estimating, setEstimating] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadBookingDetails();
  }, [id]);

  const loadBookingDetails = async () => {
    try {
      setLoading(true);
      const response = await bookingsAPI.getById(id);
      setBooking(response.data);
      
      // Try to load existing estimate
      try {
        const estimatesRes = await estimationAPI.getEstimates(id);
        if (estimatesRes.data.length > 0) {
          setEstimate(estimatesRes.data[0]);
        }
      } catch (err) {
        console.log('No existing estimates');
      }
      
      setError(null);
    } catch (err) {
      setError('Failed to load booking details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const generateEstimate = async () => {
    try {
      setEstimating(true);
      const response = await estimationAPI.estimateRefund(id);
      setEstimate(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to generate refund estimate');
      console.error(err);
    } finally {
      setEstimating(false);
    }
  };

  if (loading) {
    return <Loading description="Loading booking details..." withOverlay={false} />;
  }

  if (!booking) {
    return (
      <div className="booking-details">
        <InlineNotification
          kind="error"
          title="Booking Not Found"
          subtitle="The requested booking could not be found."
        />
        <Button onClick={() => navigate('/bookings')}>Back to Bookings</Button>
      </div>
    );
  }

  return (
    <div className="booking-details">
      <Button
        kind="ghost"
        renderIcon={ArrowLeft}
        onClick={() => navigate('/bookings')}
        className="back-button"
      >
        Back to Bookings
      </Button>

      <h1>Booking Details</h1>

      {error && (
        <InlineNotification
          kind="error"
          title="Error"
          subtitle={error}
          onCloseButtonClick={() => setError(null)}
        />
      )}

      <Grid>
        <Column lg={8} md={4} sm={4}>
          <Tile className="info-tile">
            <h3>Booking Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <span className="label">Reference:</span>
                <span className="value">{booking.booking_reference}</span>
              </div>
              <div className="info-item">
                <span className="label">Customer:</span>
                <span className="value">{booking.customer_name}</span>
              </div>
              <div className="info-item">
                <span className="label">Email:</span>
                <span className="value">{booking.customer_email}</span>
              </div>
              <div className="info-item">
                <span className="label">Origin:</span>
                <span className="value">{booking.origin}</span>
              </div>
              <div className="info-item">
                <span className="label">Destination:</span>
                <span className="value">{booking.destination}</span>
              </div>
              <div className="info-item">
                <span className="label">Travel Date:</span>
                <span className="value">
                  {format(new Date(booking.travel_date), 'MMMM dd, yyyy')}
                </span>
              </div>
              <div className="info-item">
                <span className="label">Total Cost:</span>
                <span className="value cost">
                  ₹{booking.total_cost.toLocaleString('en-IN')}
                </span>
              </div>
              <div className="info-item">
                <span className="label">Status:</span>
                <span className={`value status-${booking.status}`}>
                  {booking.status}
                </span>
              </div>
            </div>
          </Tile>

          <Tile className="components-tile">
            <h3>Booking Components</h3>
            {booking.components.map((component, index) => (
              <div key={index} className="component-item">
                <div className="component-header">
                  <span className="component-type">{component.component_type}</span>
                  <span className="component-cost">
                    ₹{component.cost.toLocaleString('en-IN')}
                  </span>
                </div>
                <div className="component-details">
                  <div>Provider: {component.provider_name}</div>
                  <div>
                    {component.is_refundable ? 'Refundable' : 'Non-refundable'}
                    {component.cancellation_fee > 0 && 
                      ` (Fee: ₹${component.cancellation_fee})`
                    }
                  </div>
                </div>
              </div>
            ))}
          </Tile>
        </Column>

        <Column lg={8} md={4} sm={4}>
          <Tile className="estimate-tile">
            <h3>Refund Estimate</h3>
            
            {!estimate ? (
              <div className="no-estimate">
                <p>No refund estimate generated yet.</p>
                <Button
                  kind="primary"
                  renderIcon={Calculator}
                  onClick={generateEstimate}
                  disabled={estimating}
                >
                  {estimating ? 'Generating...' : 'Generate Estimate'}
                </Button>
              </div>
            ) : (
              <div className="estimate-content">
                <div className="estimate-main">
                  <div className="estimate-amount">
                    <span className="label">Expected Refund</span>
                    <span className="amount">
                      ₹{estimate.expected_refund_amount.toLocaleString('en-IN')}
                    </span>
                    <span className="percentage">
                      {estimate.expected_refund_percentage.toFixed(1)}% of total
                    </span>
                  </div>

                  <div className="confidence-interval">
                    <span className="label">95% Confidence Interval</span>
                    <div className="range">
                      ₹{estimate.confidence_lower.toLocaleString('en-IN')} - 
                      ₹{estimate.confidence_upper.toLocaleString('en-IN')}
                    </div>
                    <ProgressBar
                      value={estimate.expected_refund_percentage}
                      max={100}
                      label="Refund Percentage"
                    />
                  </div>
                </div>

                <div className="risk-info">
                  <div className="risk-level">
                    <span className="label">Current Risk Level:</span>
                    <span className={`value risk-${estimate.current_risk_level}`}>
                      {estimate.current_risk_level}
                    </span>
                  </div>
                  <div className="risk-score">
                    <span className="label">Risk Score:</span>
                    <span className="value">{estimate.risk_score}/100</span>
                  </div>
                </div>

                <div className="scenarios">
                  <h4>Scenario Analysis</h4>
                  <div className="scenario-grid">
                    <div className="scenario">
                      <span className="scenario-label">Best Case</span>
                      <span className="scenario-value">
                        ₹{estimate.best_case_refund.toLocaleString('en-IN')}
                      </span>
                    </div>
                    <div className="scenario">
                      <span className="scenario-label">Most Likely</span>
                      <span className="scenario-value">
                        ₹{estimate.most_likely_refund.toLocaleString('en-IN')}
                      </span>
                    </div>
                    <div className="scenario">
                      <span className="scenario-label">Worst Case</span>
                      <span className="scenario-value">
                        ₹{estimate.worst_case_refund.toLocaleString('en-IN')}
                      </span>
                    </div>
                  </div>
                </div>

                <Button
                  kind="secondary"
                  onClick={generateEstimate}
                  disabled={estimating}
                  className="refresh-btn"
                >
                  Refresh Estimate
                </Button>
              </div>
            )}
          </Tile>
        </Column>
      </Grid>
    </div>
  );
};

export default BookingDetails;

// Made with Bob
