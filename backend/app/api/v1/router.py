from fastapi import APIRouter
from app.api.v1.endpoints import recognition, parking, records, auth, pricing

# Create main API router
api_router = APIRouter()

#sub-routers
api_router.include_router(
    recognition.router,
    prefix="/recognition",
    tags=["License Plate Recognition"]
)
api_router.include_router(
    parking.router,
    prefix="/parking",
    tags=["Parking Operations"]
)
api_router.include_router(
    records.router,
    prefix="/records",
    tags=["Parking Records"]
)
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)
api_router.include_router(
    pricing.router,
    prefix="/pricing",
    tags=["Pricing Configuration"]
)