"""Injects a Fluentogram translator (`i18n`) matching the user's language.

The middleware reads the user's saved language from the database (falling
back to Telegram's `language_code` / the default locale) and stores a ready
`TranslatorRunner` in the handler data dict as `i18n`, so every handler can
simply do `i18n.get("some-key")`.
"""
from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from fluentogram import TranslatorHub

from config import SUPPORTED_LANGUAGES, config
from db import get_db


class TranslatorRunnerMiddleware(BaseMiddleware):
    def __init__(self, translator_hub: TranslatorHub) -> None:
        self.translator_hub = translator_hub

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        locale = config.default_locale

        if user is not None:
            db_user = await get_db().get_user(user.id)
            if db_user is not None:
                locale = db_user["language"]
            elif user.language_code in SUPPORTED_LANGUAGES:
                locale = user.language_code

        data["i18n"] = self.translator_hub.get_translator_by_locale(locale)
        data["locale"] = locale
        return await handler(event, data)
