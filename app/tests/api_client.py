from typing import List, Literal, NamedTuple, Optional, Tuple

import requests

HTTP_METHOD = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
RESPONSE_TYPE = Optional[Literal["json", "text"]]


class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description

    def __str__(self):
        return f"{self.status_code=}\n{self.description=}"


class AbstractIdResponse(NamedTuple):
    id: int


class AbstractStatusResponse(NamedTuple):
    status: str


class TokenResponse(NamedTuple):
    token: str


class CreateUserResponse(AbstractIdResponse):
    pass


class GetUserResponse(NamedTuple):
    id: int
    name: str
    email: str
    articles: List[int]


class UpdateUserResponse(AbstractIdResponse):
    pass


class DeleteUserResponse(AbstractStatusResponse):
    pass


class CreateArticleResponse(AbstractIdResponse):
    pass


class ArticleItem(NamedTuple):
    id: int
    owner: int
    title: str
    description: str
    created_at: str

class GetArticleResponse(ArticleItem):
    pass


GetArticleListResponse = Tuple[ArticleItem]


class UpdateArticleResponse(AbstractIdResponse):
    pass


class DeleteArticleResponse(AbstractIdResponse):
    pass


class ArticleApiClient:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.client = requests.Session()
        self.headers = {}

    def _call(
        self,
        http_method: HTTP_METHOD,
        api_method: str,
        response_type: RESPONSE_TYPE = "json",
        json: dict = None,
        **kwargs,
    ) -> requests.Response | dict | str | list:
        headers = {**kwargs.pop("headers", {}), **self.headers}
        response = getattr(self.client, http_method.lower())(
            f"{self.api_url}{api_method}", json=json, headers=headers, **kwargs
        )

        if response.status_code >= 400:
            raise HttpError(response.status_code, response.text)

        if response_type is not None:
            response = getattr(response, response_type)
            if callable(response):
                response = response()
        return response

    def login(self, name: str, password: str) -> TokenResponse:
        return TokenResponse(
            **self._call("POST", "/login", json={"name": name, "password": password})
        )

    def auth(self, name: str, password: str) -> None:
        token = self.login(name, password).token
        self.headers["Authorization"] = token

    def create_user(self, name: str, email: str, password: str) -> CreateUserResponse:
        return CreateUserResponse(
            **self._call("POST", "/user", json={"name": name, "email": email, "password": password})
        )

    def get_user(self) -> GetUserResponse:
        return GetUserResponse(**self._call("GET", "/user"))

    def update_user(self, name: str = None, email: str = None,  password: str = None) -> UpdateUserResponse:
        payload = {}
        if name is not None:
            payload["name"] = name
        if password is not None:
            payload["password"] = password
        if email is not None:
            payload["email"] = email
        return UpdateUserResponse(**self._call("PATCH", "/user", json=payload))

    def delete_user(self) -> DeleteUserResponse:
        return DeleteUserResponse(**self._call("DELETE", "/user"))

    def get_articles(self) -> GetArticleListResponse:
        return tuple(ArticleItem(**article_item) for article_item in self._call("GET", "/article"))

    def get_article(self, article_id: int) -> GetArticleResponse:
        return GetArticleResponse(**self._call("GET", f"/article/{article_id}"))

    def update_article(
        self, article_id: int, title: str = None, description: str = None
    ) -> UpdateArticleResponse:
        payload = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        return UpdateArticleResponse(
            **self._call("PATCH", f"/article/{article_id}", json=payload)
        )

    def create_article(self, title: str, description: str) -> CreateArticleResponse:
        return CreateArticleResponse(
            **self._call("POST", "/article", json={"title": title, "description": description})
        )