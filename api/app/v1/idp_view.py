from flask import Blueprint, jsonify, request, make_response, redirect
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity


from app.models.clients import Client
from app.extensions import db

import uuid
import jwt


# Creating the blueprint for the identity provider

idp_bp = Blueprint('idp_bp', __name__, '/api/v1/oauth')


@idp_bp.route('/register', methods=['POST'])
def register_idp():
    client = Client(client_id=str(uuid.uuid4()), client_secret=str(uuid.uuid4()))
    db.session.add(client)
    db.session.commit()
    return make_response(jsonify(client.to_dict()), 201)

@idp_bp.route('/authorize?<client_id:string>&<client_secret:string>&<callback_uri:string>', methods=['POST'])
@jwt_required
def authorize_clients(client_id, client_secret, callback_uri):
    user_id = get_jwt_identity()
    approval = request.json.get('authorize')

    if not approval:
        return make_response({"msg": "Unauthorized"}, 401)
    
    access_token = jwt.encode(client_id, client_secret)
    response = make_response({"access_token": access_token}, 201)

    redirect(callback_uri, 302, response)


