from flask import Flask
import string
import random
import hashlib
import validators
from db import db, URLMapping
app = Flask(__name__)

BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase

class URLShortener:

    def encode_base62(self, num):
        if num == 0:
            return BASE62_ALPHABET[0]
        
        base62 = ""
        while num > 0:
            num, remainder = divmod(num, 62)
            base62 = BASE62_ALPHABET[remainder] + base62
        
        return base62

    def decode_base62(self, base62):
        num = 0
        for index, char in enumerate(reversed(base62)):
            num += BASE62_ALPHABET.index(char) * (62 ** index)
        
        return num
    
    def shorten_url(self, long_url, username):
        """Shorten a URL and store it in the database."""
        existing_entry = URLMapping.query.filter_by(full_url=long_url, username=username).first()
        if existing_entry:
            return existing_entry.short_id

        # Generate a hash for the URL
        hash_digest = hashlib.sha256(long_url.encode()).hexdigest()
        short_code = self.encode_base62(int(hash_digest, 16))[:6]
        print("Short code: ",short_code)

        # Ensure uniqueness
        attempt = 0
        while URLMapping.query.filter_by(short_id=short_code, username=username).first():
            attempt += 1
            print(f"Collision detected! Attempt {attempt} generating new short code...")
            # Generate a random salt (5-character alphanumeric string)
            salt = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            salted_hash = hashlib.sha256((long_url + salt).encode()).hexdigest()
            short_code = self.encode_base62(int(salted_hash, 16))[:6]

        # Store in database
        new_entry = URLMapping(short_id=short_code, full_url=long_url, username=username)
        db.session.add(new_entry)
        db.session.commit()

        return short_code
      
    def validate_url(self, full_url):
        """Validate the URL using the `validators` library."""
        return validators.url(full_url)  