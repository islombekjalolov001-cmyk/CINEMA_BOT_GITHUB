"""Inline keyboard for choosing the interface language."""
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import LANGUAGE_FLAGS, SUPPORTED_LANGUAGES
from fluentogram import TranslatorRunner

from .callback_data import LanguageCallback, SettingsCallback

LANGUAGE_NAMES = {
    "uz": "O'zbekcha",
    "ru": "Русский",
    "en": "English",
}


def language_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for code in SUPPORTED_LANGUAGES:
        text = f"{LANGUAGE_FLAGS[code]} {LANGUAGE_NAMES[code]}"
        builder.button(text=text, callback_data=LanguageCallback(code=code))
    builder.button(text=i18n.get("menu-back"), callback_data=SettingsCallback(action="back").pack())
    builder.adjust(1)
    return builder.as_markup()
