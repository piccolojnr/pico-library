def test_create_ratings(db_session, rating_factory):
    ratings = rating_factory.create()
    
    db_session.add(ratings)
    db_session.commit()
    
    assert ratings.rating is not None
    assert ratings.user_id is not None
    assert ratings.book_id is not None
    assert ratings.created_at is not None
    