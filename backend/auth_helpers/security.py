from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from .config import settings


# use sha256_crypt for hashing the user password for security purpose
password_hasher = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def hash_user_password(plain_password):
    """Hash a password using bcrypt_sha256 to handles long input password"""
    return password_hasher.hash(plain_password)

def check_password_match(plain_password, hashed_password):
    """check if readable input password matches hashed password"""
    return password_hasher.verify(plain_password, hashed_password)

def generate_jwt_token(user_email):
    """generate JWT token for a user"""
    expiration_time = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token_data = {
        "sub": user_email,
        "exp": expiration_time
    }
    
    token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt_token(token):
    """Decode and verify JWT token"""
    try:
        decoded_data = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return decoded_data
    except:
        return None
    
    