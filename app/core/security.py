from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
bearer_scheme = HTTPBearer()

def create_access_token(data: dict, expires_delta: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        payload = jwt.decode(token.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        file_id: str = payload.get("sub")
        if file_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return file_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)