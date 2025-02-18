from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from jwt_handler import create_jwt, validate_jwt  
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
    """User login route that generates a manually signed JWT"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return {"message": "Invalid username or password"}, 401

    token = create_jwt(username, expiry_minutes=60)  # Generate JWT valid for 1 hour

    return jsonify({"token": token}), 200

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
def protected_route():
    """Manually validate JWT instead of using @jwt_required()"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")

    username = validate_jwt(token)  # Validate JWT manually
    if not username:
        return {"message": "Invalid or expired token"}, 403

    return {"message": f"Hello, User {username}! This is a protected route."}

@auth_blueprint.route("/validate", methods=["POST"])
def validate_token():
    """Validates JWT sent from other services"""
    data = request.get_json()
    token = data.get("access_token")

    if not token:
        return {"message": "Missing access token"}, 400

    username = validate_jwt(token)
    if not username:
        return {"message": "Invalid or expired token"}, 403

    return jsonify({"valid": True, "identity": username}), 200
