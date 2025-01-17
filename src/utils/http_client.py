import httpx
from fastapi import HTTPException
from src.core.logging import logger


async def fetch_user(username: str, users_service_url: str) -> dict:
    """
    Fetch user details from the Users service by username.
    """
    url = f"{users_service_url}/users/username/{username}"
    logger.debug(f"Fetching user details from URL: {url}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            logger.debug(
                f"Received response from Users service: {response.status_code} - {response.text}"
            )
            response.raise_for_status()
            user_data = response.json()
            logger.info(f"Successfully fetched user details for username: {username}")
            return user_data
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error while fetching user details: {e.response.status_code} - {e.response.text}"
        )
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Unexpected error while fetching user details: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def fetch_tenant(company_name: str, users_service_url: str) -> dict:
    """
    Fetch tenant details from the Users service by company name.
    """
    url = f"{users_service_url}/tenants/{company_name}"
    logger.debug(f"Fetching tenant details from URL: {url}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            logger.debug(
                f"Received response from Tenant service: {response.status_code} - {response.text}"
            )
            response.raise_for_status()
            tenant_data = response.json()
            logger.info(
                f"Successfully fetched tenant details for company: {company_name}"
            )
            return tenant_data
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error while fetching tenant details: {e.response.status_code} - {e.response.text}"
        )
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Unexpected error while fetching tenant details: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
