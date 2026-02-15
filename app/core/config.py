from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from pathlib import Path

# Root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Configuration settings loaded from secrets folder."""
    supabase_url: str
    supabase_key: str

    model_config = ConfigDict(
        secrets_dir=BASE_DIR / "secrets"
    )

# Single instance of Settings to use throughout the project
settings = Settings()