from aiohttp import web

from pg import session_middleware, http_errors_middleware
from context import init_orm
from views import UserView, LoginView, ArticleView


def _get_app():
    app = web.Application()
    app.middlewares.extend([session_middleware, http_errors_middleware])
    app.cleanup_ctx.append(init_orm)

    app.add_routes([
        web.post(r'/login', LoginView),
        web.post(r'/user', UserView),
        web.get(r'/user', UserView),
        web.patch(r'/user', UserView),
        web.delete(r'/user', UserView),
        web.get(r'/article', ArticleView),
        web.get(r'/article/{article_id:\d+}', ArticleView),
        web.post(r'/article', ArticleView),
        web.patch(r'/article/{article_id:\d+}', ArticleView),
        web.delete(r'/article/{article_id:\d+}', ArticleView),
    ])

    return app


async def get_app():
    return _get_app()


if __name__ == "__main__":
    web.run_app(_get_app())