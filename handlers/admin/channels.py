"""Admin flows for managing mandatory and optional subscription channels."""
from __future__ import annotations

from urllib.parse import urlparse

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluentogram import TranslatorRunner

from db import Database
from states.states import AddChannel, RemoveChannel

router = Router(name="admin_channels")

ADD_MANDATORY_TEXTS = {"➕ Majburiy kanal qo'shish", "➕ Добавить обязательный канал", "➕ Add mandatory channel"}
REMOVE_MANDATORY_TEXTS = {"➖ Majburiy kanal o'chirish", "➖ Удалить обязательный канал", "➖ Remove mandatory channel"}
ADD_OPTIONAL_TEXTS = {
    "➕ Majburiy bo'lmagan kanal qo'shish", "➕ Добавить необязательный канал", "➕ Add optional channel"
}
REMOVE_OPTIONAL_TEXTS = {
    "➖ Majburiy bo'lmagan kanal o'chirish", "➖ Удалить необязательный канал", "➖ Remove optional channel"
}


def _normalize_channel_reference(raw: str) -> str:
    value = (raw or "").strip()
    if not value:
        return value

    if value.startswith(("http://", "https://")):
        parsed = urlparse(value)
        host = parsed.netloc.lower().replace("www.", "")
        if host in {"t.me", "telegram.me"}:
            path = parsed.path.lstrip("/")
            if path.startswith("joinchat/"):
                return path
            return f"@{path.lstrip('@')}" if path and not path.startswith("@") else path
        return value

    if value.startswith("@"):
        return value
    return value


@router.message(F.text.in_(ADD_MANDATORY_TEXTS))
async def start_add_mandatory(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.update_data(mandatory=True)
    await state.set_state(AddChannel.waiting_chat_id)
    await message.answer(i18n.get("admin-ask-channel-id"))


@router.message(F.text.in_(ADD_OPTIONAL_TEXTS))
async def start_add_optional(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    await state.update_data(mandatory=False)
    await state.set_state(AddChannel.waiting_chat_id)
    await message.answer(i18n.get("admin-ask-channel-id"))


@router.message(AddChannel.waiting_chat_id)
async def add_channel_id(message: Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    normalized = _normalize_channel_reference(message.text or "")
    await state.update_data(chat_id=normalized)
    await state.set_state(AddChannel.waiting_title)
    await message.answer(i18n.get("admin-ask-channel-title"))


@router.message(AddChannel.waiting_title)
async def add_channel_title(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    data = await state.get_data()
    await db.add_channel(data["chat_id"], (message.text or "").strip(), data["mandatory"])
    await state.clear()
    await message.answer(i18n.get("admin-channel-added"))


@router.message(F.text.in_(REMOVE_MANDATORY_TEXTS) | F.text.in_(REMOVE_OPTIONAL_TEXTS))
async def start_remove_channel(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    channels = await db.all_channels()
    if not channels:
        await message.answer(i18n.get("admin-no-channels"))
        return

    listing = "\n".join(f"{row['chat_id']} — {row['title'] or ''}" for row in channels)
    await state.set_state(RemoveChannel.waiting_chat_id)
    await message.answer(f"{i18n.get('admin-ask-channel-id')}\n\n{listing}")


@router.message(RemoveChannel.waiting_chat_id)
async def remove_channel(message: Message, db: Database, i18n: TranslatorRunner, state: FSMContext) -> None:
    await db.remove_channel((message.text or "").strip())
    await state.clear()
    await message.answer(i18n.get("admin-channel-removed"))
