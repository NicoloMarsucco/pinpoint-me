import pytest
import fastapi
import supabase
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app import main

client = TestClient(main.app)


def test_signup_success():
    """Test that a user can successfully sign up."""
    mock_user = {"id": "123", "email": "user@example.com"}

    with patch("app.core.config.get_supabase_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.auth.sign_up.return_value = mock_user
        mock_get_client.return_value = mock_client

        response = client.post(
            "/signup",
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
            "/signup",
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
            "/signup",
            json={"email": "user@example.com", "password": "securepassword123"}
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "Signup failed"}
