from flask import Blueprint, render_template

exp4_bp = Blueprint('exp4', __name__)

@exp4_bp.route('/')
def index():
    return render_template('exp4_bio_attack.html')
