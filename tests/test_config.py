import pytest
from app.core.config import Settings

@pytest.fixture
def temp_env(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://fake.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "randomkey123456")
    yield

def test_supabase_settings(temp_env):
    settings = Settings()
    assert isinstance(settings.supabase_url, str)
    assert settings.supabase_url.startswith("https://")
    assert isinstance(settings.supabase_key, str)
    assert len(settings.supabase_key) > 10
