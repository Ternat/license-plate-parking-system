from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    """Request model for user login (English fields)"""
    username: str
    password: str

class UserResponse(BaseModel):
    """Response model for user (English fields)"""
    id: int
    username: str
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    """Response model for JWT token (English fields)"""
    access_token: str
    token_type: str = "bearer"