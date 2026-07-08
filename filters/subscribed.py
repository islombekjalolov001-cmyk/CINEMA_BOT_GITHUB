"""Filter that verifies a user is subscribed to all mandatory channels."""
from __future__ import annotations

from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message

from services.subscription import get_unsubscribed_channels


class SubscribedFilter(BaseFilter):
    """Passes only if the user has joined every mandatory channel."""

    async def __call__(self, message: Message, bot: Bot) -> bool:
        if message.from_user is None:
            return False
        missing = await get_unsubscribed_channels(bot, message.from_user.id)
        return len(missing) == 0
