import base64
import json
import hmac
import hashlib
from datetime import datetime, timedelta
from config import Config

def base64url_encode(input_bytes: bytes) -> str:
    """Encodes bytes into a base64 URL-safe string (without padding)"""
    return base64.urlsafe_b64encode(input_bytes).decode('utf-8').replace('=', '')

def base64url_decode(input_str: str) -> bytes:
    """Decodes a base64 URL-safe string back into bytes"""
    padding_needed = 4 - (len(input_str) % 4)
    input_str += "=" * padding_needed  # Fix padding
    return base64.urlsafe_b64decode(input_str)

def create_jwt(username: str, expiry_minutes: int = 60) -> str:
    """Manually creates a JWT (header.payload.signature)"""
    
    header = {"typ": "JWT", "alg": "HS256"}
    payload = {
        "sub": username,
        "exp": int((datetime.now() + timedelta(minutes=expiry_minutes)).timestamp())
    }

    # Encode header and payload
    encoded_header = base64url_encode(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = base64url_encode(json.dumps(payload, separators=(",", ":")).encode())

    # Create the signature
    signing_input = f"{encoded_header}.{encoded_payload}".encode()
    signature = hmac.new(Config.JWT_SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
    encoded_signature = base64url_encode(signature)

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

def validate_jwt(token: str) -> str:
    """Manually validates JWT and returns the username if valid, otherwise None"""
    try:
        segments = token.split(".")
        if len(segments) != 3:
            return None  # Invalid JWT format

        # Decode header and payload
        decoded_header = json.loads(base64url_decode(segments[0]).decode())
        decoded_payload = json.loads(base64url_decode(segments[1]).decode())

        # Verify algorithm
        if decoded_header.get("alg") != "HS256":
            return None  # Invalid algorithm

        # Verify expiration
        if decoded_payload["exp"] < int(datetime.now().timestamp()):
            return None  # Token expired

        # Recreate signature to verify integrity
        signing_input = f"{segments[0]}.{segments[1]}".encode()
        expected_signature = hmac.new(Config.JWT_SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
        expected_signature_encoded = base64url_encode(expected_signature)

        if expected_signature_encoded != segments[2]:
            return None  # Signature mismatch

        return decoded_payload["sub"]  # Return username if valid

    except Exception as e:
        print("JWT validation error:", e)
        return None  # Invalid JWT
