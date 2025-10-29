import React from 'react';
import '../styles/StockCard.css';

function StockCard({ asset, onBuy, onSell, showActions = true }) {
  const {
    ticker,
    asset_type,
    current_price,
    quantity,
    avg_buy_price,
    total_value,
    profit_loss,
    profit_loss_percent,
  } = asset;

  const isProfitable = (profit_loss || 0) >= 0;

  return (
    <div className="stock-card">
      <div className="stock-header">
        <div className="stock-info">
          <h3 className="stock-ticker">{ticker}</h3>
          <span className="stock-type">{asset_type === 'crypto' ? '₿' : '📈'} {asset_type}</span>
        </div>
        <div className="stock-price">
          <span className="price">${current_price?.toFixed(2) || '0.00'}</span>
        </div>
      </div>

      {quantity !== undefined && (
        <div className="stock-details">
          <div className="detail-row">
            <span className="detail-label">Quantity:</span>
            <span className="detail-value">{quantity.toFixed(4)}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Avg Buy Price:</span>
            <span className="detail-value">${avg_buy_price?.toFixed(2)}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Total Value:</span>
            <span className="detail-value">${total_value?.toFixed(2)}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">P/L:</span>
            <span className={`detail-value ${isProfitable ? 'profit' : 'loss'}`}>
              {isProfitable ? '+' : ''}${profit_loss?.toFixed(2)} ({isProfitable ? '+' : ''}{profit_loss_percent?.toFixed(2)}%)
            </span>
          </div>
        </div>
      )}

      {showActions && (
        <div className="stock-actions">
          {onBuy && (
            <button className="btn btn-buy" onClick={() => onBuy(asset)}>
              Buy
            </button>
          )}
          {onSell && quantity > 0 && (
            <button className="btn btn-sell" onClick={() => onSell(asset)}>
              Sell
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default StockCard;

