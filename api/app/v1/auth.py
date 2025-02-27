from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

from app.models.users import User
from app.models.tokens import Token
from app.extensions import db

from app.utils.EmailRouter import EmailRouter

import uuid

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    data['id'] = str(uuid.uuid4())
    if data['password'] != data['confirm-password']:
        return make_response(jsonify({'error': 'Passwords do not match'}), 400)
    data['hashed_password'] = Bcrypt().generate_password_hash(data['password']).decode('utf-8')
    data.pop('password')
    data.pop('confirm-password')
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify(user.to_dict()), 201)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)
    if not Bcrypt().check_password_hash(user.hashed_password, data['password']):
        return make_response(jsonify({'error': 'Incorrect password'}), 401)
    
    access_token = create_access_token(identity=user.id)
    response = make_response(jsonify({'access_token': access_token}), 200)
    set_access_cookies(response, access_token)
    return response

@auth_bp.route('/test', methods=['GET'])
@jwt_required()
def testing():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return make_response(jsonify({'message': user.to_dict()}), 200)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Successfully logged out'}), 200)
    unset_jwt_cookies(response)
    return response

@auth_bp.route('/gnereate/otp', methods=['POST'])
@jwt_required()
def generate_otp():
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        return make_response(jsonify({'error': 'Invalid token'}), 401)
    
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)
    
    email_router = EmailRouter(user.email)
    generated_otp = email_router.send_otp(user)
    if not generated_otp:
        return make_response(jsonify({'error': 'Failed to generate OTP'}), 500)
    
    db.session.add(Token(user_id=user_id, otp=generated_otp))
    db.session.commit()
    return make_response(jsonify({'message': 'OTP sent successfully'}), 200)

@auth_bp.route('/verify/email?<int:otp>', methods=['POST'])
@jwt_required()
def verify_email(otp):
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        return make_response(jsonify({'error': 'Invalid token'}), 401)
    token = Token.query.filter_by(user_id=user_id, token=otp).first()
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)
    if not token:
        return make_response(jsonify({'error': 'Invalid OTP'}), 400)
    token.delete()
    user.email_verified = True
    db.session.commit()
    email_router = EmailRouter(user.email)
    email_router.send_verfication_confirmation(user)
    return make_response(jsonify({'message': 'Email verified successfully'}), 200)