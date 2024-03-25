from pprint import pprint
from tests.v1.util import search_books

import pytest


@pytest.mark.parametrize("criteria", ["author", "title", "subject", "shelf"])
def test_search_books(db_session, app, client, seed_books, criteria):
    with app.app_context():
        response = search_books(client, query="", criteria=criteria, page=1, per_page=5)
        assert response.status_code == 200
        assert response.json["page"] == 1
        assert response.json["items_per_page"] == 5
