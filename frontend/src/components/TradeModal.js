import React, { useState } from 'react';
import '../styles/TradeModal.css';

function TradeModal({ asset, type, onClose, onConfirm }) {
  const [quantity, setQuantity] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const qty = parseFloat(quantity);
    if (isNaN(qty) || qty <= 0) {
      setError('Please enter a valid quantity');
      return;
    }

    if (type === 'sell' && asset.quantity && qty > asset.quantity) {
      setError(`You only have ${asset.quantity} ${asset.ticker}`);
      return;
    }

    setLoading(true);
    try {
      await onConfirm(asset.ticker, asset.asset_type, qty);
      onClose();
    } catch (err) {
      setError(err.message || 'Transaction failed');
    } finally {
      setLoading(false);
    }
  };

  const estimatedCost = parseFloat(quantity) * (asset.current_price || 0);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{type === 'buy' ? 'Buy' : 'Sell'} {asset.ticker}</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          <div className="asset-info">
            <div className="info-row">
              <span>Current Price:</span>
              <span className="price">${asset.current_price?.toFixed(2) || '0.00'}</span>
            </div>
            {type === 'sell' && asset.quantity !== undefined && (
              <div className="info-row">
                <span>Available:</span>
                <span>{asset.quantity.toFixed(4)} {asset.ticker}</span>
              </div>
            )}
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="quantity">Quantity</label>
              <input
                id="quantity"
                type="number"
                step="0.0001"
                min="0"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                placeholder="Enter quantity"
                autoFocus
              />
            </div>

            {quantity && !isNaN(parseFloat(quantity)) && (
              <div className="estimated-cost">
                <span>Estimated {type === 'buy' ? 'Cost' : 'Revenue'}:</span>
                <span className="amount">${estimatedCost.toFixed(2)}</span>
              </div>
            )}

            {error && <div className="error-message">{error}</div>}

            <div className="modal-actions">
              <button type="button" className="btn btn-secondary" onClick={onClose}>
                Cancel
              </button>
              <button 
                type="submit" 
                className={`btn ${type === 'buy' ? 'btn-buy' : 'btn-sell'}`}
                disabled={loading}
              >
                {loading ? 'Processing...' : `Confirm ${type === 'buy' ? 'Buy' : 'Sell'}`}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default TradeModal;

