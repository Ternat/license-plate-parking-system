from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from app.schemas.common import APIResponse
from app.schemas.user import UserLogin, Token
from app.core.security import create_access_token
from app.core.config import settings
from app.core.dependencies import verify_token

router = APIRouter()

@router.post("/login", response_model=APIResponse, summary="Admin Login")
async def login(login_data: UserLogin):
    if login_data.username != settings.ADMIN_USERNAME or login_data.password != settings.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": login_data.username}, expires_delta=access_token_expires
    )

    return APIResponse(
        code=200,
        message="Login successful",
        data=Token(access_token=access_token, token_type="bearer")
    )

@router.post("/logout", response_model=APIResponse, summary="Admin Logout")
async def logout(token_data: dict = Depends(verify_token)):
    return APIResponse(
        code=200,
        message="Logout successful",
        data=None
    )