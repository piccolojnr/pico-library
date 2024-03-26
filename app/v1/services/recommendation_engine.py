from app.v1.models import (
    Book,
    User,
    BookmarkStatus,
    Bookmark,
)
from . import calculate_score, calculate_review_score, calculate_popularity_score


def generate_recommendations(user: User, page=1, per_page=10):
    user_books_query: list[Bookmark] = Bookmark.query.filter(
        Bookmark.user_id == user.id,
        Bookmark.status.in_(
            [
                BookmarkStatus.READ,
                BookmarkStatus.CURRENTLY_READING,
                BookmarkStatus.WANT_TO_READ,
                BookmarkStatus.WANT_TO_READ,
            ]
        ),
    ).all()

    books = Book.query.all()

    unread_books = [book for book in books if book not in user_books_query]

    # Calculate scores for candidate books
    scores = {}
    for book in unread_books:
        score = calculate_score(user, book)
        # Incorporate review score based on reviews and votes
        score += calculate_review_score(book)
        # Incorporate popularity score based on the number of reads
        score += calculate_popularity_score(book)
        scores[book] = score

    # Rank candidate books based on scores
    ranked_books = sorted(scores, key=scores.get, reverse=True)
    # Select top-N recommendations
    start = (page - 1) * per_page
    end = start + per_page
    recommendations_page = ranked_books[start:end]

    has_next_page = len(ranked_books) - end > 0
    has_previous_page = page > 1
    total_pages = len(ranked_books) // per_page + 1

    return recommendations_page, has_next_page, has_previous_page, total_pages
