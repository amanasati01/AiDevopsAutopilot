from datetime import datetime ,timedelta , timezone
import jwt
from app.core.config import settings
from fastapi import HTTPException,status


def create_access_token(user_id:str)->str:
    expire_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub" : user_id,
        "exp" : expire_at
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
def decode_access_token(token:str)->str:
    try:
         payload = jwt.decode(token,settings.jwt_secret_key,algorithms=settings.jwt_algorithm)
         userId = payload.get("sub")
         if userId is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
         return userId
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")
        
   
    
