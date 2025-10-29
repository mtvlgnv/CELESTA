from flask import Flask, jsonify, session
from flask_cors import CORS
import os
from datetime import timedelta

# Import database initialization
from backend.models.database import init_db

# Import blueprints
from backend.routes.auth import auth_bp
from backend.routes.portfolio import portfolio_bp
from backend.routes.market import market_bp

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'celesta-super-secret-key-change-in-production')
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    
    # Enable CORS for frontend communication
    CORS(app, 
         supports_credentials=True, 
         origins=['http://localhost:3000', 'http://localhost:3001'],
         allow_headers=['Content-Type', 'Authorization'],
         expose_headers=['Content-Type'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
    app.register_blueprint(market_bp, url_prefix='/api/market')
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'name': 'CELESTA API',
            'version': '1.0.0',
            'description': 'Stock/Crypto Trading Simulation Game API',
            'status': 'running',
            'endpoints': {
                'auth': '/api/auth',
                'portfolio': '/api/portfolio',
                'market': '/api/market'
            }
        })
    
    # Test session endpoint
    @app.route('/api/test-session')
    def test_session():
        if 'test' not in session:
            session['test'] = 'working'
        return jsonify({
            'success': True,
            'session_working': True,
            'session_id': session.get('test')
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'message': 'API is running'}), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*50)
    print("🚀 CELESTA API Server Starting...")
    print("="*50)
    print("📊 Stock/Crypto Trading Simulation Game")
    print("🌐 API running on: http://localhost:5001")
    print("📖 API Docs: http://localhost:5001")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

