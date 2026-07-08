"""Inline keyboards used only inside the admin panel."""
from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from config import COUNTRIES, GENRES, PAGE_SIZE
from utils.pagination import offset_for_page, total_pages

from .callback_data import (
    AdminCodeItemCallback,
    AdminCodesPageCallback,
    AdminConfirmCallback,
    AdminCountrySelectCallback,
    AdminEditFieldCallback,
    AdminGenreSelectCallback,
)


def admin_genre_pick_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key in GENRES:
        builder.button(text=i18n.get(f"genre-{key}"), callback_data=AdminGenreSelectCallback(key=key))
    builder.adjust(2)
    return builder.as_markup()


def admin_country_pick_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key in COUNTRIES:
        builder.button(text=i18n.get(f"country-{key}"), callback_data=AdminCountrySelectCallback(key=key))
    builder.adjust(2)
    return builder.as_markup()


def admin_confirm_add_keyboard(code: int, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.get("admin-yes"),
        callback_data=AdminConfirmCallback(action="add_movie", value=str(code), yes=True),
    )
    builder.button(
        text=i18n.get("admin-no"),
        callback_data=AdminConfirmCallback(action="add_movie", value=str(code), yes=False),
    )
    return builder.as_markup()


def admin_confirm_delete_keyboard(code: int, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.get("admin-yes"),
        callback_data=AdminConfirmCallback(action="delete_movie", value=str(code), yes=True),
    )
    builder.button(
        text=i18n.get("admin-no"),
        callback_data=AdminConfirmCallback(action="delete_movie", value=str(code), yes=False),
    )
    return builder.as_markup()


def admin_edit_fields_keyboard(code: int, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    fields = ["title", "genre", "country", "year", "rating", "description", "file"]
    builder = InlineKeyboardBuilder()
    for field in fields:
        builder.button(
            text=i18n.get(f"admin-field-{field}"),
            callback_data=AdminEditFieldCallback(code=code, field=field),
        )
    builder.adjust(2)
    return builder.as_markup()


def admin_codes_list_keyboard(
    movies: list, page: int, total_items: int, i18n: TranslatorRunner
) -> InlineKeyboardMarkup:
    pages = total_pages(total_items, PAGE_SIZE)
    builder = InlineKeyboardBuilder()
    for row in movies:
        builder.button(
            text=i18n.get("admin-code-item", code=row["code"], title=row["title"]),
            callback_data=AdminCodeItemCallback(code=row["code"]),
        )
    builder.adjust(1)

    nav_row = []
    if page > 1:
        nav_row.append(
            InlineKeyboardButton(
                text=i18n.get("prev-button"), callback_data=AdminCodesPageCallback(page=page - 1).pack()
            )
        )
    nav_row.append(
        InlineKeyboardButton(text=i18n.get("page-indicator", current=page, total=pages), callback_data="noop")
    )
    if page < pages:
        nav_row.append(
            InlineKeyboardButton(
                text=i18n.get("next-button"), callback_data=AdminCodesPageCallback(page=page + 1).pack()
            )
        )
    builder.row(*nav_row)
    return builder.as_markup()


def admin_code_item_actions_keyboard(code: int, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.get("admin-edit-movie"), callback_data=AdminEditFieldCallback(code=code, field="_menu"))
    builder.button(
        text=i18n.get("admin-delete-movie"),
        callback_data=AdminConfirmCallback(action="ask_delete", value=str(code), yes=False),
    )
    builder.adjust(2)
    return builder.as_markup()
