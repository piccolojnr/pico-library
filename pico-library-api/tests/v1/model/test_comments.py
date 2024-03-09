from app.v1.models import CommentType

def test_create_comment(db_session, comment_book_factory, comment_comment_factory, comment_review_factory):
    comment_book = comment_book_factory.create()
    db_session.add(comment_book)
    db_session.commit()
    
    assert comment_book.id is not None
    assert comment_book.content is not None
    assert comment_book.user_id is not None
    assert comment_book.book_id is not None
    assert comment_book.created_at is not None
    assert comment_book.updated_at is not None
    assert comment_book.type == CommentType.COMMENT
    
    comment_review = comment_review_factory.create()
    db_session.add(comment_review)
    db_session.commit()
    
    assert comment_review.id is not None
    assert comment_review.content is not None
    assert comment_review.user_id is not None
    assert comment_review.book_id is not None
    assert comment_review.created_at is not None
    assert comment_review.updated_at is not None
    assert comment_review.type == CommentType.REVIEW
    
    comment_comment = comment_comment_factory.create()
    db_session.add(comment_comment)
    db_session.commit()
    
    assert comment_comment.id is not None
    assert comment_comment.content is not None
    assert comment_comment.user_id is not None
    assert comment_comment.parent_id is not None
    assert comment_comment.created_at is not None
    assert comment_comment.updated_at is not None
    assert comment_comment.type == CommentType.REPLY
    
def test_create_comment_vote(db_session, comment_vote_factory):
    comment_vote = comment_vote_factory.create()
    db_session.add(comment_vote)
    db_session.commit()

    assert comment_vote.id is not None
    assert comment_vote.user_id is not None
    assert comment_vote.comment_id is not None
    assert comment_vote.vote is not None
    assert comment_vote.created_at is not None
    assert comment_vote.updated_at is not None