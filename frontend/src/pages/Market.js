import React, { useState, useEffect } from 'react';
import { getTrending, searchAssets, getHistoricalData, buyAsset, getAssetInfo } from '../services/api';
import PortfolioChart from '../components/PortfolioChart';
import TradeModal from '../components/TradeModal';
import '../styles/Market.css';

function Market() {
  const [trending, setTrending] = useState({ stocks: [], crypto: [] });
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [assetInfo, setAssetInfo] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [timePeriod, setTimePeriod] = useState('1mo');
  const [tradeModalOpen, setTradeModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrending();
  }, []);

  const fetchTrending = async () => {
    try {
      const result = await getTrending();
      if (result.success) {
        setTrending(result.trending || { stocks: [], crypto: [] });
      }
    } catch (error) {
      console.error('Error fetching trending:', error);
      setTrending({ stocks: [], crypto: [] });
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    try {
      const result = await searchAssets(searchQuery);
      if (result.success) {
        setSearchResults(result.results);
      }
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults([]);
    }
  };

  const handleSelectAsset = async (ticker, type) => {
    setSelectedAsset({ ticker, type });
    setAssetInfo(null);
    setHistoricalData([]);
    
    try {
      // Fetch asset info and historical data
      const [info, history] = await Promise.all([
        getAssetInfo(ticker, type).catch(err => ({ success: false })),
        getHistoricalData(ticker, type, timePeriod).catch(err => ({ success: false, data: [] })),
      ]);

      if (info.success) {
        setAssetInfo(info);
      } else {
        console.error('Failed to fetch asset info');
      }

      if (history.success) {
        setHistoricalData(history.data || []);
      } else {
        setHistoricalData([]);
      }
    } catch (error) {
      console.error('Error fetching asset details:', error);
      setAssetInfo(null);
      setHistoricalData([]);
    }
  };

  const handleTimePeriodChange = async (period) => {
    setTimePeriod(period);
    if (selectedAsset) {
      try {
        const result = await getHistoricalData(selectedAsset.ticker, selectedAsset.type, period);
        if (result.success) {
          setHistoricalData(result.data || []);
        } else {
          setHistoricalData([]);
        }
      } catch (error) {
        console.error('Error fetching historical data:', error);
        setHistoricalData([]);
      }
    }
  };

  const handleBuyClick = () => {
    setTradeModalOpen(true);
  };

  const handleConfirmBuy = async (ticker, assetType, quantity) => {
    await buyAsset(ticker, assetType, quantity);
    // Optionally refresh or show success message
  };

  return (
    <div className="market">
      <div className="market-header">
        <h1>Market Explorer</h1>
        <form className="search-bar" onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Search stocks or crypto (e.g., AAPL, BTC)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit">🔍 Search</button>
        </form>
      </div>

      {/* Search Results */}
      {searchResults.length > 0 && (
        <div className="search-results">
          <h2>Search Results</h2>
          <div className="results-grid">
            {searchResults.map((result) => (
              <div
                key={result.symbol}
                className="result-card"
                onClick={() => handleSelectAsset(result.symbol, result.type)}
              >
                <h3>{result.symbol}</h3>
                <p>{result.name}</p>
                <span className="asset-type">{result.type}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Selected Asset Details */}
      {selectedAsset && assetInfo && (
        <div className="asset-details">
          <div className="asset-header">
            <div>
              <h2>{selectedAsset.ticker}</h2>
              <p>{assetInfo.name}</p>
            </div>
            <button className="btn btn-buy" onClick={handleBuyClick}>
              Buy {selectedAsset.ticker}
            </button>
          </div>

          <div className="asset-stats">
            <div className="stat-card">
              <span className="stat-label">Current Price</span>
              <span className="stat-value">${assetInfo.price?.toFixed(2) || 'N/A'}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Market Cap</span>
              <span className="stat-value">
                ${(assetInfo.market_cap / 1e9)?.toFixed(2) || 'N/A'}B
              </span>
            </div>
            {selectedAsset.type === 'stock' && assetInfo.pe_ratio && (
              <div className="stat-card">
                <span className="stat-label">P/E Ratio</span>
                <span className="stat-value">{assetInfo.pe_ratio?.toFixed(2)}</span>
              </div>
            )}
            {selectedAsset.type === 'stock' && (
              <>
                <div className="stat-card">
                  <span className="stat-label">52W High</span>
                  <span className="stat-value">${assetInfo['52w_high']?.toFixed(2) || 'N/A'}</span>
                </div>
                <div className="stat-card">
                  <span className="stat-label">52W Low</span>
                  <span className="stat-value">${assetInfo['52w_low']?.toFixed(2) || 'N/A'}</span>
                </div>
              </>
            )}
          </div>

          {/* Time Period Selector */}
          <div className="time-period-selector">
            {['1d', '1w', '1mo', '3mo', '1y'].map((period) => (
              <button
                key={period}
                className={`period-btn ${timePeriod === period ? 'active' : ''}`}
                onClick={() => handleTimePeriodChange(period)}
              >
                {period.toUpperCase()}
              </button>
            ))}
          </div>

          {/* Historical Chart */}
          {historicalData.length > 0 && (
            <PortfolioChart
              data={historicalData}
              title={`${selectedAsset.ticker} Price History`}
            />
          )}

          {/* Description */}
          {assetInfo.description && (
            <div className="asset-description">
              <h3>About</h3>
              <p>{assetInfo.description}</p>
            </div>
          )}
        </div>
      )}

      {/* Trending Assets */}
      {!selectedAsset && (
        <div className="trending-section">
          <div className="trending-group">
            <h2>📈 Trending Stocks</h2>
            {trending.stocks && trending.stocks.length > 0 ? (
              <div className="trending-grid">
                {trending.stocks.map((stock, index) => (
                  <div
                    key={stock.ticker || `stock-${index}`}
                    className="trending-card"
                    onClick={() => handleSelectAsset(stock.ticker, 'stock')}
                  >
                    <h3>{stock.ticker}</h3>
                    <p className="price">${stock.price?.toFixed(2) || 'N/A'}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-state">Loading trending stocks...</p>
            )}
          </div>

          <div className="trending-group">
            <h2>₿ Trending Crypto</h2>
            {trending.crypto && trending.crypto.length > 0 ? (
              <div className="trending-grid">
                {trending.crypto.map((crypto, index) => (
                  <div
                    key={crypto.ticker || `crypto-${index}`}
                    className="trending-card"
                    onClick={() => handleSelectAsset(crypto.ticker, 'crypto')}
                  >
                    <h3>{crypto.ticker}</h3>
                    <p className="price">${crypto.price?.toFixed(2) || 'N/A'}</p>
                    <p className={`change ${(crypto.change_24h || 0) >= 0 ? 'profit' : 'loss'}`}>
                      {(crypto.change_24h || 0) >= 0 ? '+' : ''}{crypto.change_24h?.toFixed(2) || '0.00'}%
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-state">Loading trending crypto...</p>
            )}
          </div>
        </div>
      )}

      {/* Trade Modal */}
      {tradeModalOpen && selectedAsset && assetInfo && (
        <TradeModal
          asset={{
            ticker: selectedAsset.ticker,
            asset_type: selectedAsset.type,
            current_price: assetInfo.price,
          }}
          type="buy"
          onClose={() => setTradeModalOpen(false)}
          onConfirm={handleConfirmBuy}
        />
      )}
    </div>
  );
}

export default Market;

