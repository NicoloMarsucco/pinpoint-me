import pytest
from pydantic import ValidationError

from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse


def test_signup_request_valid():
    obj = SignupRequest(email="user@example.com", password="secure123")
    assert obj.email == "user@example.com"
    assert obj.password == "secure123"

def test_signup_request_invalid_email():
    with pytest.raises(ValidationError):
        SignupRequest(email="not-an-email", password="secure123")

def test_signup_request_short_password():
    with pytest.raises(ValidationError):
        SignupRequest(email="user@example.com", password="123")

def test_login_request_valid():
    obj = LoginRequest(email="user@example.com", password="secure123")
    assert obj.email == "user@example.com"
    assert obj.password == "secure123"

def test_login_request_invalid_email():
    with pytest.raises(ValidationError):
        LoginRequest(email="not-an-email", password="secure123")

def test_login_request_short_password():
    with pytest.raises(ValidationError):
        LoginRequest(email="user@example.com", password="123")

def test_token_response_valid():
    obj = TokenResponse(
        access_token="access_token",
        refresh_token="refresh_token",
        token_type="bearer"
    )
    assert obj.access_token == "access_token"
    assert obj.refresh_token == "refresh_token"
    assert obj.token_type == "bearer"

def test_token_response_immutable():
    obj = TokenResponse(
        access_token="",
        refresh_token="",
        token_type=""
    )
    with pytest.raises(ValidationError):
        obj.access_token = "a"
    with pytest.raises(ValidationError):
        obj.refresh_token = "b"
    with pytest.raises(ValidationError):
        obj.token_type = "c"