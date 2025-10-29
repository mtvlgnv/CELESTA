import React, { useState, useEffect, useCallback } from 'react';
import { getHoldings, getPortfolioSummary, getPortfolioValueHistory, sellAsset } from '../services/api';
import PortfolioChart from '../components/PortfolioChart';
import StockCard from '../components/StockCard';
import TradeModal from '../components/TradeModal';
import '../styles/Dashboard.css';

function Dashboard({ user }) {
  const [holdings, setHoldings] = useState([]);
  const [summary, setSummary] = useState(null);
  const [valueHistory, setValueHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [tradeModalOpen, setTradeModalOpen] = useState(false);
  const [tradeType, setTradeType] = useState('buy');
  const [autoRefresh, setAutoRefresh] = useState(true);

  const fetchData = useCallback(async () => {
    try {
      const [holdingsData, summaryData, historyData] = await Promise.all([
        getHoldings().catch(err => ({ success: false, holdings: [] })),
        getPortfolioSummary().catch(err => ({ success: false, summary: { total_value: 0, profit_loss: 0, profit_loss_percent: 0, holdings_count: 0 } })),
        getPortfolioValueHistory(24).catch(err => ({ success: false, snapshots: [] })),
      ]);

      if (holdingsData.success) {
        setHoldings(holdingsData.holdings || []);
      }

      if (summaryData.success) {
        setSummary(summaryData.summary);
      }

      if (historyData.success) {
        setValueHistory(historyData.snapshots || []);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Auto-refresh every 5 seconds
  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(() => {
      fetchData();
    }, 5000); // 5 seconds

    return () => clearInterval(interval);
  }, [autoRefresh, fetchData]);

  const handleSell = (asset) => {
    setSelectedAsset(asset);
    setTradeType('sell');
    setTradeModalOpen(true);
  };

  const handleConfirmSell = async (ticker, assetType, quantity) => {
    await sellAsset(ticker, assetType, quantity);
    await fetchData(); // Refresh data
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading your portfolio...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome back, {user?.username}!</h1>
        <div className="refresh-control">
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            <span className="slider"></span>
          </label>
          <span>Auto-refresh (5s)</span>
        </div>
      </div>

      {/* Portfolio Summary */}
      <div className="summary-cards">
        <div className="summary-card">
          <h3>Total Portfolio Value</h3>
          <p className="value">${summary?.total_value?.toFixed(2) || '0.00'}</p>
        </div>
        <div className="summary-card">
          <h3>Total P/L</h3>
          <p className={`value ${(summary?.profit_loss || 0) >= 0 ? 'profit' : 'loss'}`}>
            {(summary?.profit_loss || 0) >= 0 ? '+' : ''}${summary?.profit_loss?.toFixed(2) || '0.00'}
          </p>
        </div>
        <div className="summary-card">
          <h3>P/L Percentage</h3>
          <p className={`value ${(summary?.profit_loss_percent || 0) >= 0 ? 'profit' : 'loss'}`}>
            {(summary?.profit_loss_percent || 0) >= 0 ? '+' : ''}{summary?.profit_loss_percent?.toFixed(2) || '0.00'}%
          </p>
        </div>
        <div className="summary-card">
          <h3>Holdings</h3>
          <p className="value">{summary?.holdings_count || 0}</p>
        </div>
      </div>

      {/* Portfolio Chart */}
      {valueHistory.length > 0 && (
        <div className="chart-section">
          <PortfolioChart data={valueHistory} title="Portfolio Value (24h)" />
        </div>
      )}

      {/* Holdings */}
      <div className="holdings-section">
        <h2>Your Holdings</h2>
        {holdings.length === 0 ? (
          <div className="empty-state">
            <p>You don't have any holdings yet.</p>
            <p>Visit the <a href="/market">Market</a> to start trading!</p>
          </div>
        ) : (
          <div className="holdings-grid">
            {holdings.map((holding, index) => (
              <StockCard
                key={holding.id || `holding-${index}`}
                asset={holding}
                onSell={handleSell}
                showActions={true}
              />
            ))}
          </div>
        )}
      </div>

      {/* Trade Modal */}
      {tradeModalOpen && (
        <TradeModal
          asset={selectedAsset}
          type={tradeType}
          onClose={() => setTradeModalOpen(false)}
          onConfirm={handleConfirmSell}
        />
      )}
    </div>
  );
}

export default Dashboard;

