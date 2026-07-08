"""Browse movies by genre: pick a genre, then page through matching movies."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from config import PAGE_SIZE
from db import Database
from keyboards.inline.callback_data import GenrePageCallback, GenreSelectCallback, MainMenuBackCallback, MoviesPageCallback
from keyboards.inline.genre_country import genre_keyboard
from keyboards.inline.movie import movie_browse_keyboard
from keyboards.reply.user import main_menu_keyboard
from utils.pagination import clamp_page, offset_for_page, total_pages

router = Router(name="user_genre")

MENU_TEXTS = {"🎭 Janr bo'yicha qidirish", "🎭 Поиск по жанру", "🎭 Search by genre"}


@router.message(F.text.in_(MENU_TEXTS))
async def open_genre_menu(message: Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.get("choose-genre"), reply_markup=genre_keyboard(1, i18n))


@router.callback_query(MainMenuBackCallback.filter())
async def back_from_genre_menu(callback: CallbackQuery, i18n: TranslatorRunner) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        i18n.get("start-greeting", name=callback.from_user.full_name),
        reply_markup=main_menu_keyboard(i18n),
    )


@router.callback_query(GenrePageCallback.filter())
async def paginate_genres(callback: CallbackQuery, callback_data: GenrePageCallback, i18n: TranslatorRunner) -> None:
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=genre_keyboard(callback_data.page, i18n))


async def _show_movie_at(message_or_cb, db: Database, i18n: TranslatorRunner, genre: str, page: int, edit: bool) -> None:
    total = await db.count_movies_by_genre(genre)
    pages = total_pages(total, 1)  # browsing one movie per "page"
    page = clamp_page(page, pages)

    rows = await db.movies_by_genre(genre, offset=page - 1, limit=1)
    target = message_or_cb.message if isinstance(message_or_cb, CallbackQuery) else message_or_cb

    if not rows:
        text = i18n.get("no-movies-in-category")
        if edit:
            await target.delete()
            await target.answer(text)
        else:
            await target.answer(text)
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
    keyboard = movie_browse_keyboard("genre", genre, movie["code"], like_count, page, pages, i18n)

    if edit:
        await target.delete()
    await target.answer_video(video=movie["file_id"], caption=caption, reply_markup=keyboard)


@router.callback_query(GenreSelectCallback.filter())
async def select_genre(callback: CallbackQuery, callback_data: GenreSelectCallback, db: Database, i18n: TranslatorRunner) -> None:
    await callback.answer()
    await _show_movie_at(callback, db, i18n, callback_data.key, callback_data.page, edit=True)


@router.callback_query(MoviesPageCallback.filter(F.scope == "genre"))
async def paginate_genre_movies(
    callback: CallbackQuery, callback_data: MoviesPageCallback, db: Database, i18n: TranslatorRunner
) -> None:
    await callback.answer()
    await _show_movie_at(callback, db, i18n, callback_data.key, callback_data.page, edit=True)
