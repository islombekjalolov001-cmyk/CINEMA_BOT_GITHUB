"""Admin flows for adding, editing and deleting movies (all via FSM)."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from db import Database
from keyboards.inline.admin import (
    admin_confirm_add_keyboard,
    admin_confirm_delete_keyboard,
    admin_country_pick_keyboard,
    admin_edit_fields_keyboard,
    admin_genre_pick_keyboard,
)
from keyboards.inline.callback_data import (
    AdminConfirmCallback,
    AdminCountrySelectCallback,
    AdminEditFieldCallback,
    AdminGenreSelectCallback,
)
from states.states import AddMovie, DeleteMovie, EditMovie

router = Router(name="admin_movie_manage")

ADD_MOVIE_TEXTS = {"➕ Qo'shish", "➕ Добавить", "➕ Add"}
EDIT_MOVIE_TEXTS = {"✏️ Tahrirlash", "✏️ Редактировать", "✏️ Edit"}
DELETE_MOVIE_TEXTS = {"🗑 O'chirish", "🗑 Удалить", "🗑 Delete"}


# ---------------------------------------------------------------- ADD ---- #
@router.message(F.text.in_(ADD_MOVIE_TEXTS))
async def start_add_movie(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.set_state(AddMovie.code)
    await message.answer(i18n.get("admin-ask-code"))


@router.message(AddMovie.code)
async def add_movie_code(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text.isdigit():
        await message.answer(i18n.get("invalid-code"))
        return

    code = int(text)
    if await db.movie_exists(code):
        await message.answer(i18n.get("admin-code-exists"))
        return

    await state.update_data(code=code)
    await state.set_state(AddMovie.title)
    await message.answer(i18n.get("admin-ask-title"))


@router.message(AddMovie.title)
async def add_movie_title(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.update_data(title=(message.text or "").strip())
    await state.set_state(AddMovie.genre)
    await message.answer(i18n.get("admin-ask-genre"), reply_markup=admin_genre_pick_keyboard(i18n))


@router.callback_query(AddMovie.genre, AdminGenreSelectCallback.filter())
async def add_movie_genre(
    callback: CallbackQuery, callback_data: AdminGenreSelectCallback, i18n: TranslatorRunner, state: FSMContext
) -> None:
    await state.update_data(genre=callback_data.key)
    await state.set_state(AddMovie.country)
    await callback.answer()
    await callback.message.edit_text(i18n.get("admin-ask-country"), reply_markup=admin_country_pick_keyboard(i18n))


@router.callback_query(AddMovie.country, AdminCountrySelectCallback.filter())
async def add_movie_country(
    callback: CallbackQuery, callback_data: AdminCountrySelectCallback, i18n: TranslatorRunner, state: FSMContext
) -> None:
    await state.update_data(country=callback_data.key)
    await state.set_state(AddMovie.year)
    await callback.answer()
    await callback.message.edit_text(i18n.get("admin-ask-year"))


@router.message(AddMovie.year)
async def add_movie_year(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text.isdigit():
        await message.answer(i18n.get("invalid-code"))
        return
    await state.update_data(year=int(text))
    await state.set_state(AddMovie.rating)
    await message.answer(i18n.get("admin-ask-rating"))


@router.message(AddMovie.rating)
async def add_movie_rating(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    text = (message.text or "").strip().replace(",", ".")
    try:
        rating = float(text)
    except ValueError:
        await message.answer(i18n.get("invalid-code"))
        return
    await state.update_data(rating=rating)
    await state.set_state(AddMovie.description)
    await message.answer(i18n.get("admin-ask-description"))


@router.message(AddMovie.description)
async def add_movie_description(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.update_data(description=(message.text or "").strip())
    await state.set_state(AddMovie.file)
    await message.answer(i18n.get("admin-ask-file"))


@router.message(AddMovie.file, F.video)
async def add_movie_file(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.update_data(file_id=message.video.file_id)
    data = await state.get_data()
    await state.set_state(AddMovie.confirm)

    caption = i18n.get(
        "movie-card",
        title=data["title"],
        country=i18n.get(f"country-{data['country']}"),
        genre=i18n.get(f"genre-{data['genre']}"),
        year=data["year"],
        rating=data["rating"],
        description=data["description"],
    )
    await message.answer_video(
        video=data["file_id"],
        caption=i18n.get("admin-confirm-add") + "\n\n" + caption,
        reply_markup=admin_confirm_add_keyboard(data["code"], i18n),
    )


@router.callback_query(AddMovie.confirm, AdminConfirmCallback.filter(F.action == "add_movie"))
async def confirm_add_movie(
    callback: CallbackQuery,
    callback_data: AdminConfirmCallback,
    db: Database,
    i18n: TranslatorRunner,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    await state.clear()
    await callback.answer()

    if not callback_data.yes:
        await callback.message.edit_caption(caption=i18n.get("admin-cancelled"))
        return

    await db.add_movie(
        code=data["code"],
        title=data["title"],
        genre=data["genre"],
        country=data["country"],
        year=data["year"],
        rating=data["rating"],
        description=data["description"],
        file_id=data["file_id"],
    )
    await callback.message.edit_caption(caption=i18n.get("admin-movie-added"))


# --------------------------------------------------------------- EDIT ---- #
@router.message(F.text.in_(EDIT_MOVIE_TEXTS))
async def start_edit_movie(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.set_state(EditMovie.choose_field)
    await message.answer(i18n.get("admin-ask-code"))


@router.message(EditMovie.choose_field, F.text.regexp(r"^\d+$"))
async def edit_movie_lookup(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    code = int(message.text.strip())
    movie = await db.get_movie(code)
    if movie is None:
        await message.answer(i18n.get("code-not-found"))
        return

    await state.update_data(edit_code=code)
    await message.answer(i18n.get("admin-choose-field"), reply_markup=admin_edit_fields_keyboard(code, i18n))


@router.callback_query(AdminEditFieldCallback.filter())
async def choose_edit_field(
    callback: CallbackQuery, callback_data: AdminEditFieldCallback, i18n: TranslatorRunner, state: FSMContext
) -> None:
    await callback.answer()

    if callback_data.field == "genre":
        await state.update_data(edit_code=callback_data.code, edit_field="genre")
        await state.set_state(EditMovie.new_value)
        await callback.message.edit_text(i18n.get("admin-ask-genre"), reply_markup=admin_genre_pick_keyboard(i18n))
        return

    if callback_data.field == "country":
        await state.update_data(edit_code=callback_data.code, edit_field="country")
        await state.set_state(EditMovie.new_value)
        await callback.message.edit_text(i18n.get("admin-ask-country"), reply_markup=admin_country_pick_keyboard(i18n))
        return

    await state.update_data(edit_code=callback_data.code, edit_field=callback_data.field)
    await state.set_state(EditMovie.new_value)

    prompts = {
        "title": "admin-ask-title",
        "year": "admin-ask-year",
        "rating": "admin-ask-rating",
        "description": "admin-ask-description",
        "file": "admin-ask-file",
    }
    await callback.message.edit_text(i18n.get(prompts[callback_data.field]))


@router.callback_query(EditMovie.new_value, AdminGenreSelectCallback.filter())
async def edit_movie_genre_value(
    callback: CallbackQuery, callback_data: AdminGenreSelectCallback, db: Database, i18n: TranslatorRunner, state: FSMContext
) -> None:
    data = await state.get_data()
    await db.update_movie_field(data["edit_code"], "genre", callback_data.key)
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(i18n.get("admin-movie-updated"))


@router.callback_query(EditMovie.new_value, AdminCountrySelectCallback.filter())
async def edit_movie_country_value(
    callback: CallbackQuery, callback_data: AdminCountrySelectCallback, db: Database, i18n: TranslatorRunner, state: FSMContext
) -> None:
    data = await state.get_data()
    await db.update_movie_field(data["edit_code"], "country", callback_data.key)
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(i18n.get("admin-movie-updated"))


@router.message(EditMovie.new_value, F.video)
async def edit_movie_file_value(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    data = await state.get_data()
    if data.get("edit_field") != "file":
        return
    await db.update_movie_field(data["edit_code"], "file_id", message.video.file_id)
    await state.clear()
    await message.answer(i18n.get("admin-movie-updated"))


@router.message(EditMovie.new_value)
async def edit_movie_text_value(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    data = await state.get_data()
    field = data.get("edit_field")
    if field in (None, "genre", "country", "file"):
        return

    value: object = (message.text or "").strip()
    if field == "year":
        if not str(value).isdigit():
            await message.answer(i18n.get("invalid-code"))
            return
        value = int(value)
    elif field == "rating":
        try:
            value = float(str(value).replace(",", "."))
        except ValueError:
            await message.answer(i18n.get("invalid-code"))
            return

    db_field = "file_id" if field == "file" else field
    await db.update_movie_field(data["edit_code"], db_field, value)
    await state.clear()
    await message.answer(i18n.get("admin-movie-updated"))


# ------------------------------------------------------------- DELETE ---- #
@router.message(F.text.in_(DELETE_MOVIE_TEXTS))
async def start_delete_movie(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.set_state(DeleteMovie.confirm)
    await message.answer(i18n.get("admin-ask-code"))


@router.message(DeleteMovie.confirm, F.text.regexp(r"^\d+$"))
async def delete_movie_lookup(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    code = int(message.text.strip())
    movie = await db.get_movie(code)
    if movie is None:
        await message.answer(i18n.get("code-not-found"))
        return

    await message.answer(
        i18n.get("admin-confirm-delete", title=movie["title"], code=code),
        reply_markup=admin_confirm_delete_keyboard(code, i18n),
    )


@router.callback_query(AdminConfirmCallback.filter(F.action.in_(("delete_movie", "ask_delete"))))
async def confirm_delete_movie(
    callback: CallbackQuery, callback_data: AdminConfirmCallback, db: Database, i18n: TranslatorRunner, state: FSMContext
) -> None:
    await state.clear()
    await callback.answer()
    code = int(callback_data.value)

    if callback_data.action == "ask_delete":
        movie = await db.get_movie(code)
        if movie is None:
            await callback.message.edit_text(i18n.get("code-not-found"))
            return
        await callback.message.edit_text(
            i18n.get("admin-confirm-delete", title=movie["title"], code=code),
            reply_markup=admin_confirm_delete_keyboard(code, i18n),
        )
        return

    if not callback_data.yes:
        await callback.message.edit_text(i18n.get("admin-cancelled"))
        return

    await db.delete_movie(code)
    await callback.message.edit_text(i18n.get("admin-movie-deleted"))
