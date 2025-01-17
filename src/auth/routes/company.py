import sqlalchemy as sa
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from src.auth.schemas import CompanyLogin, TokenResponse
from src.auth.services import authenticate_company_user
from src.core.config import settings
from src.core.database import get_db

router = APIRouter(tags=["Company Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login_company(request: CompanyLogin, db: Session = Depends(get_db)):
    """
    Endpoint to log in a company user.
    """
    token_data = await authenticate_company_user(request)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = str(uuid4())
    created_at = datetime.utcnow()
    expires_at = created_at + timedelta(minutes=settings.access_token_expire_minutes)

    insert_query = sa.text("""
        INSERT INTO authguard_service.sessions (session_id, user_id, token, created_at, expires_at)
        VALUES (:session_id, :user_id, :token, :created_at, :expires_at)
    """)
    db.execute(
        insert_query,
        {
            "session_id": session_id,
            "user_id": token_data.user_id,
            "token": token_data.access_token,
            "created_at": created_at,
            "expires_at": expires_at,
        }
    )
    db.commit()

    return token_data


@router.post("/register", response_model=TokenResponse)
async def register_company(request: CompanyLogin):
    """
    Endpoint to register a new company and admin user.

    This endpoint assumes the `users` service handles tenant registration.
    """
    raise HTTPException(status_code=501, detail="Registration through this endpoint is not supported.")
