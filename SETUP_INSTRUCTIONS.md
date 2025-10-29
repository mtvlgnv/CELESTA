# CELESTA - Setup Instructions

## Quick Start Guide

### Step 1: Install Node.js

Download and install Node.js from: https://nodejs.org/
- Choose the LTS (Long Term Support) version
- Verify installation: `node --version` and `npm --version`

### Step 2: Set Up Backend

```bash
# Navigate to project directory
cd /Users/mtvlgnv/Desktop/CELESTA_NEW

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run the backend server
python3 run_backend.py
```

The backend API will be available at: `http://localhost:5000`

### Step 3: Set Up Frontend (After Installing Node.js)

```bash
# Navigate to frontend directory
cd frontend

# Initialize React app (only needed once)
npx create-react-app . --yes

# Install additional dependencies
npm install apexcharts react-apexcharts axios react-router-dom

# Start the frontend development server
npm start
```

The frontend will be available at: `http://localhost:3000`

## Running Both Servers

You'll need two terminal windows:

**Terminal 1 - Backend:**
```bash
cd /Users/mtvlgnv/Desktop/CELESTA_NEW
source venv/bin/activate
python3 run_backend.py
```

**Terminal 2 - Frontend:**
```bash
cd /Users/mtvlgnv/Desktop/CELESTA_NEW/frontend
npm start
```

## Project Status

### ✅ Completed
- [x] Git repository initialized and connected to GitHub
- [x] Backend Flask API structure
- [x] Database models (users, portfolio, transactions, snapshots)
- [x] User authentication system
- [x] Portfolio management endpoints
- [x] Market data endpoints (stocks & crypto)
- [x] Data fetching utilities (yfinance + CoinGecko)

### 🚧 To Do
- [ ] Install Node.js
- [ ] Set up React frontend
- [ ] Create UI components
- [ ] Implement ApexCharts visualizations
- [ ] Add dark theme styling
- [ ] Connect frontend to backend API
- [ ] Implement 5-second auto-refresh
- [ ] Test end-to-end functionality

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user
- `GET /api/auth/check` - Check authentication status

### Portfolio
- `GET /api/portfolio/holdings` - Get user's holdings
- `POST /api/portfolio/buy` - Buy an asset
- `POST /api/portfolio/sell` - Sell an asset
- `GET /api/portfolio/transactions` - Get transaction history
- `GET /api/portfolio/summary` - Get portfolio summary stats
- `GET /api/portfolio/value-history` - Get portfolio value over time

### Market
- `GET /api/market/price/<ticker>?type=stock` - Get current price
- `GET /api/market/history/<ticker>?type=stock&period=1mo` - Get historical data
- `GET /api/market/info/<ticker>?type=stock` - Get asset information
- `GET /api/market/search?q=AAPL` - Search for assets
- `GET /api/market/trending` - Get trending assets
- `POST /api/market/batch-prices` - Get multiple prices at once

## Tech Stack

**Backend:**
- Flask 3.0.0
- SQLite database
- yfinance (stock data)
- CoinGecko API (crypto data)

**Frontend (Pending Node.js install):**
- React
- ApexCharts
- Axios
- React Router

## Troubleshooting

### Flask Import Error
If you get `import flask` error, make sure you've activated the virtual environment and installed requirements:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Node.js Not Found
Download and install from: https://nodejs.org/

### Port Already in Use
If port 5000 or 3000 is already in use:
- Backend: Change port in `backend/app.py`
- Frontend: Set `PORT=3001` environment variable before `npm start`

## Next Steps

1. **Install Node.js** (if not already done)
2. **Test the backend**: Run `python3 run_backend.py` and visit http://localhost:5000
3. **Set up frontend**: Follow frontend/SETUP.md
4. **Start developing**: We'll build the UI components next!

