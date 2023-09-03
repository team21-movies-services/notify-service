from fastapi import Request
from fastapi.responses import RedirectResponse
from shared.database.models.template import Template
from sqladmin import ModelView, action


class TemplateAdminView(ModelView, model=Template):  # type: ignore
    column_list = [
        Template.id,
        Template.name,
        Template.subject,
        Template.description,
        Template.wrapper_id,
        Template.sender_id,
    ]

    @action(
        name="show_template",
        label="Show template",
        add_in_detail=True,
    )
    async def show_template(self, request: Request):
        template_id = request.query_params.get("pks")

        if not template_id:
            referer = request.headers["Referer"]
            return RedirectResponse(referer)

        return RedirectResponse(str(request.base_url) + f"api/v1/templates/{template_id}/show")
