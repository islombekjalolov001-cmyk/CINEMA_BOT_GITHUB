"""Reply keyboard shown to regular users on the main menu."""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from fluentogram import TranslatorRunner


def main_menu_keyboard(i18n: TranslatorRunner) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=i18n.get("menu-search-code")))
    builder.row(KeyboardButton(text=i18n.get("menu-search-name")))
    builder.row(
        KeyboardButton(text=i18n.get("menu-search-genre")),
        KeyboardButton(text=i18n.get("menu-search-country")),
    )
    builder.row(
        KeyboardButton(text=i18n.get("menu-request-movie")),
        KeyboardButton(text=i18n.get("menu-settings")),
    )
    builder.row(KeyboardButton(text=i18n.get("menu-back")))
    return builder.as_markup(resize_keyboard=True)


def search_back_keyboard(i18n: TranslatorRunner) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=i18n.get("menu-back")))
    return builder.as_markup(resize_keyboard=True)
