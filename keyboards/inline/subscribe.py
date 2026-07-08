"""Inline keyboard listing mandatory channels + a 'check' button."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from .callback_data import SubCheckCallback


def subscribe_keyboard(channel_ids: list[str], i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for chat_id in channel_ids:
        username = chat_id.lstrip("@")
        builder.button(
            text=f"{i18n.get('sub-button')} {chat_id}",
            url=f"https://t.me/{username}",
        )
    builder.adjust(1)
    builder.row(
        InlineKeyboardButton(
            text=i18n.get("sub-check-button"),
            callback_data=SubCheckCallback().pack(),
        )
    )
    return builder.as_markup()
