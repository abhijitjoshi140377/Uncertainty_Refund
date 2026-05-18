import { useState, useEffect } from 'react';
import { riskAPI } from '../services/api';
import { format } from 'date-fns';
import './RiskMonitor.scss';

const RiskMonitor = ({ onRiskEventCreated }) => {
  const [risks, setRisks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, active, historical
  const [showAddModal, setShowAddModal] = useState(false);
  const [formData, setFormData] = useState({
    event_type: 'pandemic',
    affected_region: '',
    severity: 'medium',
    description: '',
    start_date: new Date().toISOString().split('T')[0],
    end_date: '',
    is_active: true
  });

  useEffect(() => {
    loadRisks();
  }, []);

  const loadRisks = async () => {
    try {
      const response = await riskAPI.getAll(true);
      setRisks(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddRisk = async (e) => {
    e.preventDefault();

    const normalizedPayload = {
      ...formData,
      affected_region: formData.affected_region.trim(),
      description: formData.description.trim(),
      start_date: formData.start_date ? new Date(formData.start_date).toISOString() : null,
      end_date: formData.end_date ? new Date(formData.end_date).toISOString() : null
    };

    try {
      const response = await riskAPI.create(normalizedPayload);
      onRiskEventCreated?.(response.data);
      setShowAddModal(false);
      setFormData({
        event_type: 'pandemic',
        affected_region: '',
        severity: 'medium',
        description: '',
        start_date: new Date().toISOString().split('T')[0],
        end_date: '',
        is_active: true
      });
      loadRisks(); // Reload the list
      alert('Risk event added successfully!');
    } catch (err) {
      console.error(err);
      const errorMessage =
        err.response?.data?.detail
          ? `Failed to add risk event: ${JSON.stringify(err.response.data.detail)}`
          : 'Failed to add risk event. Please try again.';
      alert(errorMessage);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const getSeverityColor = (severity) => {
    const colors = {
      low: '#24a148',
      medium: '#0f62fe',
      high: '#ff832b',
      critical: '#da1e28'
    };
    return colors[severity] || '#8d8d8d';
  };

  const getSeverityIcon = (severity) => {
    const icons = {
      low: '✓',
      medium: '⚠',
      high: '⚠',
      critical: '⚠'
    };
    return icons[severity] || '•';
  };

  const getEventIcon = (eventType) => {
    const icons = {
      pandemic: '🦠',
      war: '⚔️',
      natural_disaster: '🌪️',
      flight_cancellation: '✈️',
      terrorism: '💣',
      political_instability: '🏛️',
      economic_crisis: '💰',
      civil_unrest: '🔥'
    };
    return icons[eventType] || '⚠️';
  };

  const filteredRisks = risks.filter(risk => {
    if (filter === 'all') return true;
    if (filter === 'active') return !risk.end_date;
    if (filter === 'historical') return risk.end_date;
    return true;
  });

  const activeCount = risks.filter(r => !r.end_date).length;
  const historicalCount = risks.filter(r => r.end_date).length;

  if (loading) {
    return (
      <div className="risk-monitor">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading risk events...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="risk-monitor">
      <div className="page-header">
        <div className="header-content">
          <div className="header-icon">⚠️</div>
          <div>
            <h1>Global Risk Monitor</h1>
            <p>Real-time monitoring of force majeure events</p>
          </div>
        </div>
        
        <div className="stats-summary">
          <div className="stat-item">
            <span className="stat-value">{activeCount}</span>
            <span className="stat-label">Active Events</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{historicalCount}</span>
            <span className="stat-label">Historical</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{risks.length}</span>
            <span className="stat-label">Total Events</span>
          </div>
        </div>
      </div>

      <div className="filter-section">
        <div className="filter-buttons">
          <button 
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            All Events ({risks.length})
          </button>
          <button 
            className={`filter-btn ${filter === 'active' ? 'active' : ''}`}
            onClick={() => setFilter('active')}
          >
            Active ({activeCount})
          </button>
          <button 
            className={`filter-btn ${filter === 'historical' ? 'active' : ''}`}
            onClick={() => setFilter('historical')}
          >
            Historical ({historicalCount})
          </button>
        </div>
        <button 
          className="add-risk-btn"
          onClick={() => setShowAddModal(true)}
        >
          <span className="btn-icon">➕</span>
          Add Risk Event
        </button>
      </div>

      {filteredRisks.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🌍</div>
          <h3>No {filter !== 'all' ? filter : ''} risk events</h3>
          <p>There are currently no {filter !== 'all' ? filter : ''} force majeure events to display.</p>
        </div>
      ) : (
        <div className="risks-grid">
          {filteredRisks.map((risk) => (
            <div 
              key={risk.id} 
              className={`risk-card ${risk.end_date ? 'historical' : 'active'}`}
              style={{ '--severity-color': getSeverityColor(risk.severity) }}
            >
              <div className="risk-card-header">
                <div className="event-icon">{getEventIcon(risk.event_type)}</div>
                <div className="severity-badge" style={{ backgroundColor: getSeverityColor(risk.severity) }}>
                  <span className="severity-icon">{getSeverityIcon(risk.severity)}</span>
                  <span className="severity-text">{risk.severity}</span>
                </div>
              </div>

              <div className="risk-card-body">
                <div className="event-type">{risk.event_type.replace(/_/g, ' ')}</div>
                <h3 className="region-name">{risk.affected_region}</h3>
                <p className="risk-description">{risk.description}</p>
              </div>

              <div className="risk-card-footer">
                <div className="date-info">
                  <div className="date-item">
                    <span className="date-label">Started</span>
                    <span className="date-value">{format(new Date(risk.start_date), 'MMM dd, yyyy')}</span>
                  </div>
                  {risk.end_date && (
                    <div className="date-item">
                      <span className="date-label">Ended</span>
                      <span className="date-value">{format(new Date(risk.end_date), 'MMM dd, yyyy')}</span>
                    </div>
                  )}
                  {!risk.end_date && (
                    <div className="status-badge active-badge">
                      <span className="pulse"></span>
                      Active
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Risk Event Modal */}
      {showAddModal && (
        <>
          <div className="modal-overlay" onClick={() => setShowAddModal(false)}></div>
          <div className="modal-container">
            <div className="modal-header">
              <h2>➕ Add New Risk Event</h2>
              <button className="close-btn" onClick={() => setShowAddModal(false)}>×</button>
            </div>
            
            <form onSubmit={handleAddRisk} className="modal-form">
              <div className="form-row">
                <div className="form-group">
                  <label>Event Type *</label>
                  <select 
                    name="event_type" 
                    value={formData.event_type}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="pandemic">🦠 Pandemic</option>
                    <option value="war">⚔️ War/Conflict</option>
                    <option value="natural_disaster">🌪️ Natural Disaster</option>
                    <option value="flight_cancellation">✈️ Flight Cancellation</option>
                    <option value="terrorism">💣 Terrorism</option>
                    <option value="political_instability">🏛️ Political Instability</option>
                    <option value="economic_crisis">💰 Economic Crisis</option>
                    <option value="civil_unrest">🔥 Civil Unrest</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Severity *</label>
                  <select 
                    name="severity" 
                    value={formData.severity}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="critical">Critical</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Affected Region *</label>
                <input 
                  type="text"
                  name="affected_region"
                  value={formData.affected_region}
                  onChange={handleInputChange}
                  placeholder="e.g., Ukraine, Middle East, Japan"
                  required
                />
              </div>

              <div className="form-group">
                <label>Description *</label>
                <textarea 
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  placeholder="Describe the risk event and its impact..."
                  rows="4"
                  required
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Start Date *</label>
                  <input 
                    type="date"
                    name="start_date"
                    value={formData.start_date}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>End Date (Optional)</label>
                  <input 
                    type="date"
                    name="end_date"
                    value={formData.end_date}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              <div className="form-group checkbox-group">
                <label>
                  <input 
                    type="checkbox"
                    name="is_active"
                    checked={formData.is_active}
                    onChange={handleInputChange}
                  />
                  <span>Mark as Active Event</span>
                </label>
              </div>

              <div className="modal-actions">
                <button type="button" className="btn-secondary" onClick={() => setShowAddModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Add Risk Event
                </button>
              </div>
            </form>
          </div>
        </>
      )}
    </div>
  );
};

export default RiskMonitor;

// Made with Bob
