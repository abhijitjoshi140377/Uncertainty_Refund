import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { historicalAPI } from '../services/api';
import './Analytics.scss';

const Analytics = () => {
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [selectedStat, setSelectedStat] = useState(null);
  const [showEventTypesModal, setShowEventTypesModal] = useState(false);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const response = await historicalAPI.getStatistics();
      setStats(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="analytics-loading">
        <div className="spinner"></div>
        <p>Loading analytics...</p>
      </div>
    );
  }

  const filteredStats = selectedFilter === 'all'
    ? stats
    : stats.filter(s => s.component_type === selectedFilter);

  const chartData = filteredStats.map(stat => ({
    name: `${stat.component_type}\n${stat.event_type}`,
    fullName: `${stat.component_type} - ${stat.event_type}`,
    refund: parseFloat(stat.average_refund_percentage.toFixed(1)),
    cases: stat.total_cases,
    data: stat
  }));

  const componentTypes = ['all', ...new Set(stats.map(s => s.component_type))];
  
  // Calculate unique event types in filtered data
  const uniqueEventTypes = new Set(filteredStats.map(s => s.event_type));
  const totalEventTypes = uniqueEventTypes.size;

  const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a'];

  const handleBarClick = (data) => {
    setSelectedStat(data.data);
  };

  // Event types with descriptions and icons
  const eventTypesInfo = {
    'pandemic': {
      icon: '🦠',
      name: 'Pandemic',
      description: 'Global health emergencies like COVID-19, SARS, H1N1',
      examples: ['COVID-19 pandemic', 'SARS outbreak', 'H1N1 flu'],
      impact: 'Critical - 80-100% refunds typically granted'
    },
    'war': {
      icon: '⚔️',
      name: 'War/Conflict',
      description: 'Military conflicts, armed conflicts, civil wars',
      examples: ['Ukraine war', 'Middle East conflicts', 'Regional wars'],
      impact: 'Critical - 90-100% refunds'
    },
    'natural_disaster': {
      icon: '🌪️',
      name: 'Natural Disaster',
      description: 'Earthquakes, hurricanes, floods, tsunamis',
      examples: ['Turkey earthquake', 'Morocco earthquake', 'Hurricanes'],
      impact: 'High - 70-95% refunds'
    },
    'flight_cancellation': {
      icon: '✈️',
      name: 'Flight Cancellation',
      description: 'Airline operational issues, strikes, technical problems',
      examples: ['Airline strikes', 'Technical failures', 'Weather delays'],
      impact: 'Medium-High - 60-90% refunds'
    },
    'terrorism': {
      icon: '💣',
      name: 'Terrorism',
      description: 'Security threats, terrorist attacks, bombings',
      examples: ['Terror attacks', 'Security threats', 'Bombings'],
      impact: 'Critical - 85-100% refunds'
    },
    'political_instability': {
      icon: '🏛️',
      name: 'Political Instability',
      description: 'Government changes, coups, protests, civil unrest',
      examples: ['Myanmar crisis', 'Government coups', 'Mass protests'],
      impact: 'High - 75-95% refunds'
    },
    'economic_crisis': {
      icon: '💰',
      name: 'Economic Crisis',
      description: 'Currency collapse, banking crisis, sanctions',
      examples: ['Argentina crisis', 'Lebanon banking crisis', 'Sanctions'],
      impact: 'Medium-High - 60-85% refunds'
    },
    'civil_unrest': {
      icon: '🔥',
      name: 'Civil Unrest',
      description: 'Riots, protests, social upheaval',
      examples: ['Mass riots', 'Social protests', 'Public unrest'],
      impact: 'Medium-High - 65-85% refunds'
    }
  };

  // Get event types present in filtered data
  const getEventTypesBreakdown = () => {
    const breakdown = {};
    filteredStats.forEach(stat => {
      if (!breakdown[stat.event_type]) {
        breakdown[stat.event_type] = {
          count: 0,
          totalCases: 0,
          avgRefund: 0,
          components: []
        };
      }
      breakdown[stat.event_type].count++;
      breakdown[stat.event_type].totalCases += stat.total_cases;
      breakdown[stat.event_type].avgRefund += stat.average_refund_percentage;
      breakdown[stat.event_type].components.push({
        type: stat.component_type,
        refund: stat.average_refund_percentage,
        cases: stat.total_cases
      });
    });
    
    // Calculate averages
    Object.keys(breakdown).forEach(key => {
      breakdown[key].avgRefund = (breakdown[key].avgRefund / breakdown[key].count).toFixed(1);
    });
    
    return breakdown;
  };

  const eventTypesBreakdown = getEventTypesBreakdown();

  return (
    <div className="analytics">
      <div className="analytics-header">
        <div>
          <h1>📊 Refund Analytics</h1>
          <p className="subtitle">Historical refund data and statistics</p>
        </div>
        <div className="filter-buttons">
          {componentTypes.map(type => (
            <button
              key={type}
              className={`filter-btn ${selectedFilter === type ? 'active' : ''}`}
              onClick={() => setSelectedFilter(type)}
            >
              {type === 'all' ? '🌐 All' : `${type.charAt(0).toUpperCase()}${type.slice(1)}`}
            </button>
          ))}
        </div>
      </div>

      <div className="analytics-grid">
        {/* Main Chart */}
        <div className="card chart-card">
          <h3>Average Refund Percentage</h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={chartData} onClick={(e) => e && e.activePayload && handleBarClick(e.activePayload[0].payload)}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
              <XAxis
                dataKey="name"
                angle={-45}
                textAnchor="end"
                height={80}
                tick={{ fontSize: 11 }}
              />
              <YAxis label={{ value: 'Refund %', angle: -90, position: 'insideLeft' }} />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    return (
                      <div className="custom-tooltip">
                        <p className="tooltip-title">{payload[0].payload.fullName}</p>
                        <p className="tooltip-value">Refund: {payload[0].value}%</p>
                        <p className="tooltip-cases">Cases: {payload[0].payload.cases}</p>
                        <p className="tooltip-hint">Click for details →</p>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Bar
                dataKey="refund"
                fill="#667eea"
                cursor="pointer"
                radius={[8, 8, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Selected Stat Details */}
        {selectedStat && (
          <div className="card details-card">
            <div className="details-header">
              <h3>📋 Selected Details</h3>
              <button className="close-btn" onClick={() => setSelectedStat(null)}>×</button>
            </div>
            <div className="details-content">
              <div className="detail-row">
                <span className="detail-label">Component:</span>
                <span className="detail-value">{selectedStat.component_type}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Event Type:</span>
                <span className="detail-value">{selectedStat.event_type}</span>
              </div>
              <div className="detail-row highlight">
                <span className="detail-label">Avg Refund:</span>
                <span className="detail-value">{selectedStat.average_refund_percentage.toFixed(1)}%</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Total Cases:</span>
                <span className="detail-value">{selectedStat.total_cases}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Force Majeure:</span>
                <span className="detail-value">{selectedStat.force_majeure_cases}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Avg Amount:</span>
                <span className="detail-value">₹{selectedStat.average_refund_amount.toLocaleString('en-IN')}</span>
              </div>
            </div>
          </div>
        )}

        {/* Summary Stats */}
        <div className="summary-cards">
          <div className="summary-card">
            <div className="summary-icon">⚠️</div>
            <div className="summary-value">{totalEventTypes}</div>
            <div className="summary-label">Event Types</div>
          </div>
          <div className="summary-card">
            <div className="summary-icon">📈</div>
            <div className="summary-value">
              {filteredStats.length > 0
                ? (filteredStats.reduce((sum, s) => sum + s.average_refund_percentage, 0) / filteredStats.length).toFixed(1)
                : '0.0'}%
            </div>
            <div className="summary-label">Overall Avg Refund</div>
          </div>
          <div className="summary-card">
            <div className="summary-icon">🎯</div>
            <div className="summary-value">
              {filteredStats.reduce((sum, s) => sum + s.total_cases, 0)}
            </div>
            <div className="summary-label">Total Cases</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;

// Made with Bob
