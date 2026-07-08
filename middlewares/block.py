"""Blocks interactions for users marked as blocked in the database."""
from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, TelegramObject

from db import Database


class BlockMiddleware(BaseMiddleware):
    def __init__(self, db: Database) -> None:
        self.db = db

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        db_user = await self.db.get_user(user.id)
        if db_user is not None and bool(db_user["is_blocked"]):
            i18n = data.get("i18n")
            text = "You are blocked from using this bot." if i18n is None else i18n.get("blocked-user-message")
            if isinstance(event, CallbackQuery):
                await event.answer(text, show_alert=True)
            else:
                await event.answer(text)
            return None

        return await handler(event, data)
