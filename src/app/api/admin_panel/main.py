from fastapi import FastAPI
from sqladmin import Admin

from api.admin_panel.v1 import NotificationAdminView
from core.config import AdminConfig


def setup_admin_panel(app: FastAPI, settings: AdminConfig):
    admin = Admin(app, base_url="/api/v1/admin", debug=settings.debug)
    admin.add_view(NotificationAdminView)
