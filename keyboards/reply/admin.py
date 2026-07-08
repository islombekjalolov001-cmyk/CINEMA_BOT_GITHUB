"""Reply keyboard shown to admins on /admin."""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from fluentogram import TranslatorRunner


def admin_menu_keyboard(i18n: TranslatorRunner) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=i18n.get("admin-movies")))
    builder.row(KeyboardButton(text=i18n.get("admin-channels")))
    builder.row(
        KeyboardButton(text=i18n.get("admin-broadcast")),
        KeyboardButton(text=i18n.get("admin-stats")),
    )
    builder.row(
        KeyboardButton(text=i18n.get("admin-export")),
        KeyboardButton(text=i18n.get("admin-all-codes")),
    )
    builder.row(
        KeyboardButton(text=i18n.get("admin-block-user")),
        KeyboardButton(text=i18n.get("admin-blocked-users")),
    )
    builder.row(KeyboardButton(text=i18n.get("menu-back")))
    return builder.as_markup(resize_keyboard=True)


def admin_movies_menu_keyboard(i18n: TranslatorRunner) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=i18n.get("admin-add-movie")),
        KeyboardButton(text=i18n.get("admin-edit-movie")),
        KeyboardButton(text=i18n.get("admin-delete-movie")),
    )
    builder.row(KeyboardButton(text=i18n.get("admin-back")))
    return builder.as_markup(resize_keyboard=True)


def admin_channels_menu_keyboard(i18n: TranslatorRunner) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=i18n.get("admin-add-mandatory")))
    builder.row(KeyboardButton(text=i18n.get("admin-remove-mandatory")))
    builder.row(KeyboardButton(text=i18n.get("admin-add-optional")))
    builder.row(KeyboardButton(text=i18n.get("admin-remove-optional")))
    builder.row(KeyboardButton(text=i18n.get("admin-back")))
    return builder.as_markup(resize_keyboard=True)
