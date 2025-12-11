from flask import Blueprint, render_template, request, jsonify, session
import secrets
import base64
import json

import os

exp7_bp = Blueprint('exp7', __name__)

# Path to the JSON database file
DB_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users):
    with open(DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)

CHALLENGES = {} # To store challenges for verification

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def base64url_decode(data):
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

@exp7_bp.route('/')
def index():
    return render_template('exp7_webauthn.html')

# 1. Password Registration
@exp7_bp.route('/register_password', methods=['POST'])
def register_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'})
    
    users = load_users()
    if username in users:
        return jsonify({'success': False, 'message': 'User already exists'})
        
    users[username] = {
        'password': password, # In real app, hash this!
        'credentials': []
    }
    save_users(users)
    return jsonify({'success': True, 'message': 'User registered with password'})

# 2. Password Login
@exp7_bp.route('/login_password', methods=['POST'])
def login_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    users = load_users()
    user = users.get(username)
    if user and user['password'] == password:
        # Check if user has registered WebAuthn credentials
        if user.get('credentials') and len(user['credentials']) > 0:
            session['pre_2fa_user'] = username
            return jsonify({'success': True, 'required_2fa': True, 'message': 'Password correct. 2FA required.'})
        else:
            session['user'] = username
            return jsonify({'success': True, 'required_2fa': False, 'message': 'Logged in with password'})
    
    return jsonify({'success': False, 'message': 'Invalid credentials'})

# 3. WebAuthn Registration (Attestation) - Step 1: Get Options
@exp7_bp.route('/webauthn/register/options', methods=['POST'])
def webauthn_register_options():
    username = session.get('user')
    if not username:
        return jsonify({'success': False, 'message': 'Not logged in'})
        
    # Generate a random challenge
    challenge = secrets.token_bytes(32)
    challenge_b64 = base64url_encode(challenge)
    
    # Store challenge
    CHALLENGES[username] = challenge_b64
    
    # Determine RP ID from request
    rp_id = request.host.split(':')[0]
    
    # Return options
    return jsonify({
        'success': True,
        'challenge': challenge_b64,
        'user': {
            'id': base64url_encode(username.encode()),
            'name': username,
            'displayName': username
        },
        'rp': {
            'name': 'Security Lab',
            # 'id': rp_id  <-- Omitted to allow browser to use current effective domain
        },
        'pubKeyCredParams': [
            {'type': 'public-key', 'alg': -7}, # ES256
            {'type': 'public-key', 'alg': -257}, # RS256
        ],
        'timeout': 60000,
        'attestation': 'none'
    })

# 3. WebAuthn Registration - Step 2: Complete
@exp7_bp.route('/webauthn/register/complete', methods=['POST'])
def webauthn_register_complete():
    username = session.get('user')
    if not username:
        return jsonify({'success': False, 'message': 'Not logged in'})
        
    data = request.get_json()
    credential_id = data.get('id')
    client_data_json = data.get('clientDataJSON')
    attestation_object = data.get('attestationObject')
    
    # Verification Logic (Simplified for Lab - No backend crypto lib dependency)
    # real implementation would parse CBOR and verify signature
    
    if not credential_id:
         return jsonify({'success': False, 'message': 'Missing credential ID'})
         
    # Store the credential ID
    users = load_users()
    if username in users:
        users[username]['credentials'].append({
            'id': credential_id,
            'rawId': credential_id # In real app store public key
        })
        save_users(users)
        return jsonify({'success': True, 'message': 'Authenticator registered successfully'})
    else:
        return jsonify({'success': False, 'message': 'User record error'})

# 4. WebAuthn Login (Assertion) - Step 1: Get Options
@exp7_bp.route('/webauthn/login/options', methods=['POST'])
def webauthn_login_options():
    # In 2FA flow, we know the user from the previous password step
    username = session.get('pre_2fa_user')
    
    users = load_users()
    if not username or username not in users:
        return jsonify({'success': False, 'message': 'Session expired or invalid user'})

    challenge = secrets.token_bytes(32)
    challenge_b64 = base64url_encode(challenge)
    CHALLENGES[username] = challenge_b64 # Store challenge associated with username attempt
    
    # Get user's registered credentials
    allow_credentials = []
    for cred in users[username]['credentials']:
        allow_credentials.append({
            'type': 'public-key',
            'id': cred['id']
        })
        
    return jsonify({
        'success': True,
        'challenge': challenge_b64,
        'allowCredentials': allow_credentials,
        'timeout': 60000,
        'userVerification': 'preferred'
    })

# 4. WebAuthn Login - Step 2: Complete
@exp7_bp.route('/webauthn/login/complete', methods=['POST'])
def webauthn_login_complete():
    username = session.get('pre_2fa_user')
    if not username:
        return jsonify({'success': False, 'message': 'Session expired'})
        
    data = request.get_json()
    credential_id = data.get('id')
    
    # Simplified Verification: Check if credential ID belongs to user
    users = load_users()
    user = users.get(username)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})
        
    valid_cred = False
    for cred in user['credentials']:
        if cred['id'] == credential_id:
            valid_cred = True
            break
            
    if valid_cred:
        session['user'] = username
        session.pop('pre_2fa_user', None) # Clear temp session
        return jsonify({'success': True, 'message': '2FA Verification Successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid credential'})

@exp7_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'success': True, 'message': 'Logged out'})

@exp7_bp.route('/status')
def status():
    return jsonify({'user': session.get('user')})
