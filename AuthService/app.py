from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
from db import db
from routes import auth_blueprint

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database and Security Modules
db.init_app(app)
bcrypt = Bcrypt(app)

# Register Blueprints (Routes)
app.register_blueprint(auth_blueprint, url_prefix="/users")

# Create Tables
with app.app_context():
    db.create_all()

# Run Flask App on Port 5001
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)