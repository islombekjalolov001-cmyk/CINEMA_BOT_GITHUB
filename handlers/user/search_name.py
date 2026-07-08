"""Search for movies by (partial) name, then browse results one by one."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from db import Database
from keyboards.inline.callback_data import NameSearchPageCallback
from keyboards.inline.movie import movie_browse_keyboard
from keyboards.reply.user import main_menu_keyboard, search_back_keyboard
from states.states import SearchByName

router = Router(name="user_search_name")

MENU_TEXTS = {"🎬 Kino nomi orqali qidirish", "🎬 Поиск по названию", "🎬 Search by movie name"}


@router.message(F.text.in_(MENU_TEXTS))
async def start_name_search(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.set_state(SearchByName.waiting_name)
    await message.answer(i18n.get("ask-name"), reply_markup=search_back_keyboard(i18n))


async def _render_result(
    target_answer, db: Database, i18n: TranslatorRunner, codes: list[int], page: int
) -> None:
    pages = len(codes)
    code = codes[page - 1]
    movie = await db.get_movie(code)
    like_count = await db.count_likes(code)

    caption = i18n.get(
        "movie-card",
        title=movie["title"],
        country=i18n.get(f"country-{movie['country']}"),
        genre=i18n.get(f"genre-{movie['genre']}"),
        year=movie["year"],
        rating=movie["rating"],
        description=movie["description"],
    )
    keyboard = movie_browse_keyboard("name", "-", code, like_count, page, pages, i18n)
    await target_answer(video=movie["file_id"], caption=caption, reply_markup=keyboard)


@router.message(F.text.func(lambda t: t in ("⬅️ Orqaga", "⬅️ Назад", "⬅️ Back")))
async def back_from_name_search(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        i18n.get("start-greeting", name=message.from_user.full_name),
        reply_markup=main_menu_keyboard(i18n),
    )


@router.message(SearchByName.waiting_name)
async def process_name_search(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    query = (message.text or "").strip()
    results = await db.search_movies_by_name(query)
    await state.clear()

    if not results:
        await message.answer(i18n.get("name-not-found"))
        return

    codes = [row["code"] for row in results]
    await state.update_data(name_search_codes=codes)

    await message.answer(i18n.get("name-results"))
    await _render_result(message.answer_video, db, i18n, codes, page=1)


@router.callback_query(NameSearchPageCallback.filter())
async def paginate_name_search(
    callback: CallbackQuery,
    callback_data: NameSearchPageCallback,
    db: Database,
    i18n: TranslatorRunner,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    codes = data.get("name_search_codes")
    if not codes:
        await callback.answer(i18n.get("error-generic"), show_alert=True)
        return

    await callback.answer()
    await callback.message.delete()
    await _render_result(callback.message.answer_video, db, i18n, codes, callback_data.page)
