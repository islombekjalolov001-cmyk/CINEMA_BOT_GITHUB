"""Browse movies by country: pick a country, then page through matching movies."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from db import Database
from keyboards.inline.callback_data import CountryPageCallback, CountrySelectCallback, MainMenuBackCallback, MoviesPageCallback
from keyboards.inline.genre_country import country_keyboard
from keyboards.inline.movie import movie_browse_keyboard
from keyboards.reply.user import main_menu_keyboard
from utils.pagination import clamp_page, total_pages

router = Router(name="user_country")

MENU_TEXTS = {"🌍 Davlat bo'yicha qidirish", "🌍 Поиск по стране", "🌍 Search by country"}


@router.message(F.text.in_(MENU_TEXTS))
async def open_country_menu(message: Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.get("choose-country"), reply_markup=country_keyboard(1, i18n))


@router.callback_query(MainMenuBackCallback.filter())
async def back_from_country_menu(callback: CallbackQuery, i18n: TranslatorRunner) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        i18n.get("start-greeting", name=callback.from_user.full_name),
        reply_markup=main_menu_keyboard(i18n),
    )


@router.callback_query(CountryPageCallback.filter())
async def paginate_countries(callback: CallbackQuery, callback_data: CountryPageCallback, i18n: TranslatorRunner) -> None:
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=country_keyboard(callback_data.page, i18n))


async def _show_movie_at(callback: CallbackQuery, db: Database, i18n: TranslatorRunner, country: str, page: int) -> None:
    total = await db.count_movies_by_country(country)
    pages = total_pages(total, 1)
    page = clamp_page(page, pages)

    rows = await db.movies_by_country(country, offset=page - 1, limit=1)
    target = callback.message

    if not rows:
        await target.delete()
        await target.answer(i18n.get("no-movies-in-category"))
        return

    movie = rows[0]
    like_count = await db.count_likes(movie["code"])
    caption = i18n.get(
        "movie-card",
        title=movie["title"],
        country=i18n.get(f"country-{movie['country']}"),
        genre=i18n.get(f"genre-{movie['genre']}"),
        year=movie["year"],
        rating=movie["rating"],
        description=movie["description"],
    )
    keyboard = movie_browse_keyboard("country", country, movie["code"], like_count, page, pages, i18n)
    await target.delete()
    await target.answer_video(video=movie["file_id"], caption=caption, reply_markup=keyboard)


@router.callback_query(CountrySelectCallback.filter())
async def select_country(
    callback: CallbackQuery, callback_data: CountrySelectCallback, db: Database, i18n: TranslatorRunner
) -> None:
    await callback.answer()
    await _show_movie_at(callback, db, i18n, callback_data.key, callback_data.page)


@router.callback_query(MoviesPageCallback.filter(F.scope == "country"))
async def paginate_country_movies(
    callback: CallbackQuery, callback_data: MoviesPageCallback, db: Database, i18n: TranslatorRunner
) -> None:
    await callback.answer()
    await _show_movie_at(callback, db, i18n, callback_data.key, callback_data.page)
