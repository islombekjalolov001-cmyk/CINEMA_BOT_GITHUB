"""Handles the ❤️ Like button on every movie card."""
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner

from db import Database
from keyboards.inline.callback_data import LikeCallback

router = Router(name="user_like")


@router.callback_query(LikeCallback.filter())
async def like_movie(
    callback: CallbackQuery, callback_data: LikeCallback, db: Database, i18n: TranslatorRunner
) -> None:
    added = await db.add_like(callback.from_user.id, callback_data.code)
    if not added:
        await callback.answer(i18n.get("movie-already-liked"), show_alert=True)
        return

    await callback.answer(i18n.get("movie-liked"))

    like_count = await db.count_likes(callback_data.code)
    # Refresh only the like button's caption count; keep the rest of the keyboard intact.
    markup = callback.message.reply_markup
    if markup is None:
        return

    new_rows = []
    for row in markup.inline_keyboard:
        new_row = []
        for button in row:
            if button.callback_data == callback_data.pack():
                button = button.model_copy(update={"text": i18n.get("movie-like-button", count=like_count)})
            new_row.append(button)
        new_rows.append(new_row)

    from aiogram.types import InlineKeyboardMarkup

    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=new_rows))
