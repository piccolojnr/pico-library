def test_create_bookmarks(db_session, bookmark_factory):
    bookmark = bookmark_factory.create()
    
    db_session.add(bookmark)
    db_session.commit()
    
    assert bookmark.user is not None
    assert bookmark.book is not None
    assert bookmark.status is not None
    
    