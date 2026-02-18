import functools
from pathlib import Path

from pydantic import ConfigDict
from pydantic_settings import BaseSettings
import supabase

# Root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Configuration settings loaded from the secrets folder.

    Used to set up the connection to Supabase.

    Attributes:
        supabase_url (str): The Supabase URL.
        supabase_key (str): The Supabase key.
    """

    supabase_url: str
    supabase_key: str

    # Load settings from the secrets folder
    model_config = ConfigDict(
        secrets_dir=BASE_DIR / "secrets"
    )


@functools.cache
def get_settings() -> Settings:
    """Return the cached application settings.

    This function uses functools.cache to avoid creating multiple
    Settings instances.

    Returns:
        Settings: The application settings object.
    """
    return Settings()

@functools.cache
def get_supabase_client() -> supabase.Client:
    """Factory function to get the cached Supabase client.

    This function uses functools.cache to avoid creating multiple
    supabase.Client instances. It retrieves the configuration from
    the cached Settings object.

    Returns:
        supabase.Client: A cached Supabase client instance.
    """
    settings = get_settings()
    return supabase.create_client(
        settings.supabase_url,
        settings.supabase_key,
    )
