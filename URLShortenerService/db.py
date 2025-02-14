from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class URLMapping(db.Model):
    """Database model for storing URL mappings per user."""
    id = db.Column(db.Integer, primary_key=True)
    short_id = db.Column(db.String(2083), unique=True, nullable=False)
    full_url = db.Column(db.String(2083), nullable=False)
    username = db.Column(db.String(150), nullable=False)  # Store the username

    def __init__(self, short_id, full_url, username):
        self.short_id = short_id
        self.full_url = full_url
        self.username = username
