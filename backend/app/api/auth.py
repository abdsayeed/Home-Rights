from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

bp = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    return True, "Valid"

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    
    if not all([email, password, first_name, last_name]):
        return jsonify({'error': 'All fields are required'}), 400
    
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    is_valid, message = validate_password(password)
    if not is_valid:
        return jsonify({'error': message}), 400
    
    db = current_app.db
    
    if db.users.find_one({'email': email}):
        return jsonify({'error': 'Email already registered'}), 400
    
    user = {
        'email': email,
        'passwordHash': generate_password_hash(password),
        'role': 'user',
        'profile': {
            'firstName': first_name,
            'lastName': last_name
        },
        'savedItems': [],
        'createdAt': datetime.utcnow(),
        'lastLogin': None
    }
    
    result = db.users.insert_one(user)
    user_id = str(result.inserted_id)
    
    # Use configured token expiration from app config
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user_id,
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'role': 'user'
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    db = current_app.db
    user = db.users.find_one({'email': email})
    
    if not user or not check_password_hash(user['passwordHash'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    db.users.update_one(
        {'_id': user['_id']},
        {'$set': {'lastLogin': datetime.utcnow()}}
    )
    
    user_id = str(user['_id'])
    # Use configured token expiration from app config
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user_id,
            'email': user['email'],
            'firstName': user['profile']['firstName'],
            'lastName': user['profile']['lastName'],
            'role': user['role']
        }
    }), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    db = current_app.db
    
    from bson import ObjectId
    user = db.users.find_one({'_id': ObjectId(user_id)})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': str(user['_id']),
        'email': user['email'],
        'firstName': user['profile']['firstName'],
        'lastName': user['profile']['lastName'],
        'role': user['role']
    }), 200
