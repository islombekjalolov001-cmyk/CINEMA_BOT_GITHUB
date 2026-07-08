"""Filter that only lets configured/DB admins pass."""
from __future__ import annotations

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from config import config
from db import get_db


class AdminFilter(BaseFilter):
    """Passes only for users listed in ADMIN_IDS or the `admins` table."""

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = event.from_user
        if user is None:
            return False
        return await get_db().is_admin(user.id, config.admin_ids)
