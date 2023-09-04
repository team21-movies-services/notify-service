from pydantic import BaseModel, EmailStr

from shared.enums.notifications import NotificationTypesEnum


class UserInfoSchema(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    notifications: list[NotificationTypesEnum]
