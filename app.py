from flask import Flask
from functools import cache


@cache
def get_app():
    app = Flask("arhub")
    return app