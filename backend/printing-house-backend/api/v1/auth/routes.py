from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from api.v1.auth.models import RegisterUser, LoginUser, UserResponse
from db.db import Session
from db.models import User

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = RegisterUser(**request.json)
    with Session() as session:
        existing_user = session.query(User).filter_by(email=data.email).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 400
        password_hash = generate_password_hash(data.password)
        new_user = User(
            email=data.email,
            password_hash=password_hash,
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone_number,
        )
        session.add(new_user)
        session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = LoginUser(**request.json)
    with Session() as session:
        user = session.query(User).filter_by(email=data.email).first()
    if not user or not check_password_hash(user.password_hash, data.password):
        return jsonify({"error": "Invalid credentials"}), 401
    access_token = create_access_token(identity=str(user.user_id))
    return UserResponse(email=user.email, access_token=access_token).model_dump_json()


@auth_blueprint.route("/status", methods=["GET"])
@jwt_required(optional=True)
def check_auth_status():
    identity = get_jwt_identity()
    if identity:
        return jsonify({"message": "User is authenticated"}), 200
    return jsonify({"message": "User is not authenticated"}), 401
