import pytest

from .api_client import HttpError
from .constants import NEW_TODO_ITEM_IMPORTANT, NEW_TODO_ITEM_NOT_IMPORTANT


class TestArticle:
    @pytest.mark.parametrize("description", ["test1", "test2"])
    def test_create_article(self, new_user_client, description: str):
        response = new_user_client.create_article(
            title="test_create_article", description=description
        )
        assert response.id is not None
        for article in new_user_client.get_user().articles:
            assert article["id"] == response.id

    def test_create_article_with_empty_name(self, new_user_client):
        with pytest.raises(HttpError) as excinfo:
            new_user_client._call("POST", "/article", json={"description": "False"})
        assert excinfo.value.status_code == 400

    def test_create_article_without_auth(self, client_non_authorized):
        with pytest.raises(HttpError) as excinfo:
            client_non_authorized.create_article("test_create_article_without_auth", "test")
        assert excinfo.value.status_code == 401

    def test_get_articles(self, new_user_client_with_articles):
        articles = new_user_client_with_articles.get_articles()
        assert len(articles) == 2
        assert articles[0].title == NEW_TODO_ITEM_IMPORTANT
        assert articles[1].title == NEW_TODO_ITEM_NOT_IMPORTANT
        assert articles[0].description == 'test'
        assert articles[1].description == 'test2'

    def test_get_articles_without_auth(self, client_non_authorized):
        with pytest.raises(HttpError) as excinfo:
            client_non_authorized.get_articles()
        assert excinfo.value.status_code == 401

    def test_get_article_id(self, new_user_client_with_articles):
        articles = new_user_client_with_articles.get_articles()
        for article in articles:
            todo_by_id = new_user_client_with_articles.get_article(article.id)
            assert todo_by_id.id == article.id
            assert todo_by_id.title == article.title
            assert todo_by_id.description == article.description

    def test_get_aricle_id_without_auth(self, client_non_authorized):
        with pytest.raises(HttpError) as excinfo:
            client_non_authorized.get_article(1)
        assert excinfo.value.status_code == 401

    def test_get_article_id_with_wrong_id(self, new_user_client_with_articles):
        with pytest.raises(HttpError) as excinfo:
            new_user_client_with_articles.get_article(9999999)
        assert excinfo.value.status_code == 404

    def test_get_article_id_not_owner(
        self, default_user_client, new_user_client_with_articles
    ):
        articles = new_user_client_with_articles.get_articles()
        for article in articles:
            with pytest.raises(HttpError) as excinfo:
                default_user_client.get_article(article.id)
            assert excinfo.value.status_code == 403

    def test_update_article_title(self, new_user_client_with_articles):
        article = new_user_client_with_articles.get_articles()[0]
        new_user_client_with_articles.update_article(article.id, title="new_name")
        article = new_user_client_with_articles.get_article(article.id)
        assert article.title == "new_name"

    def test_update_article_important(self, new_user_client_with_articles):
        article = new_user_client_with_articles.get_articles()[0]
        new_user_client_with_articles.update_article(article.id, description="Example")
        article = new_user_client_with_articles.get_article(article.id)
        assert article.description == "Example"

    def test_update_article_done(self, new_user_client_with_articles):
        article = new_user_client_with_articles.get_articles()[0]
        new_user_client_with_articles.update_article(article.id, description="Upd")
        article = new_user_client_with_articles.get_article(article.id)
        assert article.description == "Upd"
