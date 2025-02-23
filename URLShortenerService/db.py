from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class URLMapping(db.Model):
    """Database model for storing URL mappings per user with a composite primary key."""
    
    short_id = db.Column(db.String(2083), nullable=False)
    full_url = db.Column(db.String(2083), nullable=False)
    username = db.Column(db.String(150), nullable=False)  # Store the username
    
    # Define composite primary key
    __table_args__ = (
        db.PrimaryKeyConstraint('short_id', 'username'),  # Composite primary key
    )

    def __init__(self, short_id, full_url, username):
        self.short_id = short_id
        self.full_url = full_url
        self.username = username
