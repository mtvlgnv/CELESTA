from flask import Blueprint, request, jsonify, session
from backend.models.database import (
    get_user_portfolio, 
    add_to_portfolio, 
    remove_from_portfolio,
    add_transaction,
    get_user_transactions,
    get_portfolio_snapshots
)
from backend.utils.data_fetcher import get_current_price

portfolio_bp = Blueprint('portfolio', __name__)

def require_auth(f):
    """Decorator to require authentication."""
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@portfolio_bp.route('/holdings', methods=['GET'])
@require_auth
def get_holdings():
    """Get user's portfolio holdings."""
    user_id = session['user_id']
    holdings = get_user_portfolio(user_id)
    
    # Enrich with current prices
    for holding in holdings:
        price_data = get_current_price(holding['ticker'], holding['asset_type'])
        if price_data['success']:
            holding['current_price'] = price_data['price']
            holding['total_value'] = price_data['price'] * holding['quantity']
            holding['profit_loss'] = (price_data['price'] - holding['avg_buy_price']) * holding['quantity']
            holding['profit_loss_percent'] = ((price_data['price'] / holding['avg_buy_price']) - 1) * 100
        else:
            holding['current_price'] = 0
            holding['total_value'] = 0
            holding['profit_loss'] = 0
            holding['profit_loss_percent'] = 0
    
    return jsonify({'success': True, 'holdings': holdings}), 200

@portfolio_bp.route('/buy', methods=['POST'])
@require_auth
def buy_asset():
    """Buy an asset."""
    user_id = session['user_id']
    data = request.get_json()
    
    ticker = data.get('ticker', '').upper()
    asset_type = data.get('asset_type')  # 'stock' or 'crypto'
    quantity = data.get('quantity')
    
    if not ticker or not asset_type or not quantity:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    try:
        quantity = float(quantity)
        if quantity <= 0:
            return jsonify({'success': False, 'error': 'Quantity must be positive'}), 400
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid quantity'}), 400
    
    # Get current price
    price_data = get_current_price(ticker, asset_type)
    if not price_data['success']:
        return jsonify({'success': False, 'error': 'Could not fetch price'}), 400
    
    price = price_data['price']
    
    # Add to portfolio
    result = add_to_portfolio(user_id, ticker, asset_type, quantity, price)
    
    if result['success']:
        # Record transaction
        add_transaction(user_id, ticker, asset_type, 'buy', quantity, price)
        return jsonify({
            'success': True, 
            'message': f'Bought {quantity} {ticker} at ${price}',
            'total_cost': quantity * price
        }), 200
    else:
        return jsonify(result), 400

@portfolio_bp.route('/sell', methods=['POST'])
@require_auth
def sell_asset():
    """Sell an asset."""
    user_id = session['user_id']
    data = request.get_json()
    
    ticker = data.get('ticker', '').upper()
    asset_type = data.get('asset_type')
    quantity = data.get('quantity')
    
    if not ticker or not asset_type or not quantity:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    try:
        quantity = float(quantity)
        if quantity <= 0:
            return jsonify({'success': False, 'error': 'Quantity must be positive'}), 400
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid quantity'}), 400
    
    # Get current price
    price_data = get_current_price(ticker, asset_type)
    if not price_data['success']:
        return jsonify({'success': False, 'error': 'Could not fetch price'}), 400
    
    price = price_data['price']
    
    # Remove from portfolio
    result = remove_from_portfolio(user_id, ticker, quantity)
    
    if result['success']:
        # Record transaction
        add_transaction(user_id, ticker, asset_type, 'sell', quantity, price)
        return jsonify({
            'success': True,
            'message': f'Sold {quantity} {ticker} at ${price}',
            'total_revenue': quantity * price
        }), 200
    else:
        return jsonify(result), 400

@portfolio_bp.route('/transactions', methods=['GET'])
@require_auth
def get_transactions():
    """Get transaction history."""
    user_id = session['user_id']
    limit = request.args.get('limit', 50, type=int)
    
    transactions = get_user_transactions(user_id, limit)
    return jsonify({'success': True, 'transactions': transactions}), 200

@portfolio_bp.route('/value-history', methods=['GET'])
@require_auth
def get_value_history():
    """Get portfolio value history."""
    user_id = session['user_id']
    hours = request.args.get('hours', 24, type=int)
    
    snapshots = get_portfolio_snapshots(user_id, hours)
    return jsonify({'success': True, 'snapshots': snapshots}), 200

@portfolio_bp.route('/summary', methods=['GET'])
@require_auth
def get_portfolio_summary():
    """Get portfolio summary statistics."""
    user_id = session['user_id']
    holdings = get_user_portfolio(user_id)
    
    total_value = 0
    total_cost = 0
    
    for holding in holdings:
        price_data = get_current_price(holding['ticker'], holding['asset_type'])
        if price_data['success']:
            current_value = price_data['price'] * holding['quantity']
            cost = holding['avg_buy_price'] * holding['quantity']
            total_value += current_value
            total_cost += cost
    
    profit_loss = total_value - total_cost
    profit_loss_percent = ((total_value / total_cost) - 1) * 100 if total_cost > 0 else 0
    
    return jsonify({
        'success': True,
        'summary': {
            'total_value': round(total_value, 2),
            'total_cost': round(total_cost, 2),
            'profit_loss': round(profit_loss, 2),
            'profit_loss_percent': round(profit_loss_percent, 2),
            'holdings_count': len(holdings)
        }
    }), 200

