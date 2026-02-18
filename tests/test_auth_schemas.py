import pytest
from pydantic import ValidationError

from app.schemas import auth


def test_signup_request_valid():
    obj = auth.SignupRequest(email="user@example.com", password="secure123")
    assert obj.email == "user@example.com"
    assert obj.password == "secure123"

def test_signup_request_invalid_email():
    with pytest.raises(ValidationError):
        auth.SignupRequest(email="not-an-email", password="secure123")

def test_signup_request_short_password():
    with pytest.raises(ValidationError):
        auth.SignupRequest(email="user@example.com", password="123")