# Frontend Setup Guide

## Prerequisites

You need to install Node.js first:
- Download from: https://nodejs.org/
- Install the LTS version (recommended)
- Verify installation: `node --version` and `npm --version`

## Setup Instructions

Once Node.js is installed:

### 1. Create React App

```bash
cd /Users/mtvlgnv/Desktop/CELESTA_NEW/frontend
npx create-react-app . --yes
```

### 2. Install Dependencies

```bash
npm install apexcharts react-apexcharts
npm install axios
npm install react-router-dom
```

### 3. Project Structure

The frontend will have this structure:
```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── Navbar.js
│   │   ├── StockCard.js
│   │   ├── PortfolioChart.js
│   │   └── ...
│   ├── pages/           # Page components
│   │   ├── Login.js
│   │   ├── Signup.js
│   │   ├── Dashboard.js
│   │   ├── Market.js
│   │   └── Settings.js
│   ├── services/        # API service layer
│   │   └── api.js
│   ├── styles/          # CSS files
│   │   └── App.css
│   ├── App.js           # Main app component
│   └── index.js         # Entry point
└── package.json
```

### 4. Development

```bash
# Start the development server
npm start
```

The app will run on http://localhost:3000

## Next Steps

After setting up React, we'll implement:
1. Authentication pages (Login/Signup)
2. Dashboard with portfolio charts
3. Market page for browsing and buying assets
4. Real-time data updates
5. Dark theme UI

## API Connection

The frontend will connect to the Flask backend at:
- `http://localhost:5000/api/`

Make sure the backend is running before testing the frontend!

