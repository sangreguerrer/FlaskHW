import datetime
from aiohttp.web import View
from sqlalchemy import select

from crud import select_one
from models import TOKEN_TTL
from errors import get_http_error
import bcrypt
from models import Token, MODEL
from aiohttp import web


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def check_token(handler):
    async def wrapper(view: View):
        token_uid = view.request.headers.get("Authorization")
        if token_uid is None:
            raise get_http_error(web.HTTPUnauthorized, "No token provided")
        token_query = select(Token).where(
            Token.token == token_uid,
            Token.creation_time >
            datetime.datetime.now() - datetime.timedelta(seconds=TOKEN_TTL)
        )
        token = await select_one(token_query, view.session)
        if token is None:
            raise get_http_error(web.HTTPUnauthorized, "Unauthorized")

        view.request.token = token
        return await handler(view)
    
    return wrapper


def check_user(item: MODEL, user_id: int):
    if item.user_id != user_id:
        raise get_http_error(web.HTTPForbidden, "Access denied")
