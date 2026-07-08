"""Broadcast a message to all users with live progress reporting."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter, TelegramBadRequest
from aiogram.types import Message

from db import get_db


@dataclass
class BroadcastResult:
    total: int
    sent: int = 0
    failed: int = 0
    blocked: int = 0


async def broadcast_message(
    bot: Bot,
    source_message: Message,
    progress_callback=None,
) -> BroadcastResult:
    """Copy `source_message` to every stored user.

    `progress_callback(sent, total)` is awaited periodically so the caller
    (e.g. an admin handler) can update a "sending..." status message.
    """
    db = get_db()
    user_ids = await db.all_user_ids()
    result = BroadcastResult(total=len(user_ids))

    for index, user_id in enumerate(user_ids, start=1):
        try:
            await source_message.copy_to(chat_id=user_id)
            result.sent += 1
        except TelegramForbiddenError:
            result.blocked += 1
            await db.set_blocked(user_id, True)
        except TelegramRetryAfter as exc:
            await asyncio.sleep(exc.retry_after)
            try:
                await source_message.copy_to(chat_id=user_id)
                result.sent += 1
            except Exception:
                result.failed += 1
        except TelegramBadRequest:
            result.failed += 1
        except Exception:
            result.failed += 1

        if progress_callback is not None and index % 25 == 0:
            await progress_callback(index, result.total)

        # Telegram flood-control friendly pacing
        await asyncio.sleep(0.05)

    if progress_callback is not None:
        await progress_callback(result.total, result.total)

    return result
