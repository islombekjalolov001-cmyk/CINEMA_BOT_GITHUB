"""Helpers to check whether a user is subscribed to mandatory channels."""
from __future__ import annotations

from urllib.parse import urlparse

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from config import MAIN_CHANNEL
from db import get_db

NOT_MEMBER_STATUSES = {"left", "kicked"}


def _is_supported_subscription_target(chat_id: str) -> bool:
    value = (chat_id or "").strip()
    if not value:
        return False

    if value.startswith(("http://", "https://")):
        parsed = urlparse(value)
        host = parsed.netloc.lower().replace("www.", "")
        return host in {"t.me", "telegram.me"}

    return value.startswith("@") or value.startswith("-100") or value.isdigit()


async def _is_member(bot: Bot, chat_id: str, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    except TelegramBadRequest:
        # Kanal topilmadi yoki bot admin emas -> obuna talabini o'tkazib yubormaymiz
        return False
    return member.status not in NOT_MEMBER_STATUSES


async def get_mandatory_channel_ids() -> list[str]:
    """Static main channel + any mandatory channels stored in the DB."""
    db = get_db()
    rows = await db.mandatory_channels()
    channel_ids = [MAIN_CHANNEL]
    channel_ids.extend(row["chat_id"] for row in rows if row["chat_id"] != MAIN_CHANNEL)
    return channel_ids


async def get_unsubscribed_channels(bot: Bot, user_id: int) -> list[str]:
    """Return the list of mandatory channel ids the user is NOT a member of."""
    missing: list[str] = []
    for chat_id in await get_mandatory_channel_ids():
        if not _is_supported_subscription_target(chat_id):
            continue
        if not await _is_member(bot, chat_id, user_id):
            missing.append(chat_id)
    return missing
