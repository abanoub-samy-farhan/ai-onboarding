from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import cross_origin
from front_txt_extraction.gemini_ocr_v2 import FrontIDExtractor


from app.models.users import User
from app.models.tokens import Token
from app.extensions import db

from app.utils.EmailRouter import EmailRouter
from app.utils.FaceRecognition import FaceVerifier

import uuid
import os
import json

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
        return make_response(jsonify({'error': 'email is not found'}), 404)
    if not Bcrypt().check_password_hash(user.hashed_password, data['password']):
        return make_response(jsonify({'error': 'Incorrect password'}), 401)
    
    access_token_cookie = create_access_token(identity=user.id)
    response = make_response(jsonify({'access_token_cookie': access_token_cookie}), 200)
    set_access_cookies(response, access_token_cookie)
    return response


@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Successfully logged out'}), 200)
    unset_jwt_cookies(response)
    return response


@auth_bp.route('/generate/otp', methods=['GET'])
@jwt_required()
def generate_otp():
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)
    
    email_router = EmailRouter(user.email)
    generated_otp = int(email_router.send_otp(user))
    if not generated_otp:
        return make_response(jsonify({'error': 'Failed to generate OTP'}), 500)
    
    token = Token(user_id=user_id, token=generated_otp)
    print(token.user_id, token.token)
    db.session.add(token)
    db.session.commit()
    return make_response(jsonify({'message': 'OTP sent successfully'}), 200)


@auth_bp.route('/verify/email', methods=['POST'])
@jwt_required()
def verify_email():
    try:
        user_id = get_jwt_identity()
    except Exception:
        return make_response(jsonify({'error': 'Invalid token'}), 401)

    otp = int(request.json.get('otp'))
    if not otp:
        return make_response(jsonify({'error': 'OTP is required'}), 400)

    token = Token.query.filter_by(user_id=user_id, token=otp).first()
    user = User.query.get(user_id)

    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    if not token:
        return make_response(jsonify({'error': 'Invalid OTP'}), 400)

    # Delete the token after successful verification
    user.email_verified = True
    db.session.commit()

    # Send verification confirmation email
    email_router = EmailRouter(user.email)
    email_router.send_verification_confirmation(user)  # Fixed method name

    return make_response(jsonify({'message': 'Email verified successfully'}), 200)


@auth_bp.route('/verify/identity', methods=['POST'])
@jwt_required()
def verify_identity():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)
    if not request.files['identity_card_photo'] or not request.files['identity_card_video']:
        return make_response(jsonify({'error': 'Please provide both photo and video'}), 400)
    
    identity_card_photo = request.files['identity_card_photo']
    identity_card_video = request.files['identity_card_video']
    # if the file of the upload not created, create it
    if not os.path.exists(os.environ.get('UPLOAD_FOLDER')):
        os.makedirs(os.environ.get('UPLOAD_FOLDER'))

    identity_card_photo_uri = os.environ.get('UPLOAD_FOLDER') + f'/{user_id}-photo.{identity_card_photo.filename.split(".")[-1]}'
    identity_card_video_uri = os.environ.get('UPLOAD_FOLDER') + f'/{user_id}-video.{identity_card_video.filename.split(".")[-1]}'

    identity_card_photo.save(os.path.join(os.environ.get('UPLOAD_FOLDER'), f'{user_id}-photo.{identity_card_photo.filename.split(".")[-1]}'))
    identity_card_video.save(os.path.join(os.environ.get('UPLOAD_FOLDER'), f'{user_id}-video.{identity_card_video.filename.split(".")[-1]}'))
    front_id_extractor = FrontIDExtractor()
    # Extracted data of the ID
    
    extracted_data = front_id_extractor.run(identity_card_photo_uri)[0]
    print(extracted_data)
    
    
    # Verify the video matching with the photo
    face_reco = FaceVerifier(identity_card_photo_uri)
    recogntion_result = face_reco.verify_video(identity_card_video_uri)
    if not recogntion_result:
        return make_response(jsonify({'error': 'Identity verification failed'}), 400)
    
    user.identity_verified = True
    db.session.commit()
    return make_response(jsonify({**extracted_data}), 200)