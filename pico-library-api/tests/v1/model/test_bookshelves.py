def test_create_bookshelf(bookshelf_factory, db_session):
    bookshelf = bookshelf_factory.create()
    db_session.add(bookshelf)
    db_session.commit()

    assert bookshelf.id is not None
    assert bookshelf.name is not None