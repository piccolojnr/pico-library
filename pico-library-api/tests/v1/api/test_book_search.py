from pprint import pprint
from tests.v1.util import search_books


def test_search_books(db_session, app, client, seed_books):
    with app.app_context():
        response = search_books(client, query="", criteria="author", page=1, per_page=5)

        assert response.status_code == 200
        assert response.json["total_items"] == 5
        assert response.json["page"] == 1
        assert response.json["items_per_page"] == 5

        response = search_books(client, query="", criteria="author", page=2, per_page=5)
        assert response.status_code == 200
        assert response.json["total_items"] == 5
        assert response.json["items_per_page"] == 5
        assert response.json["page"] == 2
