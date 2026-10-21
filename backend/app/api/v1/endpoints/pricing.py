from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.schemas.common import APIResponse
from app.core.config import settings
from app.core.dependencies import verify_token
from app.utils.logger import logger
import json, os

router = APIRouter()

PRICING_FILE = os.path.join(os.path.dirname(__file__), "../../../../pricing_config.json")

class PricingConfig(BaseModel):
    free_hours: float = Field(..., ge=0, le=24, description="Free parking hours")
    hourly_rate: float = Field(..., ge=0.5, le=50, description="Hourly parking fee in GBP")

def _load_pricing() -> dict:
    if os.path.exists(PRICING_FILE):
        with open(PRICING_FILE, "r") as f:
            return json.load(f)
    return {
        "free_hours": settings.FREE_PARKING_HOURS,
        "hourly_rate": settings.HOURLY_PARKING_FEE,
    }

def _save_pricing(data: dict):
    with open(PRICING_FILE, "w") as f:
        json.dump(data, f)

def get_current_pricing() -> dict:
    return _load_pricing()

@router.get("/config", response_model=APIResponse, summary="Get Current Pricing Config")
async def get_pricing(token_data: dict = Depends(verify_token)):
    pricing = _load_pricing()
    return APIResponse(code=200, message="Pricing config retrieved", data=pricing)

@router.put("/config", response_model=APIResponse, summary="Update Pricing Config")
async def update_pricing(
    config: PricingConfig,
    token_data: dict = Depends(verify_token)
):
    data = {"free_hours": config.free_hours, "hourly_rate": config.hourly_rate}
    _save_pricing(data)
    logger.info(f"Pricing updated: free_hours={config.free_hours}, hourly_rate={config.hourly_rate}")
    return APIResponse(code=200, message="Pricing config updated successfully", data=data)
