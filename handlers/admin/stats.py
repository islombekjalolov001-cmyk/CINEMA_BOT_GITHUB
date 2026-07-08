"""📊 Show basic user statistics (total / today / week / month)."""
from __future__ import annotations

import time

from aiogram import F, Router
from aiogram.types import Message
from fluentogram import TranslatorRunner

from db import Database

router = Router(name="admin_stats")

STATS_TEXTS = {"📊 Statistika", "📊 Статистика", "📊 Statistics"}
DAY = 86400


@router.message(F.text.in_(STATS_TEXTS))
async def show_stats(message: Message, db: Database, i18n: TranslatorRunner) -> None:
    now = int(time.time())
    total = await db.count_users_total()
    today = await db.count_users_since(now - DAY)
    week = await db.count_users_since(now - 7 * DAY)
    month = await db.count_users_since(now - 30 * DAY)

    await message.answer(i18n.get("admin-stats-title", total=total, today=today, week=week, month=month))
