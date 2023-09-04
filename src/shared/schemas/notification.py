from .base import BaseSchema
from .template import TemplateSchema


class NotificationSchema(BaseSchema):
    event_name: str
    template: TemplateSchema
