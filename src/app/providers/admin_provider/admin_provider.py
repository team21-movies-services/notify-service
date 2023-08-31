from fastapi import FastAPI
from sqladmin import Admin

from providers import BaseProvider
from core.config import AdminConfig
from providers.admin_provider.views import NotificationAdminView


class AdminProvider(BaseProvider):
    def __init__(self, app: FastAPI, settings: AdminConfig):
        self.app = app
        self.admin = Admin(app, base_url="/api/v1/admin", debug=settings.debug)

    async def startup(self):
        """FastAPI startup event"""
        setattr(self.app.state, "admin", self.admin)
        self.admin.add_view(NotificationAdminView)

    async def shutdown(self):
        """FastAPI shutdown event"""
        ...
