import sqlite3
from datetime import datetime
import hashlib
import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'celesta.db')

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Portfolio table - stores current holdings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            ticker TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            avg_buy_price REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, ticker)
        )
    ''')
    
    # Transactions table - stores all buy/sell transactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            ticker TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Portfolio snapshots - stores hourly portfolio value
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_value REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")

def hash_password(password):
    """Simple password hashing using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify a password against its hash."""
    return hash_password(password) == password_hash

# Database operations for users
def create_user(username, email, password):
    """Create a new user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {'success': True, 'user_id': user_id}
    except sqlite3.IntegrityError as e:
        conn.close()
        return {'success': False, 'error': 'Username or email already exists'}

def get_user_by_username(username):
    """Get user by username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def authenticate_user(username, password):
    """Authenticate a user."""
    user = get_user_by_username(username)
    if user and verify_password(password, user['password_hash']):
        return {'success': True, 'user_id': user['id'], 'username': user['username']}
    return {'success': False, 'error': 'Invalid credentials'}

# Database operations for portfolio
def add_to_portfolio(user_id, ticker, asset_type, quantity, price):
    """Add or update portfolio holding."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if holding exists
    cursor.execute(
        'SELECT * FROM portfolio WHERE user_id = ? AND ticker = ?',
        (user_id, ticker)
    )
    existing = cursor.fetchone()
    
    if existing:
        # Update existing holding
        new_quantity = existing['quantity'] + quantity
        new_avg_price = ((existing['avg_buy_price'] * existing['quantity']) + 
                        (price * quantity)) / new_quantity
        
        cursor.execute(
            'UPDATE portfolio SET quantity = ?, avg_buy_price = ? WHERE user_id = ? AND ticker = ?',
            (new_quantity, new_avg_price, user_id, ticker)
        )
    else:
        # Create new holding
        cursor.execute(
            'INSERT INTO portfolio (user_id, ticker, asset_type, quantity, avg_buy_price) VALUES (?, ?, ?, ?, ?)',
            (user_id, ticker, asset_type, quantity, price)
        )
    
    conn.commit()
    conn.close()
    return {'success': True}

def remove_from_portfolio(user_id, ticker, quantity):
    """Remove from portfolio holding."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT * FROM portfolio WHERE user_id = ? AND ticker = ?',
        (user_id, ticker)
    )
    holding = cursor.fetchone()
    
    if not holding:
        conn.close()
        return {'success': False, 'error': 'Holding not found'}
    
    if holding['quantity'] < quantity:
        conn.close()
        return {'success': False, 'error': 'Insufficient quantity'}
    
    new_quantity = holding['quantity'] - quantity
    
    if new_quantity == 0:
        cursor.execute('DELETE FROM portfolio WHERE user_id = ? AND ticker = ?', (user_id, ticker))
    else:
        cursor.execute(
            'UPDATE portfolio SET quantity = ? WHERE user_id = ? AND ticker = ?',
            (new_quantity, user_id, ticker)
        )
    
    conn.commit()
    conn.close()
    return {'success': True}

def get_user_portfolio(user_id):
    """Get all holdings for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM portfolio WHERE user_id = ?', (user_id,))
    holdings = cursor.fetchall()
    conn.close()
    return [dict(row) for row in holdings]

# Database operations for transactions
def add_transaction(user_id, ticker, asset_type, transaction_type, quantity, price):
    """Record a transaction."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO transactions (user_id, ticker, asset_type, transaction_type, quantity, price) VALUES (?, ?, ?, ?, ?, ?)',
        (user_id, ticker, asset_type, transaction_type, quantity, price)
    )
    conn.commit()
    conn.close()
    return {'success': True}

def get_user_transactions(user_id, limit=50):
    """Get transaction history for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
        (user_id, limit)
    )
    transactions = cursor.fetchall()
    conn.close()
    return [dict(row) for row in transactions]

# Database operations for portfolio snapshots
def add_portfolio_snapshot(user_id, total_value):
    """Add a portfolio value snapshot."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO portfolio_snapshots (user_id, total_value) VALUES (?, ?)',
        (user_id, total_value)
    )
    conn.commit()
    conn.close()
    return {'success': True}

def get_portfolio_snapshots(user_id, hours=24):
    """Get portfolio snapshots for a time period."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT * FROM portfolio_snapshots 
           WHERE user_id = ? 
           AND timestamp > datetime('now', '-' || ? || ' hours')
           ORDER BY timestamp ASC''',
        (user_id, hours)
    )
    snapshots = cursor.fetchall()
    conn.close()
    return [dict(row) for row in snapshots]

if __name__ == '__main__':
    init_db()

