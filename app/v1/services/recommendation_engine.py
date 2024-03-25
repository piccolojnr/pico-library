from app.v1.models import (
    Book,
    User,
    BookmarkStatus,
    Bookmark,
    Comment,
    CommentType,
)
from sqlalchemy import func

from math import log1p


def calculate_review_score(book: Book):
    reviews: list[Comment] = Comment.query.filter(
        Comment.book_id == book.id, Comment.type == CommentType.REVIEW
    ).all()
    total_score = 0
    total_votes = 0
    for review in reviews:
        total_score += review.average_rating * (
            review.upvotes() - review.downvotes()
        )  # Consider both rating and svotes
        total_votes += review.upvotes() + review.downvotes()

    if total_votes > 0:
        return total_score / total_votes  # Calculate average score per vote
    else:
        return 0  # Default score if no reviews available


def calculate_popularity_score(book: Book):
    max_reads = max(Bookmark.query.count(), 1)
    num_reads = max(Bookmark.query.filter(Bookmark.book_id == book.id).count(), 1)
    max_downloads = max(Book.query.with_entities(func.max(Book.downloads)).scalar(), 1)

    # Normalize reads and downloads to a 0-1 scale
    normalized_reads = log1p(num_reads) / log1p(max_reads)
    normalized_downloads = log1p(book.downloads) / log1p(max_downloads)

    # Calculate score
    score = (5 * normalized_reads) + (5 * normalized_downloads)

    return score * 10


def calculate_score(user: User, book: Book):
    # Example scoring function
    score = 0
    for subject in book.subjects:
        if subject in user.subjects:
            score += 1

            score += (
                subject.score
            )  # Incorporate subject score into the score calculation

    for bookshelf in book.bookshelves:
        if bookshelf in user.bookshelves:
            score += 1
            score += bookshelf.score

    # Incorporate other factors into the score calculation, such as average rating
    if book.average_rating:
        score += book.average_rating

    return score


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
    books = sorted(
        books, key=lambda x: x.average_rating
    )  # Replace some_criteria with the actual sorting criteria

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
