"""Typed CallbackData factories used across inline keyboards."""
from aiogram.filters.callback_data import CallbackData


class LanguageCallback(CallbackData, prefix="lang"):
    code: str


class SubCheckCallback(CallbackData, prefix="subcheck"):
    pass


class GenrePageCallback(CallbackData, prefix="genrepg"):
    page: int


class GenreSelectCallback(CallbackData, prefix="genresel"):
    key: str
    page: int = 1


class CountryPageCallback(CallbackData, prefix="countrypg"):
    page: int


class CountrySelectCallback(CallbackData, prefix="countrysel"):
    key: str
    page: int = 1


class MoviesPageCallback(CallbackData, prefix="moviespg"):
    """Generic pagination for genre/country movie lists and favorites."""

    scope: str  # "genre" | "country" | "favorites"
    key: str    # genre/country key, or "-" for favorites
    page: int


class LikeCallback(CallbackData, prefix="like"):
    code: int


class NameSearchPageCallback(CallbackData, prefix="namepg"):
    page: int


class SettingsCallback(CallbackData, prefix="settings"):
    action: str  # "language" | "favorites" | "requests" | "back"


class MainMenuBackCallback(CallbackData, prefix="mainback"):
    pass


# ---------------------------------------------------------------- admin --- #
class AdminGenreSelectCallback(CallbackData, prefix="admgenre"):
    key: str


class AdminCountrySelectCallback(CallbackData, prefix="admcountry"):
    key: str


class AdminCodesPageCallback(CallbackData, prefix="admcodespg"):
    page: int


class AdminCodeItemCallback(CallbackData, prefix="admcodeitem"):
    code: int


class AdminEditFieldCallback(CallbackData, prefix="admeditfield"):
    code: int
    field: str


class AdminConfirmCallback(CallbackData, prefix="admconfirm"):
    action: str  # "add_movie" | "delete_movie" | "prepare_block_user" | "confirm_block_user" | "confirm_unblock_user"
    value: str   # code or user identifier, as string
    yes: bool


class BroadcastConfirmCallback(CallbackData, prefix="bcconfirm"):
    yes: bool
