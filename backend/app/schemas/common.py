from pydantic import BaseModel
from typing import Any, Optional

class APIResponse(BaseModel):
    """Standardized API response model (English fields)"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None