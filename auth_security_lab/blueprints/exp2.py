from flask import Blueprint, render_template, jsonify

exp2_bp = Blueprint('exp2', __name__)

@exp2_bp.route('/')
def index():
    return render_template('exp2_attack.html')

@exp2_bp.route('/api/dictionary')
def get_dictionary():
    # A small dictionary for the attack simulation
    return jsonify({
        'passwords': [
            '123456', 'password', 'admin', 'welcome', 'login', 
            'qwerty', '111111', 'sunshine', 'wonderland', 'builder', 'password123'
        ]
    })
