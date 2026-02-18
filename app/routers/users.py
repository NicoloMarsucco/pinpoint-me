import fastapi
import supabase

from app.core import config
from app.schemas.auth import SignupRequest

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

