from flask import Blueprint, render_template, request, jsonify
import ssl
import socket

exp5_bp = Blueprint('exp5', __name__)

@exp5_bp.route('/')
def index():
    return render_template('exp5_ssl.html')

@exp5_bp.route('/api/handshake')
def handshake_sim():
    # Simulate the steps of an SSL handshake
    steps = [
        {'step': 1, 'actor': 'Client', 'action': 'ClientHello', 'details': 'Cipher Suites: TLS_AES_256_GCM_SHA384, Random: 0x8F3...'},
        {'step': 2, 'actor': 'Server', 'action': 'ServerHello', 'details': 'Selected Cipher: TLS_AES_256_GCM_SHA384, Session ID: 0x1A2...'},
        {'step': 3, 'actor': 'Server', 'action': 'Certificate', 'details': 'CN=localhost, Issuer=SelfSigned'},
        {'step': 4, 'actor': 'Server', 'action': 'ServerKeyExchange', 'details': 'Curve: X25519, PubKey: 0x99A...'},
        {'step': 5, 'actor': 'Client', 'action': 'ClientKeyExchange', 'details': 'PubKey: 0xBB2...'},
        {'step': 6, 'actor': 'Client', 'action': 'ChangeCipherSpec', 'details': 'Switching to Encrypted Mode'},
        {'step': 7, 'actor': 'Server', 'action': 'Finished', 'details': 'Handshake Complete'}
    ]
    return jsonify(steps)
