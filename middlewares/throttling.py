"""Simple per-user throttling using an in-memory TTL cache."""
from __future__ import annotations

import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.7) -> None:
        self.rate_limit = rate_limit
        self._last_call: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        if user is not None:
            now = time.monotonic()
            last = self._last_call.get(user.id, 0.0)
            if now - last < self.rate_limit:
                return None
            self._last_call[user.id] = now

        return await handler(event, data)
