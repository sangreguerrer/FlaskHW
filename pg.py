from flask import Flask, request
from views import UserView, ArticleView, LoginView
from models import Session
from errors import HttpError
from tools import handle_error


from app import get_app


app = get_app()


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


user_view = UserView.as_view("user")
article_view = ArticleView.as_view("article")
login_view = LoginView.as_view("login")


app.add_url_rule("/user", view_func=user_view, methods=["POST", "GET", "PATCH", "DELETE"])
app.add_url_rule("/login", view_func=login_view, methods=["POST"])
app.add_url_rule("/article", view_func=article_view, methods=["POST", "GET"])
app.add_url_rule("/article/<int:article_id>", view_func=article_view, methods=["GET", "PATCH", "DELETE"])

app.register_error_handler(HttpError, handle_error)

app.run()