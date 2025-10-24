from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.find_by_email(data['email']):
            return jsonify({'message': 'Email already exists'}), 400
        
        # Create new user
        User.create_user(data['username'], data['email'], data['password'])
        return jsonify({'message': 'User created successfully'}), 201
        
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing email or password'}), 400
        
        # Find user
        user = User.find_by_email(data['email'])
        
        if not user or not User.verify_password(user['password'], data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        # Create access token
        access_token = create_access_token(identity=str(user['_id']))
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500