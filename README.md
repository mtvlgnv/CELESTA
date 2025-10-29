# CELESTA - Stock/Crypto Trading Simulation Game

A modern web application that allows users to simulate stock and cryptocurrency trading with unlimited virtual buying power. Track your portfolio performance in real-time with beautiful interactive charts.

## Features

- 🔐 Multi-user authentication system
- 📈 Real-time stock and cryptocurrency price tracking
- 💰 Unlimited virtual trading (no balance restrictions)
- 📊 Interactive portfolio performance graphs using ApexCharts
- 🔍 Detailed market data (historical charts, volume, market cap, etc.)
- 📝 Transaction history tracking
- 🌙 Modern dark-themed UI inspired by Grok/Perplexity
- ⚡ Auto-refresh every 5 seconds with smooth animations

## Tech Stack

### Backend
- **Flask** - Python web framework
- **SQLite** - Database for user accounts and portfolios
- **yfinance** - Stock market data
- **CoinGecko API** - Cryptocurrency data
- **pandas** - Data manipulation

### Frontend
- **React** - UI framework
- **ApexCharts** - Interactive charts and graphs
- **CSS** - Modern styling with dark theme

## Project Structure

```
CELESTA_NEW/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── routes/
│   ├── utils/
│   └── database.db
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   └── package.json
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup Instructions

### Backend Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
cd backend
python app.py
```

### Frontend Setup
```bash
# Install dependencies
cd frontend
npm install

# Run React development server
npm start
```

## Usage

1. Sign up for an account
2. Browse stocks and cryptocurrencies in the Market page
3. Buy/sell assets with unlimited virtual money
4. Track your portfolio performance on the Dashboard
5. View detailed charts with customizable time ranges

## Development Notes

- Portfolio value snapshots are stored hourly
- Price data updates every 5 seconds when viewing charts
- Rate limits: Designed for ~10 concurrent users
- Simple password hashing for educational purposes

## Author

Built as a portfolio project showcasing basic data science and software engineering skills.

## License

MIT

