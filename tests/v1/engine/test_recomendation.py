from app.v1.services.recommendation_engine import generate_recommendations
from app.v1.models import Book, Subject
import random
from tests.v1.util import get_user_recommendations, register_user
from pprint import pprint


def test_recommedations_for_user(db_session, app, client, seed_books, user_factory):

    user = user_factory.create()

    db_session.add(user)
    db_session.commit()

    recommendations_1, has_next, has_prev, total_pages = generate_recommendations(
        user, 1, 20
    )

    assert len(recommendations_1) == 20
    assert type(recommendations_1[0]) == Book

    recommendations_2, has_next, has_prev, total_pages = generate_recommendations(
        user, 1, 20
    )

    assert recommendations_1 == recommendations_2

    subjects = Subject.query.all()

    u_subjects = [random.choice(subjects) for _ in range(5)]

    for subject in u_subjects:
        subject.score = 2

    db_session.commit()

    recommendations_3, has_next, has_prev, total_pages = generate_recommendations(
        user, 1, 20
    )

    assert len(recommendations_1) == 20
    assert type(recommendations_1[0]) == Book
    recommendations_4, has_next, has_prev, total_pages = generate_recommendations(
        user, 1, 20
    )

    assert len(recommendations_1) == 20
    assert type(recommendations_1[0]) == Book

    with app.app_context():
        response = register_user(client)
        assert response.status_code == 201

        auth_token = response.json["auth"]["auth_token"]

        response = get_user_recommendations(client, auth_token)

        assert "has_prev" in response.json and not response.json["has_prev"]
        assert "has_next" in response.json and response.json["has_next"]
        assert "page" in response.json and response.json["page"] == 1
        assert "total_pages" in response.json
        assert (
            "items_per_page" in response.json and response.json["items_per_page"] == 10
        )
        assert "total_items" in response.json and response.json["total_items"] == 10
        assert "items" in response.json and len(response.json["items"]) == 10
