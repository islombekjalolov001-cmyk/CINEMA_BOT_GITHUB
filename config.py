"""Configuration module. Loads environment variables via python-dotenv."""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Holds all runtime configuration for the bot."""

    bot_token: str
    admin_ids: list[int] = field(default_factory=list)
    db_path: str = "data/database.db"
    log_path: str = "logs/bot.log"
    default_locale: str = "uz"
    locales_dir: str = "locales"

    @classmethod
    def load(cls) -> "Config":
        token = os.getenv("BOT_TOKEN", "")
        if not token:
            raise RuntimeError("BOT_TOKEN topilmadi. .env faylini tekshiring.")

        raw_admins = os.getenv("ADMIN_IDS", "8560459628")
        admin_ids = [int(x.strip()) for x in raw_admins.split(",") if x.strip()]

        return cls(
            bot_token=token,
            admin_ids=admin_ids,
            db_path=os.getenv("DB_PATH", "data/database.db"),
            log_path=os.getenv("LOG_PATH", "logs/bot.log"),
        )


config = Config.load()

# Majburiy asosiy kanal (statik). Qo'shimcha kanallar DB orqali boshqariladi.
MAIN_CHANNEL = "@uzbmediakino"

SUPPORTED_LANGUAGES = ("uz", "ru", "en")

LANGUAGE_FLAGS = {
    "uz": "🇺🇿",
    "ru": "🇷🇺",
    "en": "🇺🇸",
}

GENRES = [
    "action", "comedy", "drama", "horror", "romance", "thriller",
    "fantasy", "scifi", "animation", "documentary", "adventure",
    "crime", "family", "musical", "war", "history", "mystery", "sport",
]

COUNTRIES = [
    "uzbekistan", "turkey", "usa", "russia", "india", "south_korea",
    "france", "germany", "china", "japan", "united_kingdom", "italy",
    "spain", "brazil", "mexico", "canada", "iran", "egypt", "kazakhstan", "other",
]

PAGE_SIZE = 10
