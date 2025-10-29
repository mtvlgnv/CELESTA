import yfinance as yf
import requests
from datetime import datetime, timedelta
import pandas as pd

# CoinGecko API base URL (free, no API key needed)
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Mapping common crypto symbols to CoinGecko IDs
CRYPTO_ID_MAP = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'USDT': 'tether',
    'BNB': 'binancecoin',
    'SOL': 'solana',
    'XRP': 'ripple',
    'ADA': 'cardano',
    'DOGE': 'dogecoin',
    'AVAX': 'avalanche-2',
    'DOT': 'polkadot',
    'MATIC': 'matic-network',
    'LINK': 'chainlink',
    'UNI': 'uniswap',
    'ATOM': 'cosmos',
    'LTC': 'litecoin',
}

def is_crypto(ticker):
    """Check if ticker is a known cryptocurrency."""
    return ticker.upper() in CRYPTO_ID_MAP

def get_stock_current_price(ticker):
    """Get current price for a stock using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d', interval='1m')
        if len(data) > 0:
            current_price = data['Close'].iloc[-1]
            return {
                'success': True,
                'ticker': ticker,
                'price': round(float(current_price), 2),
                'timestamp': datetime.now().isoformat()
            }
        return {'success': False, 'error': 'No data available'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_crypto_current_price(ticker):
    """Get current price for a cryptocurrency using CoinGecko."""
    try:
        crypto_id = CRYPTO_ID_MAP.get(ticker.upper())
        if not crypto_id:
            return {'success': False, 'error': 'Cryptocurrency not found'}
        
        url = f"{COINGECKO_BASE_URL}/simple/price"
        params = {
            'ids': crypto_id,
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if crypto_id in data:
            return {
                'success': True,
                'ticker': ticker.upper(),
                'price': data[crypto_id]['usd'],
                'change_24h': data[crypto_id].get('usd_24h_change', 0),
                'market_cap': data[crypto_id].get('usd_market_cap', 0),
                'volume_24h': data[crypto_id].get('usd_24h_vol', 0),
                'timestamp': datetime.now().isoformat()
            }
        return {'success': False, 'error': 'No data available'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_current_price(ticker, asset_type):
    """Get current price for any asset (stock or crypto)."""
    if asset_type == 'crypto':
        return get_crypto_current_price(ticker)
    else:
        return get_stock_current_price(ticker)

def get_stock_historical_data(ticker, period='1mo', interval='1d'):
    """
    Get historical data for a stock.
    
    period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period, interval=interval)
        
        if len(data) > 0:
            # Convert to list of dictionaries
            historical_data = []
            for index, row in data.iterrows():
                historical_data.append({
                    'timestamp': index.isoformat(),
                    'open': round(float(row['Open']), 2),
                    'high': round(float(row['High']), 2),
                    'low': round(float(row['Low']), 2),
                    'close': round(float(row['Close']), 2),
                    'volume': int(row['Volume'])
                })
            
            return {
                'success': True,
                'ticker': ticker,
                'period': period,
                'data': historical_data
            }
        return {'success': False, 'error': 'No data available'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_crypto_historical_data(ticker, days=30):
    """Get historical data for a cryptocurrency."""
    try:
        crypto_id = CRYPTO_ID_MAP.get(ticker.upper())
        if not crypto_id:
            return {'success': False, 'error': 'Cryptocurrency not found'}
        
        url = f"{COINGECKO_BASE_URL}/coins/{crypto_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': days,
            'interval': 'daily' if days > 1 else 'hourly'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'prices' in data:
            historical_data = []
            for price_point in data['prices']:
                timestamp = datetime.fromtimestamp(price_point[0] / 1000)
                historical_data.append({
                    'timestamp': timestamp.isoformat(),
                    'price': round(price_point[1], 2)
                })
            
            return {
                'success': True,
                'ticker': ticker.upper(),
                'days': days,
                'data': historical_data
            }
        return {'success': False, 'error': 'No data available'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_historical_data(ticker, asset_type, period='1mo'):
    """Get historical data for any asset."""
    if asset_type == 'crypto':
        # Convert period to days for crypto
        days_map = {
            '1d': 1,
            '1w': 7,
            '1mo': 30,
            '3mo': 90,
            '1y': 365
        }
        days = days_map.get(period, 30)
        return get_crypto_historical_data(ticker, days)
    else:
        return get_stock_historical_data(ticker, period)

def get_stock_info(ticker):
    """Get detailed information about a stock."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            'success': True,
            'ticker': ticker,
            'name': info.get('longName', ticker),
            'sector': info.get('sector', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'volume': info.get('volume', 0),
            'avg_volume': info.get('averageVolume', 0),
            '52w_high': info.get('fiftyTwoWeekHigh', 0),
            '52w_low': info.get('fiftyTwoWeekLow', 0),
            'description': info.get('longBusinessSummary', 'No description available')
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_crypto_info(ticker):
    """Get detailed information about a cryptocurrency."""
    try:
        crypto_id = CRYPTO_ID_MAP.get(ticker.upper())
        if not crypto_id:
            return {'success': False, 'error': 'Cryptocurrency not found'}
        
        url = f"{COINGECKO_BASE_URL}/coins/{crypto_id}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'community_data': 'false',
            'developer_data': 'false'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        market_data = data.get('market_data', {})
        
        return {
            'success': True,
            'ticker': ticker.upper(),
            'name': data.get('name', ticker),
            'symbol': data.get('symbol', ticker).upper(),
            'market_cap': market_data.get('market_cap', {}).get('usd', 0),
            'total_volume': market_data.get('total_volume', {}).get('usd', 0),
            'high_24h': market_data.get('high_24h', {}).get('usd', 0),
            'low_24h': market_data.get('low_24h', {}).get('usd', 0),
            'price_change_24h': market_data.get('price_change_percentage_24h', 0),
            'circulating_supply': market_data.get('circulating_supply', 0),
            'description': data.get('description', {}).get('en', 'No description available')
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_asset_info(ticker, asset_type):
    """Get detailed information about any asset."""
    if asset_type == 'crypto':
        return get_crypto_info(ticker)
    else:
        return get_stock_info(ticker)

def search_stocks(query):
    """Search for stocks by query."""
    try:
        # Using yfinance search functionality
        # This is a simple implementation - you might want to use a better search API
        ticker = yf.Ticker(query.upper())
        info = ticker.info
        
        if 'symbol' in info:
            return {
                'success': True,
                'results': [{
                    'symbol': info.get('symbol', query.upper()),
                    'name': info.get('longName', query.upper()),
                    'type': 'stock'
                }]
            }
        return {'success': False, 'error': 'No results found'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def search_crypto(query):
    """Search for cryptocurrencies by query."""
    query_upper = query.upper()
    results = []
    
    for symbol, crypto_id in CRYPTO_ID_MAP.items():
        if query_upper in symbol or query.lower() in crypto_id:
            results.append({
                'symbol': symbol,
                'name': crypto_id.replace('-', ' ').title(),
                'type': 'crypto'
            })
    
    if results:
        return {'success': True, 'results': results}
    return {'success': False, 'error': 'No results found'}

