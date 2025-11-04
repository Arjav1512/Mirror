"""
JWT Authentication System for Mirror
Enables seamless session transfer between Landing Page and Streamlit App
"""

import jwt
import datetime
from typing import Optional, Dict
import os

# Secret key for JWT - CHANGE THIS IN PRODUCTION
JWT_SECRET = os.getenv('JWT_SECRET', 'mirror-secret-key-change-in-production-2024')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

def generate_auth_token(user_id: int, email: str, name: str) -> str:
    """
    Generate JWT token for user authentication
    
    Args:
        user_id: User's database ID
        email: User's email
        name: User's full name
    
    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'name': name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_auth_token(token: str) -> Optional[Dict]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        Dict with user data if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {
            'user_id': payload['user_id'],
            'email': payload['email'],
            'name': payload['name']
        }
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


def create_streamlit_url(base_url: str, token: str) -> str:
    """
    Create Streamlit URL with auth token
    
    Args:
        base_url: Base Streamlit URL (e.g., 'http://localhost:8501')
        token: JWT authentication token
    
    Returns:
        Full URL with token parameter
    """
    return f"{base_url}?auth_token={token}"
