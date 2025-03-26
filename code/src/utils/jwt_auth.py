from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JWTAuth:
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY')
        if not self.secret_key:
            raise ValueError("JWT_SECRET_KEY must be set in environment variables")
        
        self.algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
        self.access_token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    
    def create_access_token(self, data: Dict) -> str:
        """Create a new JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode a JWT token."""
        try:
            decoded_token = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return decoded_token
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None
    
    def refresh_token(self, token: str) -> Optional[str]:
        """Refresh an existing token if it's still valid."""
        decoded = self.verify_token(token)
        if decoded:
            # Create new token with updated expiration
            new_token = self.create_access_token({
                "sub": decoded.get("sub"),
                "role": decoded.get("role")
            })
            return new_token
        return None 