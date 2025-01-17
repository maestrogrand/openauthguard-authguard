from fastapi import Request, HTTPException
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.config import settings
from src.core.logging import logger
from src.utils.http_client import fetch_user


class JWTValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for validating JWT tokens for microservice communication.
    """

    async def dispatch(self, request: Request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url.path}")

        public_endpoints = ["/health", "/"]
        if any(request.url.path.startswith(endpoint) for endpoint in public_endpoints):
            logger.debug(f"Skipping JWT validation for {request.url.path}.")
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            logger.warning("Missing or invalid Authorization header.")
            raise HTTPException(
                status_code=403, detail="Authorization token is required."
            )

        try:
            token = token.split(" ")[1]
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )

            if (
                "sub" not in payload
                or "user_id" not in payload
                or "role" not in payload
            ):
                logger.warning("Token is missing required claims.")
                raise HTTPException(status_code=403, detail="Invalid token claims.")

            user = await fetch_user(payload["sub"], settings.users_service_url)
            if not user:
                logger.warning("User not found in the Users service.")
                raise HTTPException(status_code=404, detail="User not found.")

            logger.debug("JWT token validated successfully.")
        except JWTError as e:
            logger.error(f"JWT validation failed: {e}")
            raise HTTPException(status_code=403, detail="Invalid or expired token.")

        return await call_next(request)
