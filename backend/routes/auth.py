from flask import Blueprint, request, jsonify, session
from backend.models.database import create_user, authenticate_user, get_user_by_username

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Register a new user."""
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    result = create_user(username, email, password)
    
    if result['success']:
        session['user_id'] = result['user_id']
        session['username'] = username
        return jsonify({'success': True, 'message': 'User created successfully'}), 201
    else:
        return jsonify(result), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user."""
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Missing credentials'}), 400
    
    result = authenticate_user(username, password)
    
    if result['success']:
        session['user_id'] = result['user_id']
        session['username'] = result['username']
        return jsonify({'success': True, 'user': {'id': result['user_id'], 'username': result['username']}}), 200
    else:
        return jsonify(result), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Log out the current user."""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current logged-in user."""
    if 'user_id' in session:
        user = get_user_by_username(session['username'])
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
            }), 200
    return jsonify({'success': False, 'error': 'Not authenticated'}), 401

@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated."""
    if 'user_id' in session:
        return jsonify({'success': True, 'authenticated': True, 'user_id': session['user_id']}), 200
    return jsonify({'success': True, 'authenticated': False}), 200

