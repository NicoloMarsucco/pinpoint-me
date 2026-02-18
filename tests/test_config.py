import pytest

from app.core import config


@pytest.fixture
def temp_env(monkeypatch):
    """Override environment variables for testing Settings.

    Temporarily sets SUPABASE_URL and SUPABASE_KEY for testing.
    """
    monkeypatch.setenv("SUPABASE_URL", "https://fake.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "randomkey123456")
    yield


def test_supabase_settings(temp_env):
    """Test that Supabase settings are loaded correctly from the environment.

    Checks that supabase_url is a string starting with https://
    and that supabase_key is a string with length > 10.
    """
    settings = config.get_settings()

    # URL should be a string and start with https://
    assert isinstance(settings.supabase_url, str), "supabase_url should be a string"
    assert settings.supabase_url.startswith("https://"), "supabase_url should start with https://"

    # Key should be a string and reasonably long
    assert isinstance(settings.supabase_key, str), "supabase_key should be a string"
    assert len(settings.supabase_key) > 10, "supabase_key should be longer than 10 characters"
