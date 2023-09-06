import logging

from fastapi import Depends, Header

from app.core.exceptions.auth import TokenException, TokenExpiredException
from app.schemas.auth import AuthData
from app.services import AuthServiceABC

logger = logging.getLogger().getChild('auth')


async def get_ws_auth_data(
    auth_service: AuthServiceABC = Depends(),
    access_token: str | None = Header(None, alias="Authorization"),
) -> tuple[AuthData | None, str]:
    if not access_token:
        return None, "UNAUTHORIZED"
    try:
        auth_data: AuthData = await auth_service.validate_access_token(access_token)
    except TokenException:
        return None, "FORBIDDEN"
    except TokenExpiredException:
        return None, "TOKEN EXPIRED"
    return auth_data, "SUCCESS"
