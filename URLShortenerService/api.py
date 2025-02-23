from flask import Flask, request, redirect
from flask_restful import Resource, Api
from url_shortener import URLShortener
import config, os
from db import db, URLMapping  # Import database setup & model
from cache import cache  # Import Redis client
import requests
app = Flask(__name__)
app.config.from_object(config)  # Load database configuration

db.init_app(app)  # Initialize database with Flask app
api = Api(app)

with app.app_context():
    db.create_all()  # Create tables if they don’t exist

# Initialize URLShortenerService
shortener_service = URLShortener()


# Get the auth service URL from environment variables
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:5001/users/validate")

def validate_jwt(token):
    """Send JWT to the Auth Service for validation"""

    response = requests.post(AUTH_SERVICE_URL, json={"access_token": token})
    
    if response.status_code == 200 and response.json().get("valid"):
        return response.json().get("identity")  # Return username from token
    
    return None  # Invalid token

def extract_jwt():
    """Extract JWT token from Authorization header"""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]  # Extract token after "Bearer"
    elif auth_header:
        return auth_header
    return None

class URLResource(Resource):
    def get(self, url_id):
        # We cannot use cache anymore
        # full_url = cache.get(url_id)
        # if full_url:
        #     print("Cache hit!")
        #     cache.expire(url_id, 86400)
        #     return {"value": full_url}, 301 #cache hit
        
        # print(f"Cache miss, querying PostgreSQL...")
        """Retrieve long URL from short ID"""
        token = extract_jwt()
        username = validate_jwt(token)  # Validate JWT locally
        if not username:
            return {"message": "Forbidden"}, 403  # Invalid token
        
        url_mapping = URLMapping.query.filter_by(short_id=url_id, username=username).first()
        if url_mapping:
            return {"value": url_mapping.full_url}, 301  # Redirect to original URL
        return {"error": "Short URL not found"}, 404

    def put(self, url_id):
        # First validate the token
        token = extract_jwt()
        username = validate_jwt(token)
        if not username:
            return {"message": "Forbidden"}, 403  #Return 403 if token is invalid
        
        """Update an existing short URL mapping"""
        url_mapping = URLMapping.query.filter_by(short_id=url_id, username=username).first()
        if not url_mapping:
            return {"error": "Short URL not found"}, 404

        data = request.get_json(force=True)
        new_url = data.get("url")
        
        if not new_url or not shortener_service.validate_url(new_url):
            return {"error": "Invalid URL format"}, 400

        url_mapping.full_url = new_url
        db.session.commit()
        #cache.setex(url_id, 86400, new_url) #update cache

        return {"message": "URL updated successfully"}, 200

    def delete(self, url_id):
        # First validate the token
        token = extract_jwt()
        username = validate_jwt(token)
        if not username:
            return {"message": "Forbidden"}, 403  #Return 403 if token is invalid
        
        """Delete a short URL mapping"""
        url_mapping = URLMapping.query.filter_by(short_id=url_id, username=username).first()
        if url_mapping:
            db.session.delete(url_mapping)
            db.session.commit()
            #cache.delete(url_id)
            return '',204
        return {"error": "Short URL not found"}, 404

class URLCreationResource(Resource):

    def post(self):
        # First validate the token
        token = extract_jwt()
        username = validate_jwt(token)
        if not username:
            return {"message": "Forbidden"}, 403  #Return 403 if token is invalid
        
        """Create a new short URL"""
        data = request.get_json()
        long_url = data.get("value")
        if not long_url or not shortener_service.validate_url(long_url):
            return {"error": "Invalid URL format"},400

        # Generate a unique short ID and handle db operations.
        short_id = shortener_service.shorten_url(long_url,username)

        #cache.setex(short_id, 86400, long_url) #cache for 24 hrs

        return {"id": short_id}, 201

class URLListResource(Resource):
    def get(self):
        # First validate the token
        token = extract_jwt()
        username = validate_jwt(token)
        if not username:
            return {"message": "Forbidden"}, 403  #Return 403 if token is invalid
        
        """List all Short ID and Long URL pairs"""
        url_mappings = URLMapping.query.filter_by(username=username).all()
        result = [{"short_id": url.short_id, "long_url": url.full_url} for url in url_mappings]
        return {"url_mapping": result}, 200

    def delete(self):
        # First validate the token
        token = extract_jwt()
        username = validate_jwt(token)
        if not username:
            return {"message": "Forbidden"}, 403  #Return 403 if token is invalid
        
        """Prevent bulk deletion (returns 404)"""
        return {"error": "Bulk deletion is not allowed"},404

api.add_resource(URLResource, "/<string:url_id>")  
api.add_resource(URLCreationResource, "/")  
api.add_resource(URLListResource,"/")
