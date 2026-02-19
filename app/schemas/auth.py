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
