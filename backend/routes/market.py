from flask import Blueprint, request, jsonify
from backend.utils.data_fetcher import (
    get_current_price,
    get_historical_data,
    get_asset_info,
    search_stocks,
    search_crypto,
    is_crypto
)

market_bp = Blueprint('market', __name__)

@market_bp.route('/price/<ticker>', methods=['GET'])
def get_price(ticker):
    """Get current price for an asset."""
    asset_type = request.args.get('type', 'stock')  # 'stock' or 'crypto'
    
    result = get_current_price(ticker.upper(), asset_type)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404

@market_bp.route('/history/<ticker>', methods=['GET'])
def get_history(ticker):
    """Get historical data for an asset."""
    asset_type = request.args.get('type', 'stock')
    period = request.args.get('period', '1mo')  # 1d, 1w, 1mo, 3mo, 1y
    
    result = get_historical_data(ticker.upper(), asset_type, period)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404

@market_bp.route('/info/<ticker>', methods=['GET'])
def get_info(ticker):
    """Get detailed information about an asset."""
    asset_type = request.args.get('type', 'stock')
    
    result = get_asset_info(ticker.upper(), asset_type)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404

@market_bp.route('/search', methods=['GET'])
def search():
    """Search for stocks and cryptocurrencies."""
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'all')  # 'stock', 'crypto', or 'all'
    
    if not query:
        return jsonify({'success': False, 'error': 'Query parameter required'}), 400
    
    results = []
    
    if search_type in ['stock', 'all']:
        stock_results = search_stocks(query)
        if stock_results['success']:
            results.extend(stock_results['results'])
    
    if search_type in ['crypto', 'all']:
        crypto_results = search_crypto(query)
        if crypto_results['success']:
            results.extend(crypto_results['results'])
    
    if results:
        return jsonify({'success': True, 'results': results}), 200
    else:
        return jsonify({'success': False, 'error': 'No results found'}), 404

@market_bp.route('/trending', methods=['GET'])
def get_trending():
    """Get trending/popular assets."""
    # Predefined list of popular stocks and cryptos
    popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META']
    popular_cryptos = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP']
    
    trending = {
        'stocks': [],
        'crypto': []
    }
    
    # Get current prices for popular stocks
    for ticker in popular_stocks:
        price_data = get_current_price(ticker, 'stock')
        if price_data['success']:
            trending['stocks'].append({
                'ticker': ticker,
                'price': price_data['price']
            })
    
    # Get current prices for popular cryptos
    for ticker in popular_cryptos:
        price_data = get_current_price(ticker, 'crypto')
        if price_data['success']:
            trending['crypto'].append({
                'ticker': ticker,
                'price': price_data['price'],
                'change_24h': price_data.get('change_24h', 0)
            })
    
    return jsonify({'success': True, 'trending': trending}), 200

@market_bp.route('/batch-prices', methods=['POST'])
def get_batch_prices():
    """Get current prices for multiple assets at once."""
    data = request.get_json()
    tickers = data.get('tickers', [])
    
    if not tickers:
        return jsonify({'success': False, 'error': 'No tickers provided'}), 400
    
    results = []
    
    for item in tickers:
        ticker = item.get('ticker', '').upper()
        asset_type = item.get('type', 'stock')
        
        price_data = get_current_price(ticker, asset_type)
        if price_data['success']:
            results.append({
                'ticker': ticker,
                'type': asset_type,
                'price': price_data['price'],
                'timestamp': price_data['timestamp']
            })
    
    return jsonify({'success': True, 'prices': results}), 200

