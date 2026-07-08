"""Paginated inline keyboards for genre / country selection."""
from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from config import COUNTRIES, GENRES, PAGE_SIZE
from utils.pagination import offset_for_page, total_pages

from .callback_data import (
    CountryPageCallback,
    CountrySelectCallback,
    GenrePageCallback,
    GenreSelectCallback,
    MainMenuBackCallback,
)


def _paginate(items: list[str]) -> tuple[list[str], int]:
    return items, total_pages(len(items), PAGE_SIZE)


def genre_keyboard(page: int, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    pages = total_pages(len(GENRES), PAGE_SIZE)
    offset = offset_for_page(page, PAGE_SIZE)
    chunk = GENRES[offset: offset + PAGE_SIZE]

    builder = InlineKeyboardBuilder()
    for key in chunk:
        builder.button(
            text=i18n.get(f"genre-{key}"),
            callback_data=GenreSelectCallback(key=key, page=1),
        )
    builder.adjust(2)

    nav_row = []
    if page > 1:
        nav_row.append(
            InlineKeyboardButton(text=i18n.get("prev-button"), callback_data=GenrePageCallback(page=page - 1).pack())
        )
    nav_row.append(
        InlineKeyboardButton(text=i18n.get("page-indicator", current=page, total=pages), callback_data="noop")
    )
    if page < pages:
        nav_row.append(
            InlineKeyboardButton(text=i18n.get("next-button"), callback_data=GenrePageCallback(page=page + 1).pack())
        )
    builder.row(*nav_row)
    builder.row(InlineKeyboardButton(text=i18n.get("menu-back"), callback_data=MainMenuBackCallback().pack()))
    return builder.as_markup()


def country_keyboard(page: int, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    pages = total_pages(len(COUNTRIES), PAGE_SIZE)
    offset = offset_for_page(page, PAGE_SIZE)
    chunk = COUNTRIES[offset: offset + PAGE_SIZE]

    builder = InlineKeyboardBuilder()
    for key in chunk:
        builder.button(
            text=i18n.get(f"country-{key}"),
            callback_data=CountrySelectCallback(key=key, page=1),
        )
    builder.adjust(2)

    nav_row = []
    if page > 1:
        nav_row.append(
            InlineKeyboardButton(text=i18n.get("prev-button"), callback_data=CountryPageCallback(page=page - 1).pack())
        )
    nav_row.append(
        InlineKeyboardButton(text=i18n.get("page-indicator", current=page, total=pages), callback_data="noop")
    )
    if page < pages:
        nav_row.append(
            InlineKeyboardButton(text=i18n.get("next-button"), callback_data=CountryPageCallback(page=page + 1).pack())
        )
    builder.row(*nav_row)
    builder.row(InlineKeyboardButton(text=i18n.get("menu-back"), callback_data=MainMenuBackCallback().pack()))
    return builder.as_markup()
