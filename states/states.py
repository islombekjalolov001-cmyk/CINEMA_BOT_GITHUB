"""All FSM state groups used across the bot."""
from aiogram.fsm.state import State, StatesGroup


class SearchByCode(StatesGroup):
    waiting_code = State()


class SearchByName(StatesGroup):
    waiting_name = State()


class RequestMovie(StatesGroup):
    waiting_movie_name = State()


class AddMovie(StatesGroup):
    code = State()
    title = State()
    genre = State()
    country = State()
    year = State()
    rating = State()
    description = State()
    file = State()
    confirm = State()


class EditMovie(StatesGroup):
    choose_field = State()
    new_value = State()


class DeleteMovie(StatesGroup):
    confirm = State()


class AddChannel(StatesGroup):
    waiting_chat_id = State()
    waiting_title = State()


class RemoveChannel(StatesGroup):
    waiting_chat_id = State()


class Broadcast(StatesGroup):
    waiting_content = State()
    confirm = State()


class AdminUserManage(StatesGroup):
    waiting_block_target = State()
    confirm_block = State()
    waiting_unblock_target = State()
    confirm_unblock = State()
