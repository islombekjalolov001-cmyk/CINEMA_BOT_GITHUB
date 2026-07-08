"""/admin command and top-level admin menu navigation."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from db import Database
from keyboards.inline.callback_data import AdminConfirmCallback
from keyboards.reply.admin import admin_channels_menu_keyboard, admin_menu_keyboard, admin_movies_menu_keyboard

router = Router(name="admin_panel")

ADMIN_BACK_TEXTS = {"⬅️ Admin menyu", "⬅️ Меню админа", "⬅️ Admin menu"}
GLOBAL_BACK_TEXTS = {"⬅️ Orqaga", "⬅️ Назад", "⬅️ Back"}
MOVIES_TEXTS = {"🎬 Kinolar", "🎬 Фильмы", "🎬 Movies"}
CHANNELS_TEXTS = {"📡 Kanallar", "📡 Каналы", "📡 Channels"}
BLOCK_USER_TEXTS = {"🚫 Foydalanuvchini bloklash", "🚫 Заблокировать пользователя", "🚫 Block user"}
BLOCKED_USERS_TEXTS = {"🚫 Bloklangan foydalanuvchilar", "🚫 Заблокированные пользователи", "🚫 Blocked users"}

from states.states import AdminUserManage


def normalize_user_identifier(text: str) -> str:
    return (text or "").strip().lstrip("@").strip()


def format_user_reference(user) -> str:
    username = user["username"] or "-"
    nickname = user["full_name"] or "-"
    return f"• ID: {user['user_id']} | Username: @{username} | Nickname: {nickname}"


def _prepare_block_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.get("admin-block-user-inline"),
        callback_data=AdminConfirmCallback(action="prepare_block_user", value="0", yes=False),
    )
    return builder.as_markup()


def _prepare_unblock_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.get("admin-unblock-user-inline"),
        callback_data=AdminConfirmCallback(action="prepare_unblock_user", value="0", yes=False),
    )
    return builder.as_markup()


def _confirm_action_keyboard(i18n: TranslatorRunner, action: str, value: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.get("admin-yes"),
        callback_data=AdminConfirmCallback(action=action, value=value, yes=True),
    )
    builder.button(
        text=i18n.get("admin-no"),
        callback_data=AdminConfirmCallback(action=action, value=value, yes=False),
    )
    return builder.as_markup()


async def _send_user_list(message: Message, db: Database, i18n: TranslatorRunner, blocked: bool) -> None:
    users = await db.get_users_by_status(blocked=blocked)
    title = i18n.get("admin-blocked-users-title") if blocked else i18n.get("admin-all-users-title")
    lines = [title]
    if users:
        lines.extend(format_user_reference(user) for user in users)
    else:
        lines.append(i18n.get("admin-no-users"))

    keyboard = _prepare_unblock_keyboard(i18n) if blocked else _prepare_block_keyboard(i18n)
    await message.answer("\n\n".join(lines), reply_markup=keyboard)


@router.message(Command("admin"))
async def cmd_admin(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.clear()
    await message.answer(i18n.get("admin-panel-title"), reply_markup=admin_menu_keyboard(i18n))


@router.message(F.text.in_(MOVIES_TEXTS))
async def open_movies_menu(message: Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.get("admin-movies"), reply_markup=admin_movies_menu_keyboard(i18n))


@router.message(F.text.in_(CHANNELS_TEXTS))
async def open_channels_menu(message: Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.get("admin-channels"), reply_markup=admin_channels_menu_keyboard(i18n))


@router.message(F.text.in_(BLOCK_USER_TEXTS))
async def start_block_user(message: Message, db: Database, i18n: TranslatorRunner) -> None:
    await _send_user_list(message, db, i18n, blocked=False)


@router.message(F.text.in_(BLOCKED_USERS_TEXTS))
async def list_blocked_users(message: Message, db: Database, i18n: TranslatorRunner) -> None:
    await _send_user_list(message, db, i18n, blocked=True)


@router.callback_query(AdminConfirmCallback.filter(F.action == "prepare_block_user"))
async def prepare_block_user(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    state: FSMContext,
) -> None:
    await callback.answer()
    await state.set_state(AdminUserManage.waiting_block_target)
    await state.update_data(user_manage_action="block")
    await callback.message.answer(i18n.get("admin-ask-user-id-or-username"))


@router.callback_query(AdminConfirmCallback.filter(F.action == "prepare_unblock_user"))
async def prepare_unblock_user(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    state: FSMContext,
) -> None:
    await callback.answer()
    await state.set_state(AdminUserManage.waiting_unblock_target)
    await state.update_data(user_manage_action="unblock")
    await callback.message.answer(i18n.get("admin-ask-user-id-or-username-unblock"))


@router.message(AdminUserManage.waiting_block_target)
async def receive_block_target(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    identifier = normalize_user_identifier(message.text or "")
    if not identifier:
        await message.answer(i18n.get("admin-invalid-user-target"))
        return

    user = await db.find_user_by_identifier(identifier)
    if user is None:
        await message.answer(i18n.get("admin-user-not-found"))
        return

    if bool(user["is_blocked"]):
        await message.answer(i18n.get("admin-user-already-blocked"))
        await state.clear()
        return

    await state.update_data(target_user_id=user["user_id"])
    await state.set_state(AdminUserManage.confirm_block)
    await message.answer(
        i18n.get(
            "admin-confirm-block-user",
            user_id=user["user_id"],
            username=user["username"] or "-",
            nickname=user["full_name"] or "-",
        ),
        reply_markup=_confirm_action_keyboard(i18n, "confirm_block_user", str(user["user_id"])),
    )


@router.message(AdminUserManage.waiting_unblock_target)
async def receive_unblock_target(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    identifier = normalize_user_identifier(message.text or "")
    if not identifier:
        await message.answer(i18n.get("admin-invalid-user-target"))
        return

    user = await db.find_user_by_identifier(identifier)
    if user is None:
        await message.answer(i18n.get("admin-user-not-found"))
        return

    if not bool(user["is_blocked"]):
        await message.answer(i18n.get("admin-user-not-blocked"))
        await state.clear()
        return

    await state.update_data(target_user_id=user["user_id"])
    await state.set_state(AdminUserManage.confirm_unblock)
    await message.answer(
        i18n.get(
            "admin-confirm-unblock-user",
            user_id=user["user_id"],
            username=user["username"] or "-",
            nickname=user["full_name"] or "-",
        ),
        reply_markup=_confirm_action_keyboard(i18n, "confirm_unblock_user", str(user["user_id"])),
    )


@router.callback_query(AdminUserManage.confirm_block, AdminConfirmCallback.filter())
async def confirm_block_user(
    callback: CallbackQuery,
    callback_data: AdminConfirmCallback,
    db: Database,
    i18n: TranslatorRunner,
    state: FSMContext,
) -> None:
    await callback.answer()
    if not callback_data.yes:
        await state.clear()
        await callback.message.edit_text(i18n.get("admin-cancelled"))
        return

    target_user_id = int(callback_data.value)
    await db.set_blocked(target_user_id, True)
    await state.clear()
    await callback.message.edit_text(i18n.get("admin-user-blocked", user_id=target_user_id))


@router.callback_query(AdminUserManage.confirm_unblock, AdminConfirmCallback.filter())
async def confirm_unblock_user(
    callback: CallbackQuery,
    callback_data: AdminConfirmCallback,
    db: Database,
    i18n: TranslatorRunner,
    state: FSMContext,
) -> None:
    await callback.answer()
    if not callback_data.yes:
        await state.clear()
        await callback.message.edit_text(i18n.get("admin-cancelled"))
        return

    target_user_id = int(callback_data.value)
    await db.set_blocked(target_user_id, False)
    await state.clear()
    await callback.message.edit_text(i18n.get("admin-user-unblocked", user_id=target_user_id))


@router.message(F.text.in_(ADMIN_BACK_TEXTS))
async def back_to_admin_root(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.clear()
    await message.answer(i18n.get("admin-panel-title"), reply_markup=admin_menu_keyboard(i18n))
