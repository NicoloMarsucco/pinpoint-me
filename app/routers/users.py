import fastapi
import supabase

from app.core import config
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse

router = fastapi.APIRouter()


@router.post("/signup")
def signup(request: SignupRequest):
    """Sign up a new user with Supabase.

    This route uses the Supabase client to create a new user account.
    Only Supabase-specific errors are caught and mapped to HTTP responses.
    Pydantic automatically validates the request.

    Args:
        request (SignupRequest): Request body containing email and password.

    Returns:
        dict: Success message if the user is created.

    Raises:
        fastapi.HTTPException: If the signup fails due to Supabase errors.
    """
    try:
        client = config.get_supabase_client()
        client.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        return {"message": "User created successfully"}

    except supabase.AuthApiError as e:
        msg = str(e)
        if "already registered" in msg.lower():
            raise fastapi.HTTPException(status_code=400, detail="Email already registered")
        raise fastapi.HTTPException(status_code=400, detail="Signup failed")

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate user and return JWT tokens"
)
def login(request: LoginRequest):
    """Log in a user using Supabase.

    Authenticates the user with email and password and returns
    an access token and refresh token to be used by the frontend.

    Args:
        request: Request body containing the user's email and password.

    Returns:
        TokenResponse: Object containing the access token,
            refresh token, and token type.

    Raises:
        fastapi.HTTPException: If authentication fails due to
            invalid credentials or Supabase errors.
    """
    client = config.get_supabase_client()

    try:
        response = client.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password,
        })

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer",
        }
    except supabase.AuthApiError as e:
        raise fastapi.HTTPException(
            status_code=401, 
            detail="Invalid email or password"
        )