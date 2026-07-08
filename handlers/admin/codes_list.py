"""📋 Barcha kino kodlari — paginated list of every movie code + title."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from config import PAGE_SIZE
from db import Database
from keyboards.inline.admin import admin_code_item_actions_keyboard, admin_codes_list_keyboard, admin_edit_fields_keyboard
from keyboards.inline.callback_data import AdminCodeItemCallback, AdminCodesPageCallback, AdminConfirmCallback, AdminEditFieldCallback
from states.states import EditMovie
from utils.pagination import offset_for_page

router = Router(name="admin_codes_list")

ALL_CODES_TEXTS = {"📋 Barcha kino kodlari", "📋 Все коды фильмов", "📋 All movie codes"}


async def _render_page(target_answer, db: Database, i18n: TranslatorRunner, page: int, edit: bool) -> None:
    total = await db.count_movies_total()
    offset = offset_for_page(page, PAGE_SIZE)
    movies = await db.all_movies_paginated(offset, PAGE_SIZE)
    keyboard = admin_codes_list_keyboard(movies, page, total, i18n)

    if edit:
        await target_answer(i18n.get("admin-all-codes-title"), reply_markup=keyboard)
    else:
        await target_answer(i18n.get("admin-all-codes-title"), reply_markup=keyboard)


@router.message(F.text.in_(ALL_CODES_TEXTS))
async def open_codes_list(message: Message, db: Database, i18n: TranslatorRunner) -> None:
    await _render_page(message.answer, db, i18n, page=1, edit=False)


@router.callback_query(AdminCodesPageCallback.filter())
async def paginate_codes_list(
    callback: CallbackQuery, callback_data: AdminCodesPageCallback, db: Database, i18n: TranslatorRunner
) -> None:
    await callback.answer()
    await _render_page(callback.message.edit_text, db, i18n, callback_data.page, edit=True)


@router.callback_query(AdminCodeItemCallback.filter())
async def open_code_item(
    callback: CallbackQuery, callback_data: AdminCodeItemCallback, db: Database, i18n: TranslatorRunner
) -> None:
    await callback.answer()
    movie = await db.get_movie(callback_data.code)
    if movie is None:
        await callback.message.edit_text(i18n.get("code-not-found"))
        return

    await callback.message.edit_text(
        i18n.get("admin-code-item", code=movie["code"], title=movie["title"]),
        reply_markup=admin_code_item_actions_keyboard(movie["code"], i18n),
    )


@router.callback_query(AdminEditFieldCallback.filter(F.field == "_menu"))
async def open_edit_from_codes_list(
    callback: CallbackQuery, callback_data: AdminEditFieldCallback, i18n: TranslatorRunner, state: FSMContext
) -> None:
    await callback.answer()
    await state.update_data(edit_code=callback_data.code)
    await state.set_state(EditMovie.choose_field)
    await callback.message.edit_text(
        i18n.get("admin-choose-field"), reply_markup=admin_edit_fields_keyboard(callback_data.code, i18n)
    )
