from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Request body for creating a new user.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password (minimum length 8 characters).
    """
    
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., min_length=8, description="The user's password")

class LoginRequest(BaseModel):
    """Request to login.
    
    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password (minimum length 8 characters).
    """

    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., min_length=8, description="The user's password")

class TokenResponse(BaseModel, frozen=True):
    """Response body returned after successful authentication.

    Attributes:
        access_token (str): JWT access token used to authenticate API requests
        refresh_token (str): Token used to obtain a new access token when it expires.
        token_type (str): Type of the token (usually 'bearer')
    """
    access_token: str = Field(
        ...,
        description="JWT access token used to authenticate API requests"
    )
    refresh_token: str = Field(
        ...,
        description="Token used to obtain a new access token when it expires"
    )
    token_type: str = Field(
        ...,
        description="Type of the token (usually 'bearer')"
    )