import pytest
import fastapi
import supabase
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app import main

client = TestClient(main.app)

AUTH_PREFIX = "api/v1"

###### SIGNUP #######

def test_signup_success():
    """Test that a user can successfully sign up."""
    mock_user = {"id": "123", "email": "user@example.com"}

    with patch("app.core.config.get_supabase_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.auth.sign_up.return_value = mock_user
        mock_get_client.return_value = mock_client

        response = client.post(
            f"{AUTH_PREFIX}/signup",
            json={"email": "user@example.com", "password": "securepassword123"}
        )

    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

def test_signup_email_already_registered():
    """Test signup when the email is already registered."""
    with patch("app.core.config.get_supabase_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.auth.sign_up.side_effect = supabase.AuthApiError(
            "Email already registered", 400, "BAD_REQUEST"
        )
        mock_get_client.return_value = mock_client

        response = client.post(
            f"{AUTH_PREFIX}/signup",
            json={"email": "user@example.com", "password": "securepassword123"}
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}



def test_signup_generic_failure():
    """Test signup when a generic Supabase error occurs."""
    with patch("app.core.config.get_supabase_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.auth.sign_up.side_effect = supabase.AuthApiError(
            "Something went wrong", 500, "INTERNAL_SERVER_ERROR"
        )
        mock_get_client.return_value = mock_client

        response = client.post(
            f"{AUTH_PREFIX}/signup",
            json={"email": "user@example.com", "password": "securepassword123"}
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "Signup failed"}

###### LOGIN #######

def test_login_success():
    """Test successful login returns tokens."""
    with patch("app.core.config.get_supabase_client") as mock_get_client:
        mock_client = MagicMock()

        # Mock Supabase session object
        mock_session = MagicMock()
        mock_session.access_token = "access123"
        mock_session.refresh_token = "refresh123"

        mock_response = MagicMock()
        mock_response.session = mock_session

        mock_client.auth.sign_in_with_password.return_value = mock_response
        mock_get_client.return_value = mock_client

        response = client.post(
            f"{AUTH_PREFIX}/login",
            json={
                "email": "user@example.com",
                "password": "securepassword123",
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "access123",
        "refresh_token": "refresh123",
        "token_type": "bearer",
    }


def test_login_invalid_credentials():
    """Test login with invalid credentials returns 401."""
    with patch("app.core.config.get_supabase_client") as mock_get_client:
        mock_client = MagicMock()

        mock_client.auth.sign_in_with_password.side_effect = supabase.AuthApiError(
            message="Invalid login credentials",
            status=401,
            code="invalid_credentials",
        )

        mock_get_client.return_value = mock_client

        response = client.post(
            f"{AUTH_PREFIX}/login",
            json={
                "email": "user@example.com",
                "password": "wrongpassword",
            },
        )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid email or password"
    }


def test_login_invalid_email_format():
    """Test validation error for invalid email."""
    response = client.post(
        f"{AUTH_PREFIX}/login",
        json={
            "email": "not-an-email",
            "password": "securepassword123",
        },
    )

    assert response.status_code == 422


def test_login_short_password():
    """Test validation error for short password."""
    response = client.post(
        f"{AUTH_PREFIX}/login",
        json={
            "email": "user@example.com",
            "password": "123",
        },
    )

    assert response.status_code == 422
