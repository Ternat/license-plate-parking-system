from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Union, Dict, Any

class APIException(Exception):
    """Custom API Exception for standardized error responses"""
    def __init__(self, status_code: int, message: str, data: Any = None):
        self.status_code = status_code
        self.message = message
        self.data = data

class PlateDetectionError(Exception):
    """Raised when no license plate is detected in the image"""
    def __init__(self, message: str = "No license plate detected in the image"):
        self.message = message
        super().__init__(self.message)

async def api_exception_handler(request: Request, exc: APIException):
    """Global exception handler for APIException"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.message,
            "data": exc.data
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Global handler for unexpected exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal server error",
            "data": None
        }
    )