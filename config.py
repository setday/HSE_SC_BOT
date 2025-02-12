from __future__ import annotations

from pathlib import Path
import secrets
from typing import Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    A base configuration class that reads the environment variables and validates them.
    """
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")

    project_dir: Path = Field(default=Path(__file__).parent, env="PROJECT_DIR")
    assets_dir: Path = Field(default=Path(__file__).parent / "Assets", env="ASSETS_DIR")

    standart_posters_dir: Path = Field(default=Path(__file__).parent / "Assets" / "Posters" / "Standart", env="DEFAULT_POSTERS_DIR")
    valentines_day_posters_dir: Path = Field(default=Path(__file__).parent / "Assets" / "Posters" / "ValentinesDay", env="VALENTINES_DAY_POSTERS_DIR")
    posters_dir: Path = Field(default=Path(__file__).parent / "Assets" / "Posters" / "Standart", env="POSTERS_DIR")

    bot_api_token: str = Field(default=None, env="BOT_API_TOKEN")
    
    back_chat_id: int = Field(default=None, env="BACK_CHAT_ID")
    vote_chat_id: int = Field(default=None, env="VOTE_CHAT_ID")

    secret_trash: str = Field(default=secrets.token_urlsafe(32), env="SECRET_TRASH")

    current_event: Optional[str] = Field(default=None, env="CURRENT_EVENT")

    @model_validator(mode="after")
    def set_assets_path(self) -> "Config":
        self.activate_event(self.current_event)

        # check if path exists
        if not self.assets_dir.exists():
            raise FileNotFoundError(f"Assets directory not found: {self.assets_dir}")
        if not self.standart_posters_dir.exists():
            raise FileNotFoundError(f"Standart posters directory not found: {self.standart_posters_dir}")
        if not self.valentines_day_posters_dir.exists():
            raise FileNotFoundError(f"Valentines Day posters directory not found: {self.valentines_day_posters_dir}")
        if not self.posters_dir.exists():
            raise FileNotFoundError(f"Posters directory not found: {self.posters_dir}")

        return self

    def activate_event(self, event: str | None) -> None:
        self.current_event = event

        match event:
            case "valentines_day":
                self.posters_dir = self.valentines_day_posters_dir
            case _:
                self.posters_dir = self.standart_posters_dir
        
config = Config()
