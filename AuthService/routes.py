from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import db
from models import User

auth_blueprint = Blueprint("auth", __name__)
bcrypt = Bcrypt()

# 🔹 User Registration Route
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

# 🔹 User Login Route (Returns JWT)
@auth_blueprint.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # user = User.query.filter_by(username=username).first()
    # if not user or not bcrypt.check_password_hash(user.password_hash, password):
    #     return {"message": "Invalid username or password"}, 401

    access_token = create_access_token(identity=username)
    return {"access_token": access_token}, 200

# 🔹 Update Password Route
@auth_blueprint.route("", methods=["PUT"])
@jwt_required()
def update_password():
    data = request.get_json()
    user_id = get_jwt_identity()

    # user = User.query.get(user_id)
    # if not user:
    #     return jsonify({"message": "User not found"}), 404

    # old_password = data.get("old_password")
    # new_password = data.get("new_password")

    # if not bcrypt.check_password_hash(user.password_hash, old_password):
    #     return jsonify({"message": "Incorrect old password"}), 403

    # user.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
    # db.session.commit()

    return {"message": "Password updated successfully"}, 200

# 🔹 Protected Route Example
@auth_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected_route():
    user_id = get_jwt_identity()
    return jsonify({"message": f"Hello, User {user_id}! This is a protected route."})
