from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from src.core.config import settings
from src.utils.helpers import decode_access_token


def get_current_user(token: str = Depends(decode_access_token)) -> dict:
    """
    Validate the JWT token and return the user claims.
    """
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing token.")

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if "sub" not in payload or "user_id" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token payload.")
        return payload
    except JWTError as e:
        raise HTTPException(status_code=403, detail=f"Token validation failed: {e}")
