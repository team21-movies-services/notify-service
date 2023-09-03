from abc import ABC, abstractmethod
from uuid import UUID

from jinja2 import DictLoader, Environment, meta

from shared.database.repositories.templates import TemplatesRepositoryProtocol


class TemplatesServiceABC(ABC):
    @abstractmethod
    async def render_template(self, template_id: UUID) -> str:
        raise NotImplementedError


class TemplatesService(TemplatesServiceABC):
    def __init__(self, template_repository: TemplatesRepositoryProtocol) -> None:
        self.__template_repository = template_repository

    async def render_template(self, template_id: UUID) -> str:
        template = await self.__template_repository.get(template_id)

        tmp_loader = DictLoader({"body": template.body})
        tmp_env = Environment(loader=tmp_loader, autoescape=True)

        tmp_variables = template.json_vars
        if not tmp_variables:
            # Парсим переменные шаблона, чтобы отобразить их в примере
            parsed_content = tmp_env.parse(template.body)
            variables = meta.find_undeclared_variables(parsed_content)
            tmp_variables = {key: "{{ " + str(key) + " }}" for key in variables}

        template = tmp_env.from_string(template.wrapper.body)
        rendered_template = template.render(**tmp_variables)

        return rendered_template
