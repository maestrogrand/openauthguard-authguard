from datetime import timedelta
from fastapi import HTTPException
import os

from src.auth.schemas import CompanyLogin, IndividualLogin, TokenResponse
from src.core.config import settings
from src.utils.helpers import verify_password, create_access_token
from src.utils.http_client import fetch_user, fetch_tenant

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL")


async def authenticate_company_user(request: CompanyLogin) -> TokenResponse:
    """
    Authenticate a company user by validating their credentials.
    """
    tenant = await fetch_tenant(request.company_name, USERS_SERVICE_URL)
    if not tenant:
        raise HTTPException(status_code=400, detail="Company not found.")

    user = await fetch_user(request.username, USERS_SERVICE_URL)
    if (
        not user
        or user["tenant_id"] != tenant["tenant_id"]
        or not verify_password(request.password, user["password_hash"])
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    access_token = create_access_token(
        data={
            "sub": user["username"],
            "user_id": user["user_id"],
            "role": user["role"],
            "tenant_id": user["tenant_id"],
        },
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        tenant_id=user["tenant_id"],
    )


async def authenticate_individual_user(request: IndividualLogin) -> TokenResponse:
    """
    Authenticate an individual user by validating their credentials via the Users service.
    """
    user = await fetch_user(request.username, USERS_SERVICE_URL)
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    access_token = create_access_token(
        data={
            "sub": user["username"],
            "user_id": user["user_id"],
            "role": user["role"],
        },
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
