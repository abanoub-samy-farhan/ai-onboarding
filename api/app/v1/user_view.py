from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from app.models.users import User
from app.extensions import db

import uuid

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/v1/user')


@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)
    return make_response(jsonify(user.to_dict()), 200)

@user_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
def get_user_by_id(id):
    user = User.query.get(id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)
    return make_response(jsonify(user.to_dict()), 200)

@user_bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    data['id'] = str(uuid.uuid4())
    print(data)
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify(data), 201)

@user_bp.route('/<string:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get(id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)
    data = request.get_json()
    user.update(data)
    db.session.commit()
    return make_response(jsonify(user), 200)

@user_bp.route('/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify(user.to_dict()), 204)