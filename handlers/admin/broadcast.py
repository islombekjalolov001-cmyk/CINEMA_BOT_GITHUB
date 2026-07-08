"""📣 Broadcast a message to every bot user, with live progress."""
from __future__ import annotations

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from keyboards.inline.callback_data import BroadcastConfirmCallback
from services.broadcast_service import broadcast_message
from states.states import Broadcast

router = Router(name="admin_broadcast")

BROADCAST_TEXTS = {"📣 Broadcast"}


def _confirm_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.get("admin-broadcast-yes"), callback_data=BroadcastConfirmCallback(yes=True))
    builder.button(text=i18n.get("admin-broadcast-no"), callback_data=BroadcastConfirmCallback(yes=False))
    return builder.as_markup()


@router.message(F.text.in_(BROADCAST_TEXTS))
async def start_broadcast(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.set_state(Broadcast.waiting_content)
    await message.answer(i18n.get("admin-ask-broadcast"))


@router.message(Broadcast.waiting_content)
async def receive_broadcast_content(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    # Stored as-is (MemoryStorage keeps plain Python objects, no serialization needed).
    await state.update_data(source_message=message)
    await state.set_state(Broadcast.confirm)
    await message.answer(i18n.get("admin-broadcast-confirm"), reply_markup=_confirm_keyboard(i18n))


@router.callback_query(Broadcast.confirm, BroadcastConfirmCallback.filter())
async def confirm_broadcast(
    callback: CallbackQuery,
    callback_data: BroadcastConfirmCallback,
    bot: Bot,
    i18n: TranslatorRunner,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    await state.clear()
    await callback.answer()

    if not callback_data.yes:
        await callback.message.edit_text(i18n.get("admin-cancelled"))
        return

    source_message: Message = data["source_message"]

    await callback.message.edit_text(i18n.get("admin-broadcast-started"))
    status_message = await callback.message.answer(i18n.get("admin-broadcast-progress", sent=0, total="?"))

    async def progress(sent: int, total: int) -> None:
        try:
            await status_message.edit_text(i18n.get("admin-broadcast-progress", sent=sent, total=total))
        except Exception:
            pass

    result = await broadcast_message(bot, source_message, progress_callback=progress)

    await status_message.edit_text(
        i18n.get("admin-broadcast-done", sent=result.sent, failed=result.failed, blocked=result.blocked)
    )
