from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from api.routers.admin import (
    NotificationAdminView,
    ScheduleAdminView,
    SenderAdminView,
    TemplateAdminView,
    WrapperAdminView,
)
from core.config import AdminConfig
from providers import BaseProvider


class AdminProvider(BaseProvider):
    def __init__(self, app: FastAPI, settings: AdminConfig, session_maker: async_sessionmaker[AsyncSession]):
        self.app = app
        self.admin = Admin(
            app,
            base_url="/admin",
            session_maker=session_maker,  # type: ignore
            debug=settings.debug,
        )

    async def startup(self):
        """FastAPI startup event"""
        self.admin.add_view(NotificationAdminView)
        self.admin.add_view(TemplateAdminView)
        self.admin.add_view(WrapperAdminView)
        self.admin.add_view(SenderAdminView)
        self.admin.add_view(ScheduleAdminView)

    async def shutdown(self):
        """FastAPI shutdown event"""
        ...
