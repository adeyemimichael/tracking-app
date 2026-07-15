from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Initialize session data
def init_session():
    if 'balance' not in session:
        session['balance'] = 0
        session['total_spent'] = 0
        session['spending_history'] = []
        session['current_view'] = 'menu'  # Track which view to show

@app.route('/')
def index():
    init_session()
    return render_template('index.html', 
                         balance=session.get('balance', 0),
                         total_spent=session.get('total_spent', 0),
                         spending_history=session.get('spending_history', []),
                         current_view=session.get('current_view', 'menu'),
                         message=session.pop('message', None),
                         message_type=session.pop('message_type', None))

@app.route('/set_balance', methods=['POST'])
def set_balance():
    balance = int(request.form.get('balance', 0))
    session['balance'] = balance
    session['total_spent'] = 0
    session['spending_history'] = []
    session['current_view'] = 'menu'
    return redirect(url_for('index'))

@app.route('/choose', methods=['POST'])
def choose():
    choice = request.form.get('choice')
    session['current_view'] = choice
    return redirect(url_for('index'))

@app.route('/spend', methods=['POST'])
def spend():
    init_session()
    spent = int(request.form.get('spent', 0))
    note = request.form.get('note', '').strip()
    balance = session['balance']
    
    message = ""
    message_type = ""
    
    # OPTION 1 — Spend Money (same logic as original code)
    if spent <= 0:
        message = "Please enter a valid amount."
        message_type = "error"
    elif spent > balance:
        message = "Insufficient balance!"
        message_type = "error"
    else:
        balance -= spent
        session['total_spent'] += spent
        
        # Store spending with note as a dictionary
        spending_entry = {
            'amount': spent,
            'note': note if note else 'No description'
        }
        session['spending_history'].append(spending_entry)
        session['balance'] = balance
        
        message = f"Money spent successfully. Remaining Balance: ₦{balance}"
        message_type = "success"
        
        if balance < 1000:
            message += " ⚠️ Warning: Your balance is low!"
    
    session['message'] = message
    session['message_type'] = message_type
    session['current_view'] = 'menu'  # Return to menu after action
    return redirect(url_for('index'))

@app.route('/back_to_menu')
def back_to_menu():
    session['current_view'] = 'menu'
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
