from fastapi import APIRouter, HTTPException
from src.auth.schemas import LoginRequest
from src.utils.helpers import verify_password, create_access_token
from src.utils.http_client import fetch_user
from src.core.config import settings
from src.core.logging import logger

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login_user(request: LoginRequest):
    """
    Endpoint to authenticate a user and generate a JWT token.
    """
    logger.info("Attempting to log in user: %s", request.username)

    user_data = await fetch_user(request.username, settings.users_service_url)
    logger.debug(f"Fetched user data: {user_data}")

    if not user_data or "password_hash" not in user_data:
        logger.warning(
            "Invalid user data or missing password hash for user: %s", request.username
        )
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(request.password, user_data["password_hash"]):
        logger.warning("Invalid credentials for user: %s", request.username)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {"sub": user_data["username"], "user_id": user_data["user_id"]}
    )
    logger.info("Access token generated for user: %s", request.username)

    return {"access_token": access_token, "token_type": "bearer"}
