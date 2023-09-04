from .base import BaseSchema


class TemplateSchema(BaseSchema):
    name: str
    description: str
    subject: str
    body: str
    json_vars: dict | None
    wrapper: 'WrapperSchema'
    sender: 'SenderSchema'


class WrapperSchema(BaseSchema):
    name: str
    body: str


class SenderSchema(BaseSchema):
    name: str
    description: str
