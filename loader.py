"""Central place where the Bot, Dispatcher, Database and i18n hub are built.

Importing `loader` gives every other module access to the same singleton
instances, matching the "loader.py" convention requested in the spec.
"""
from __future__ import annotations

from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

from config import SUPPORTED_LANGUAGES, config
from db import Database, set_db
from middlewares import BlockMiddleware, DatabaseMiddleware, ThrottlingMiddleware, TranslatorRunnerMiddleware

BASE_DIR = Path(__file__).resolve().parent


def create_translator_hub() -> TranslatorHub:
    """Build a Fluentogram TranslatorHub from the .ftl files under locales/."""
    translators = []
    for locale in SUPPORTED_LANGUAGES:
        ftl_path = BASE_DIR / "locales" / locale / "LC_MESSAGES" / "txt.ftl"
        bundle = FluentBundle.from_files(locale, filenames=[str(ftl_path)])
        translators.append(FluentTranslator(locale=locale, translator=bundle))

    return TranslatorHub(
        locales_map={
            "uz": ("uz", "en"),
            "ru": ("ru", "en"),
            "en": ("en",),
        },
        translators=translators,
        root_locale="en",
    )


bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

db = Database(config.db_path)
set_db(db)

translator_hub = create_translator_hub()


def setup_middlewares() -> None:
    dp.update.middleware(DatabaseMiddleware(db))
    dp.update.middleware(TranslatorRunnerMiddleware(translator_hub))
    dp.update.middleware(BlockMiddleware(db))
    dp.message.middleware(ThrottlingMiddleware())
