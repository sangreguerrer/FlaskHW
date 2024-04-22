from errors import HttpError
from flask import jsonify, request
from flask.views import MethodView
from models import Article, Token, User
from schema import CreateArticle, CreateUser, Login, UpdateUser, UpdateArticle
from sqlalchemy.orm import Session
from auth import check_token, hash_password, check_password, check_user
from crud import get_item_by_id, add_item, create_item, update_item, delete_item
from tools import validate


class BaseView(MethodView):
    @property
    def session(self) -> Session:
        return request.session

    @property
    def token(self) -> Token:
        return request.token

    @property
    def user(self) -> User:
        return request.token.user


class UserView(BaseView):

    @check_token
    def get(self):
        return jsonify(self.user.dict)
    
    def post(self):
        payload = validate(CreateUser, request.json)
        payload["password"] = hash_password(payload["password"])
        user = create_item(User, payload, self.session)
        return jsonify({"id": user.id})
    
    @check_token
    def patch(self):
        payload = validate(UpdateUser, request.json)
        user = update_item(self.token.user, payload, self.session)
        return jsonify({"user": user.id, "email": user.email})
    
    @check_token
    def delete(self):
        delete_item(self.token.user, self.session)
        return jsonify({"User deleted": "Ok"})


class LoginView(BaseView):
    def post(self):
        payload = validate(Login, request.json)
        user = self.session.query(User).filter_by(name=payload["name"]).first()
        if user is None:
            raise HttpError(404, "User not found")
        if check_password(user.password, payload["password"]):
            token = create_item(Token, {"user_id": user.id}, self.session)
            add_item(token, self.session)
            return jsonify({"token": token.token})
        raise HttpError(401, "Invalid password")
    

class ArticleView(BaseView):

    @check_token
    def get(self, article_id:int=None):
        if article_id is None:
            return jsonify([article.dict for article in self.user.articles])
        article = get_item_by_id(Article, article_id, self.session)
        check_user(article, self.token.user_id)
        return jsonify(article.dict)

    @check_token
    def post(self):
        payload = validate(CreateArticle, request.json)
        article = create_item(Article, dict(user_id=self.token.user_id, **payload), self.session)
        return jsonify({"id": article.id})
    
    @check_token
    def patch(self, article_id):
        payload = validate(UpdateArticle, request.json)
        article = get_item_by_id(Article, article_id, self.session)
        check_user(article, self.token.user_id)
        article = update_item(article, payload, self.session)
        return jsonify({"id": article.id})
    
    @check_token
    def delete(self, article_id):
        article = get_item_by_id(Article, article_id, self.session)
        check_user(article, self.token.user_id)
        delete_item(article, self.session)
        return jsonify({"status": "ok"})