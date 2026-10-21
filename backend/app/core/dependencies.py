from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Validate JWT token for protected API endpoints.
    Used for UK university project submission — ALL ENGLISH.
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Please log in first",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload