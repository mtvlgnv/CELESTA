import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important for session cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================
// AUTHENTICATION
// ============================================

export const signup = async (username, email, password) => {
  const response = await api.post('/auth/signup', { username, email, password });
  return response.data;
};

export const login = async (username, password) => {
  const response = await api.post('/auth/login', { username, password });
  return response.data;
};

export const logout = async () => {
  const response = await api.post('/auth/logout');
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

export const checkAuth = async () => {
  const response = await api.get('/auth/check');
  return response.data;
};

// ============================================
// PORTFOLIO
// ============================================

export const getHoldings = async () => {
  const response = await api.get('/portfolio/holdings');
  return response.data;
};

export const buyAsset = async (ticker, assetType, quantity) => {
  const response = await api.post('/portfolio/buy', {
    ticker,
    asset_type: assetType,
    quantity,
  });
  return response.data;
};

export const sellAsset = async (ticker, assetType, quantity) => {
  const response = await api.post('/portfolio/sell', {
    ticker,
    asset_type: assetType,
    quantity,
  });
  return response.data;
};

export const getTransactions = async (limit = 50) => {
  const response = await api.get(`/portfolio/transactions?limit=${limit}`);
  return response.data;
};

export const getPortfolioSummary = async () => {
  const response = await api.get('/portfolio/summary');
  return response.data;
};

export const getPortfolioValueHistory = async (hours = 24) => {
  const response = await api.get(`/portfolio/value-history?hours=${hours}`);
  return response.data;
};

// ============================================
// MARKET
// ============================================

export const getPrice = async (ticker, assetType = 'stock') => {
  const response = await api.get(`/market/price/${ticker}?type=${assetType}`);
  return response.data;
};

export const getHistoricalData = async (ticker, assetType = 'stock', period = '1mo') => {
  const response = await api.get(`/market/history/${ticker}?type=${assetType}&period=${period}`);
  return response.data;
};

export const getAssetInfo = async (ticker, assetType = 'stock') => {
  const response = await api.get(`/market/info/${ticker}?type=${assetType}`);
  return response.data;
};

export const searchAssets = async (query, searchType = 'all') => {
  const response = await api.get(`/market/search?q=${query}&type=${searchType}`);
  return response.data;
};

export const getTrending = async () => {
  const response = await api.get('/market/trending');
  return response.data;
};

export const getBatchPrices = async (tickers) => {
  const response = await api.post('/market/batch-prices', { tickers });
  return response.data;
};

export default api;

