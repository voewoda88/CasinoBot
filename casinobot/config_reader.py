from enum import Enum
import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    bot_token: SecretStr
    fsm_mode: str
    bot_language: str
    starting_points: int = 50
    starting_bet: int = 1
    send_gameover_sticker: bool = False
    throttle_time_spin: int = 2
    throttle_time_other: int = 1

    model_config = SettingsConfigDict(env_file='config.env', env_file_encoding='utf-8')