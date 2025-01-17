from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class CompanyLogin(BaseModel):
    company_name: str
    username: str
    password: str


class IndividualLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    tenant_id: Optional[str] = None
