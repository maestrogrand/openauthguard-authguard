from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.dependencies import get_current_user
from src.utils.http_client import fetch_user
from src.core.config import settings  # Import the missing `settings`

router = APIRouter(tags=["Microservice Integration"])


@router.get("/user/details")
async def get_user_details(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Retrieve user details by validating the token.
    """
    user_info = await fetch_user(current_user["sub"], settings.users_service_url)
    return {
        "user_id": current_user["user_id"],
        "username": current_user["sub"],
        "role": current_user["role"],
        "details": user_info,
    }
