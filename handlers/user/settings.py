"""⚙️ Settings menu: language change, favorites list, movie requests."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from config import config
from db import Database
from keyboards.inline.callback_data import MoviesPageCallback, SettingsCallback, LanguageCallback
from keyboards.inline.language import language_keyboard
from keyboards.inline.movie import movie_browse_keyboard
from keyboards.reply.user import main_menu_keyboard
from loader import bot
from states.states import RequestMovie
from utils.pagination import clamp_page, total_pages

router = Router(name="user_settings")

MENU_TEXTS = {"⚙️ Sozlamalar", "⚙️ Настройки", "⚙️ Settings"}


def _settings_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.get("settings-language"), callback_data=SettingsCallback(action="language"))
    builder.button(text=i18n.get("settings-favorites"), callback_data=SettingsCallback(action="favorites"))
    builder.button(text=i18n.get("settings-requests"), callback_data=SettingsCallback(action="requests"))
    builder.button(text=i18n.get("menu-back"), callback_data=SettingsCallback(action="back"))
    builder.adjust(1)
    return builder.as_markup()


@router.message(F.text.in_(MENU_TEXTS))
async def open_settings(message: Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.get("settings-title"), reply_markup=_settings_keyboard(i18n))


@router.message(F.text.func(lambda t: t in ("🎬 Kino so'rash", "🎬 Запросить фильм", "🎬 Request movie")))
async def request_movie(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.set_state(RequestMovie.waiting_movie_name)
    await message.answer(i18n.get("ask-request-name"), reply_markup=main_menu_keyboard(i18n))


@router.callback_query(SettingsCallback.filter(F.action == "language"))
async def open_language(callback: CallbackQuery, i18n: TranslatorRunner) -> None:
    await callback.answer()
    await callback.message.edit_text(i18n.get("language-choose"), reply_markup=language_keyboard(i18n))


@router.callback_query(SettingsCallback.filter(F.action == "back"))
async def back_from_settings(callback: CallbackQuery, i18n: TranslatorRunner) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        i18n.get("start-greeting", name=callback.from_user.full_name),
        reply_markup=main_menu_keyboard(i18n),
    )


@router.callback_query(LanguageCallback.filter())
async def set_language(
    callback: CallbackQuery, callback_data: LanguageCallback, db: Database, i18n: TranslatorRunner
) -> None:
    await db.set_language(callback.from_user.id, callback_data.code)
    # i18n in this scope still reflects the OLD language (resolved before this handler ran),
    # fetch a translator for the NEW language so the confirmation is shown correctly.
    from loader import translator_hub

    new_i18n = translator_hub.get_translator_by_locale(callback_data.code)

    await callback.answer(new_i18n.get("language-changed"))
    await callback.message.delete()
    await callback.message.answer(new_i18n.get("language-changed"), reply_markup=main_menu_keyboard(new_i18n))


@router.callback_query(SettingsCallback.filter(F.action == "favorites"))
async def open_favorites(callback: CallbackQuery, db: Database, i18n: TranslatorRunner) -> None:
    await callback.answer()
    await _show_favorite_at(callback, db, i18n, page=1, edit=True)


async def _show_favorite_at(callback: CallbackQuery, db: Database, i18n: TranslatorRunner, page: int, edit: bool) -> None:
    user_id = callback.from_user.id
    total = await db.count_user_favorites(user_id)

    if total == 0:
        if edit:
            await callback.message.edit_text(i18n.get("favorites-empty"))
        else:
            await callback.message.answer(i18n.get("favorites-empty"))
        return

    pages = total_pages(total, 1)
    page = clamp_page(page, pages)
    rows = await db.user_favorites(user_id, offset=page - 1, limit=1)
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
    keyboard = movie_browse_keyboard("favorites", "-", movie["code"], like_count, page, pages, i18n)

    if edit:
        await callback.message.delete()
    await callback.message.answer_video(video=movie["file_id"], caption=caption, reply_markup=keyboard)


@router.callback_query(MoviesPageCallback.filter(F.scope == "favorites"))
async def paginate_favorites(
    callback: CallbackQuery, callback_data: MoviesPageCallback, db: Database, i18n: TranslatorRunner
) -> None:
    await callback.answer()
    await _show_favorite_at(callback, db, i18n, callback_data.page, edit=True)


@router.callback_query(SettingsCallback.filter(F.action == "requests"))
async def open_requests(callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(RequestMovie.waiting_movie_name)
    await callback.message.edit_text(i18n.get("ask-request-name"))


@router.message(RequestMovie.waiting_movie_name)
async def process_movie_request(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    movie_name = (message.text or "").strip()
    await db.add_request(message.from_user.id, movie_name)
    await state.clear()

    user = message.from_user
    username = user.username or "-"
    full_name = user.full_name or "-"
    admin_ids = config.admin_ids
    for admin_id in admin_ids:
        try:
            await bot.send_message(
                admin_id,
                (
                    f"📩 Yangi kino so'rovi\n"
                    f"👤 Foydalanuvchi: {full_name}\n"
                    f"🆔 ID: {user.id}\n"
                    f"@ Username: @{username}\n"
                    f"🎬 Kino: {movie_name}"
                ),
            )
        except Exception:
            continue

    await message.answer(i18n.get("request-sent"), reply_markup=main_menu_keyboard(i18n))
