from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database setup
DATABASE = 'pocket_money.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_db():
    """Initialize the database with tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance INTEGER DEFAULT 0,
            total_spent INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create spending history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spending_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            note TEXT,
            spent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

# Initialize database when app starts
init_db()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    session['current_view'] = session.get('current_view', 'menu')

    # Get user data from database
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    # Get spending history
    history = conn.execute(
        'SELECT * FROM spending_history WHERE user_id = ? ORDER BY spent_at DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    return render_template('index.html',
                         username=user['username'],
                         balance=user['balance'],
                         total_spent=user['total_spent'],
                         spending_history=history,
                         current_view=session.get('current_view', 'menu'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                          (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                       (username, password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists', 'error')
            conn.close()
    
    return render_template('register.html')

@app.route('/choose', methods=['POST'])
def choose():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    choice = request.form.get('choice', 'menu')
    option_map = {
        '1': 'spend',
        '2': 'balance',
        '3': 'history',
        '4': 'menu'
    }

    session['current_view'] = option_map.get(choice, 'menu')
    return redirect(url_for('index'))

@app.route('/set_balance', methods=['POST'])
def set_balance():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    balance = int(request.form.get('balance', 0))

    conn = get_db_connection()
    conn.execute('UPDATE users SET balance = ? WHERE id = ?',
               (balance, session['user_id']))
    conn.commit()
    conn.close()

    session['current_view'] = 'menu'
    flash(f'Balance set to ₦{balance}', 'success')
    return redirect(url_for('index'))

@app.route('/spend', methods=['POST'])
def spend():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    spent = int(request.form.get('spent', 0))
    note = request.form.get('note', '').strip()

    conn = get_db_connection()
    user = conn.execute('SELECT balance, total_spent FROM users WHERE id = ?',
                       (session['user_id'],)).fetchone()
    balance = user['balance']
    total_spent = user['total_spent']

    # Same validation logic as original code
    if spent <= 0:
        flash('Please enter a valid amount.', 'error')
    elif spent > balance:
        flash('Insufficient balance!', 'error')
    else:
        # Update balance and total spent
        new_balance = balance - spent
        new_total_spent = total_spent + spent

        conn.execute('UPDATE users SET balance = ?, total_spent = ? WHERE id = ?',
                   (new_balance, new_total_spent, session['user_id']))

        # Add to spending history
        conn.execute('INSERT INTO spending_history (user_id, amount, note) VALUES (?, ?, ?)',
                   (session['user_id'], spent, note if note else 'No description'))

        conn.commit()

        message = f'Money spent successfully. Remaining Balance: ₦{new_balance}'
        if new_balance < 1000:
            message += ' ⚠️ Warning: Your balance is low!'

        flash(message, 'success')

    session['current_view'] = 'menu'
    conn.close()
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    # Delete all spending history
    conn.execute('DELETE FROM spending_history WHERE user_id = ?', (session['user_id'],))
    # Reset balance and total spent
    conn.execute('UPDATE users SET balance = 0, total_spent = 0 WHERE id = ?',
               (session['user_id'],))
    conn.commit()
    conn.close()

    session['current_view'] = 'menu'
    flash('All data has been reset!', 'success')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
