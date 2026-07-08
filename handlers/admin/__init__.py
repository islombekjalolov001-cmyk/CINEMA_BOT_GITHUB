"""Aggregates every admin router into one Router, gated by AdminFilter."""
from aiogram import Router

from filters import AdminFilter

from . import broadcast, channels, codes_list, export, movie_manage, panel, stats

admin_router = Router(name="admin_root")
admin_router.message.filter(AdminFilter())
admin_router.callback_query.filter(AdminFilter())

admin_router.include_router(panel.router)
admin_router.include_router(movie_manage.router)
admin_router.include_router(channels.router)
admin_router.include_router(broadcast.router)
admin_router.include_router(stats.router)
admin_router.include_router(export.router)
admin_router.include_router(codes_list.router)

__all__ = ["admin_router"]
