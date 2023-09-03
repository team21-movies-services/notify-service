from __future__ import annotations

from dataclasses import dataclass
from shared.dto import base

from shared.database.models import Template, Wrapper, Sender


@dataclass
class WrapperDto(base.Dto):
    name: str
    body: str

    @classmethod
    def from_model(cls, wrapper_model: Wrapper) -> WrapperDto:
        return cls(
            name=wrapper_model.name,
            body=wrapper_model.body,
        )


@dataclass
class SenderDto(base.Dto):
    name: str
    description: str

    @classmethod
    def from_model(cls, sender_model: Sender) -> SenderDto:
        return cls(
            name=sender_model.name,
            description=sender_model.description,
        )


@dataclass
class TemplateDto(base.Dto):
    name: str
    description: str
    subject: str
    body: str
    json_vars: dict | None
    wrapper: WrapperDto
    sender: SenderDto

    @classmethod
    def from_model(cls, template_model: Template) -> TemplateDto:
        wrapper = WrapperDto.from_model(template_model.wrapper)
        sender = SenderDto.from_model(template_model.sender)
        return cls(
            name=template_model.name,
            description=template_model.description,
            subject=template_model.subject,
            body=template_model.body,
            json_vars=template_model.json_vars,
            wrapper=wrapper,
            sender=sender,
        )
