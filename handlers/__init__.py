"""Top-level handlers package: combines admin and user routers."""
from aiogram import Router

from .admin import admin_router
from .user import user_router

main_router = Router(name="main_root")
main_router.include_router(admin_router)
main_router.include_router(user_router)

__all__ = ["main_router"]
