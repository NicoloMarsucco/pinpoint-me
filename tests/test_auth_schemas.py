import pytest
from pydantic import ValidationError

from app.schemas.auth import SignupRequest


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