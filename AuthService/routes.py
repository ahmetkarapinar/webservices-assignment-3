from flask import Blueprint, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
from db import db
from models import User

auth_blueprint = Blueprint("auth", __name__)
bcrypt = Bcrypt()

# User Registration Route
@auth_blueprint.route("", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"message": "Username and password are required"}, 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {"message": "User already exists"}, 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, password_hash=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201

# User Login Route (Returns JWT)
@auth_blueprint.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return {"message": "Invalid username or password"}, 401

    access_token = create_access_token(identity=str(username))
    return {"token": access_token}, 200

# Update Password Route
@auth_blueprint.route("", methods=["PUT"])
def update_password():
    data = request.get_json()
    username = data.get("username")

    user = User.query.filter_by(username=username).first()
    if not user:
        return {"message": "User not found"}, 404

    old_password = data.get("old-password")
    new_password = data.get("new-password")

    if not bcrypt.check_password_hash(user.password_hash, old_password):
        return {"message": "Incorrect old password"}, 403

    user.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
    db.session.commit()

    return {"message": "Password updated successfully"}, 200

# Protected Route Example
@auth_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected_route():
    username = get_jwt_identity()
    return {"message": f"Hello, User {username}! This is a protected route."}

@auth_blueprint.route("/validate", methods=["POST"])
def validate_jwt():
    """Validate JWT sent by URL Shortener Service"""
    data = request.get_json()
    token = data.get("access_token")

    if not token:
        return {"message": "Missing access token"}, 400

    try:
        decoded_token = decode_token(token)  # Flask-JWT-Extended built-in function
        return {"valid": True, "identity": decoded_token["sub"]}, 200  # `sub` contains the identity
    except Exception as e:
        return {"valid": False, "error": str(e)}, 403