from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from errors import Unauthorized
from models import Article, Token, User
from schema import CreateArticle, CreateUser, Login, UpdateUser, UpdateArticle, SCHEMA_MODEL
from auth import check_token, hash_password, check_password, check_user
from crud import get_item_by_id, create_item, update_item, delete_item, select_one
from tools import validate


class BaseView(web.View):
    @property
    def session(self) -> AsyncSession:
        return self.request.session

    @property
    def token(self) -> Token:
        return self.request.token

    @property
    def user(self) -> User:
        return self.request.token.user

    @property
    def is_authorized(self) -> bool:
        return hasattr(self.request, "token")

    async def validated_json(self, schema: SCHEMA_MODEL):
        raw_json = await self.request.json()
        return validate(schema, raw_json)


class UserView(BaseView):
    @check_token
    async def get(self):
        return web.json_response(self.user.dict)
    
    async def post(self):
        payload = await self.validated_json(CreateUser)
        payload["password"] = hash_password(payload["password"])
        user = await create_item(User, payload, self.session)
        return web.json_response({"id": user.id})
    
    @check_token
    async def patch(self):
        payload = await self.validated_json(UpdateUser)
        user = await update_item(self.token.user, payload, self.session)
        return web.json_response({"id": user.id})
    
    @check_token
    async def delete(self):
        await delete_item(self.token.user, self.session)
        return web.json_response({"status": "Ok"})


class LoginView(BaseView):
    async def post(self):
        payload = await self.validated_json(Login)
        query = select(User).where(User.name == payload["name"]).limit(1)
        user = await select_one(query, self.session)
        if not user:
            raise Unauthorized("invalid user or password")
        if check_password(payload["password"], user.password):
            token = await create_item(Token, {"user_id": user.id}, self.session)
            return web.json_response({"token": str(token.token)})
        raise Unauthorized("Invalid user or password")
    

class ArticleView(BaseView):

    @property
    def article_id(self):
        article_id = self.request.match_info.get("article_id", None)
        return int(article_id) if article_id else None

    @check_token
    async def get(self):
        if self.article_id is None:
            return web.json_response([article.dict for article in self.user.articles])
        article = await get_item_by_id(Article, self.article_id, self.session)
        check_user(article, self.token.user_id)
        return web.json_response(article.dict)

    @check_token
    async def post(self):
        payload = await self.validated_json(CreateArticle)
        article = await create_item(Article, dict(user_id=self.token.user_id, **payload), self.session)
        return web.json_response({"id": article.id})
    
    @check_token
    async def patch(self):
        payload = await self.validated_json(UpdateArticle)
        article = await get_item_by_id(Article, self.article_id, self.session)
        check_user(article, self.token.user_id)
        article = await update_item(article, payload, self.session)
        return web.json_response({"id": article.id})
    
    @check_token
    async def delete(self):
        article = await get_item_by_id(Article, self.article_id, self.session)
        check_user(article, self.token.user_id)
        await delete_item(article, self.session)
        return web.json_response({"status": "ok"})
