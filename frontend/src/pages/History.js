import React, { useState, useEffect } from 'react';
import { getTransactions } from '../services/api';
import '../styles/History.css';

function History() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const result = await getTransactions(100);
      if (result.success) {
        setTransactions(result.transactions);
      }
    } catch (error) {
      console.error('Error fetching transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading transaction history...</p>
      </div>
    );
  }

  return (
    <div className="history">
      <h1>Transaction History</h1>

      {transactions.length === 0 ? (
        <div className="empty-state">
          <p>No transactions yet.</p>
          <p>Start trading to see your history here!</p>
        </div>
      ) : (
        <div className="transactions-table">
          <table>
            <thead>
              <tr>
                <th>Date & Time</th>
                <th>Ticker</th>
                <th>Type</th>
                <th>Action</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((tx) => (
                <tr key={tx.id}>
                  <td>{formatDate(tx.timestamp)}</td>
                  <td className="ticker">{tx.ticker}</td>
                  <td>
                    <span className="asset-type">{tx.asset_type}</span>
                  </td>
                  <td>
                    <span className={`action ${tx.transaction_type}`}>
                      {tx.transaction_type === 'buy' ? '📈 Buy' : '📉 Sell'}
                    </span>
                  </td>
                  <td>{tx.quantity.toFixed(4)}</td>
                  <td>${tx.price.toFixed(2)}</td>
                  <td className="total">
                    ${(tx.quantity * tx.price).toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default History;

