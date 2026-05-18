import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Bookings API
export const bookingsAPI = {
  getAll: (skip = 0, limit = 100) => 
    api.get(`/bookings?skip=${skip}&limit=${limit}`),
  
  getById: (id) => 
    api.get(`/bookings/${id}`),
  
  create: (bookingData) => 
    api.post('/bookings', bookingData),
};

// Refund Estimation API
export const estimationAPI = {
  estimateRefund: (bookingId, payload = {}) =>
    api.post(`/estimate-refund/${bookingId}`, payload),
  
  getEstimates: (bookingId) =>
    api.get(`/estimates/${bookingId}`),
};

// Risk Events API
export const riskAPI = {
  getAll: (activeOnly = true) =>
    api.get(`/risk-events?active_only=${activeOnly}`),
  
  getByRegion: (region) =>
    api.get(`/risk-events/region/${region}`),

  create: (riskEventData) =>
    api.post('/risk-events', riskEventData),
};

// Historical Data API
export const historicalAPI = {
  getRefunds: (componentType = null, eventType = null, limit = 100) => {
    let url = `/historical-refunds?limit=${limit}`;
    if (componentType) url += `&component_type=${componentType}`;
    if (eventType) url += `&event_type=${eventType}`;
    return api.get(url);
  },
  
  getStatistics: () => 
    api.get('/statistics/refund-rates'),
};

// Provider Policies API
export const providersAPI = {
  getAll: (providerType = null) => {
    let url = '/providers';
    if (providerType) url += `?provider_type=${providerType}`;
    return api.get(url);
  },
  
  getByName: (providerName) => 
    api.get(`/providers/${providerName}`),
};

// Health Check
export const healthAPI = {
  check: () => api.get('/health'),
};

export default api;

// Made with Bob
