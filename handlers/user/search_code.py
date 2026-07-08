"""Search for a movie by its numeric code."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluentogram import TranslatorRunner

from db import Database
from keyboards.inline.movie import movie_card_keyboard
from keyboards.reply.user import main_menu_keyboard, search_back_keyboard
from states.states import SearchByCode

router = Router(name="user_search_code")

MENU_TEXTS = {"🔍 Kod orqali qidirish", "🔍 Поиск по коду", "🔍 Search by code"}


@router.message(F.text.in_(MENU_TEXTS))
async def start_code_search(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.set_state(SearchByCode.waiting_code)
    await message.answer(i18n.get("ask-code"), reply_markup=search_back_keyboard(i18n))


@router.message(F.text.func(lambda t: t in ("⬅️ Orqaga", "⬅️ Назад", "⬅️ Back")))
async def back_from_code_search(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        i18n.get("start-greeting", name=message.from_user.full_name),
        reply_markup=main_menu_keyboard(i18n),
    )


@router.message(SearchByCode.waiting_code)
async def process_code_search(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text.isdigit():
        await message.answer(i18n.get("invalid-code"))
        return

    code = int(text)
    movie = await db.get_movie(code)
    await state.clear()

    if movie is None:
        await message.answer(i18n.get("code-not-found"))
        return

    await send_movie_card(message, db, movie, i18n)


async def send_movie_card(message: Message, db: Database, movie, i18n: TranslatorRunner) -> None:
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
    await message.answer_video(
        video=movie["file_id"],
        caption=caption,
        reply_markup=movie_card_keyboard(movie["code"], like_count, i18n),
    )
