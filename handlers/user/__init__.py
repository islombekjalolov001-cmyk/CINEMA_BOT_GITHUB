"""Aggregates every user-facing router into a single Router for loader.py."""
from aiogram import Router

from . import country, genre, like, search_code, search_name, settings, start

user_router = Router(name="user_root")
user_router.include_router(start.router)
user_router.include_router(search_code.router)
user_router.include_router(search_name.router)
user_router.include_router(genre.router)
user_router.include_router(country.router)
user_router.include_router(settings.router)
user_router.include_router(like.router)

__all__ = ["user_router"]
