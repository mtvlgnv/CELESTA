import React from 'react';
import '../styles/Settings.css';

function Settings({ user }) {
  return (
    <div className="settings">
      <h1>Settings</h1>

      <div className="settings-section">
        <h2>Account Information</h2>
        <div className="info-grid">
          <div className="info-item">
            <label>Username</label>
            <p>{user?.username || 'N/A'}</p>
          </div>
          <div className="info-item">
            <label>Email</label>
            <p>{user?.email || 'N/A'}</p>
          </div>
          <div className="info-item">
            <label>Member Since</label>
            <p>{user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</p>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <h2>About CELESTA</h2>
        <p>
          CELESTA is a stock and cryptocurrency trading simulation game. 
          Practice your trading strategies with unlimited virtual money and real market data.
        </p>
        <div className="features-list">
          <div className="feature">
            <span className="icon">📊</span>
            <div>
              <h3>Real-time Data</h3>
              <p>Live stock and crypto prices updated every 5 seconds</p>
            </div>
          </div>
          <div className="feature">
            <span className="icon">💰</span>
            <div>
              <h3>Unlimited Trading</h3>
              <p>Buy as many assets as you want with no restrictions</p>
            </div>
          </div>
          <div className="feature">
            <span className="icon">📈</span>
            <div>
              <h3>Performance Tracking</h3>
              <p>Monitor your portfolio with beautiful interactive charts</p>
            </div>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <h2>Data Sources</h2>
        <ul className="data-sources">
          <li><strong>Stocks:</strong> Yahoo Finance (via yfinance)</li>
          <li><strong>Cryptocurrency:</strong> CoinGecko API</li>
        </ul>
      </div>
    </div>
  );
}

export default Settings;

