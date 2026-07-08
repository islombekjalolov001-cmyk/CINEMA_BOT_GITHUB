"""Inline keyboards for a single movie card and paginated movie lists."""
from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from .callback_data import LikeCallback, MoviesPageCallback


def movie_card_keyboard(code: int, like_count: int, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.get("movie-like-button", count=like_count),
        callback_data=LikeCallback(code=code),
    )
    return builder.as_markup()


def movie_browse_keyboard(
    scope: str,
    key: str,
    code: int,
    like_count: int,
    page: int,
    pages: int,
    i18n: TranslatorRunner,
) -> InlineKeyboardMarkup:
    """Used when browsing movies one-by-one inside genre/country/favorites.

    Shows the like button on its own row, then prev/page/next navigation.
    """
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=i18n.get("movie-like-button", count=like_count),
            callback_data=LikeCallback(code=code).pack(),
        )
    )
    nav_row = []
    if page > 1:
        nav_row.append(
            InlineKeyboardButton(
                text=i18n.get("prev-button"),
                callback_data=MoviesPageCallback(scope=scope, key=key, page=page - 1).pack(),
            )
        )
    nav_row.append(
        InlineKeyboardButton(text=i18n.get("page-indicator", current=page, total=pages), callback_data="noop")
    )
    if page < pages:
        nav_row.append(
            InlineKeyboardButton(
                text=i18n.get("next-button"),
                callback_data=MoviesPageCallback(scope=scope, key=key, page=page + 1).pack(),
            )
        )
    builder.row(*nav_row)
    return builder.as_markup()


def movies_list_pagination_keyboard(
    scope: str, key: str, page: int, pages: int, i18n: TranslatorRunner
) -> InlineKeyboardMarkup:
    """scope: 'genre' | 'country' | 'favorites'."""
    builder = InlineKeyboardBuilder()
    nav_row = []
    if page > 1:
        nav_row.append(
            InlineKeyboardButton(
                text=i18n.get("prev-button"),
                callback_data=MoviesPageCallback(scope=scope, key=key, page=page - 1).pack(),
            )
        )
    nav_row.append(
        InlineKeyboardButton(text=i18n.get("page-indicator", current=page, total=pages), callback_data="noop")
    )
    if page < pages:
        nav_row.append(
            InlineKeyboardButton(
                text=i18n.get("next-button"),
                callback_data=MoviesPageCallback(scope=scope, key=key, page=page + 1).pack(),
            )
        )
    builder.row(*nav_row)
    return builder.as_markup()
