from flask import Blueprint, render_template, jsonify

exp6_bp = Blueprint('exp6', __name__)

@exp6_bp.route('/')
def index():
    return render_template('exp6_ssl_attack.html')

@exp6_bp.route('/api/mitm_handshake')
def mitm_sim():
    # Simulate a MITM attack (SSL Strip / Downgrade)
    steps = [
        {'step': 1, 'actor': 'Client', 'action': 'ClientHello', 'details': 'Cipher Suites: TLS_AES_256_GCM_SHA384...'},
        {'step': 2, 'actor': 'Attacker', 'action': 'Intercept', 'details': 'Intercepted ClientHello. Modifying Cipher Suites...'},
        {'step': 3, 'actor': 'Attacker (to Server)', 'action': 'ClientHello (Modified)', 'details': 'Cipher Suites: NULL, EXPORT_RSA... (Weak Ciphers)'},
        {'step': 4, 'actor': 'Server', 'action': 'ServerHello', 'details': 'Selected Cipher: EXPORT_RSA (Weak)'},
        {'step': 5, 'actor': 'Attacker', 'action': 'Relay', 'details': 'Relaying Weak Cipher to Client'},
        {'step': 6, 'actor': 'System', 'action': 'Alert', 'details': 'VULNERABILITY EXPLOITED: Weak Encryption Negotiated'}
    ]
    return jsonify(steps)
