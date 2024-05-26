from aiohttp import web

from pg import session_middleware
from context import init_orm
from views import UserView, LoginView, ArticleView


def get_app():
    app = web.Application()
    app.middlewares.extend([session_middleware])
    app.cleanup_ctx.append(init_orm)

    app.add_routes([
        web.get(r'/user/{user_id:\d+}', UserView),
        web.patch(r'/user', UserView),
        web.delete(r'/user', UserView),
        web.post(r'/user', UserView),
        web.post("/login", LoginView),
        web.post("/article", ArticleView),
        web.get("/article", ArticleView),
        web.get(r"/article/{article_id:\d+}", ArticleView),
        web.patch(r"/article/{article_id:\d+}", ArticleView),
        web.delete(r"/article/{article_id:\d+}", ArticleView),
    ])

    return app


async def _get_app():
    return get_app()


if __name__ == "__main__":
    web.run_app(get_app())