from flask import Blueprint, render_template, request, jsonify
import hashlib

exp3_bp = Blueprint('exp3', __name__)

# In-memory storage for biometric templates (simulated)
# Format: { 'username': 'hash_of_face_data' }
BIOMETRIC_DB = {}

@exp3_bp.route('/')
def index():
    return render_template('exp3_bio.html')

@exp3_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    face_image = data.get('image') # Base64 string
    
    if not username or not face_image:
        return jsonify({'success': False, 'message': 'Missing data'})
        
    # Simulate feature extraction by hashing the image data
    # In reality, this would be a vector of facial features
    feature_hash = hashlib.sha256(face_image.encode()).hexdigest()
    BIOMETRIC_DB[username] = feature_hash
    
    return jsonify({'success': True, 'message': 'Biometric data registered'})

@exp3_bp.route('/api/verify', methods=['POST'])
def verify():
    data = request.get_json()
    username = data.get('username')
    face_image = data.get('image')
    
    if username not in BIOMETRIC_DB:
        return jsonify({'success': False, 'message': 'User not found'})
        
    # Verify against stored hash
    incoming_hash = hashlib.sha256(face_image.encode()).hexdigest()
    stored_hash = BIOMETRIC_DB[username]
    
    # In this simple simulation, we require an exact match (which implies the exact same image file)
    # This perfectly sets up Exp 4 (Replay Attack)
    if incoming_hash == stored_hash:
        return jsonify({'success': True, 'message': 'Identity Verified'})
    else:
        return jsonify({'success': False, 'message': 'Biometric Mismatch'})
