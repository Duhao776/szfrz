from flask import Blueprint, render_template, request, jsonify

exp1_bp = Blueprint('exp1', __name__)

# Simulated User Database
USERS = {
    'admin': 'password123',
    'alice': 'wonderland',
    'bob': 'builder'
}

@exp1_bp.route('/')
def index():
    return render_template('exp1_login.html')

@exp1_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in USERS and USERS[username] == password:
        return jsonify({'success': True, 'message': f'Welcome, {username}!'})
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
