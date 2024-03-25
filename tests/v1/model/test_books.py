def test_create_book(db_session, book_factory):
    book = book_factory.create()
    db_session.add(book)
    db_session.commit()

    assert book.id is not None
    assert book.format is not None  # Add similar assertions for other fields


def test_book_relationships(book_factory, agent_factory, bookshelf_factory, language_factory, publisher_factory, resource_factory, subject_factory, db_session):
    # Create dummy data for related models
    agent = agent_factory.create()
    bookshelf = bookshelf_factory.create()
    language = language_factory.create()
    publisher = publisher_factory.create()
    resource = resource_factory.create()
    subject = subject_factory.create()

    db_session.add_all([agent, bookshelf, language, publisher, resource, subject])
    db_session.commit()

    # Create a book with relationships
    book_data = {
        "format": "pdf",
        "title": "Sample Book",
        "description": "A sample book for testing",
        "downloads": 500,
        "license": "CC BY-SA",
        "agents": [agent],
        "bookshelves": [bookshelf],
        "languages": [language],
        "publishers": [publisher],
        "resources": [resource],
        "subjects": [subject]
    }

    book = book_factory.create(**book_data)
    db_session.add(book)
    db_session.commit()

    # Test relationships
    assert book.id is not None
    assert len(book.agents) == 1
    assert book.agents[0] == agent

    assert len(book.bookshelves) == 1
    assert book.bookshelves[0] == bookshelf

    assert len(book.languages) == 1
    assert book.languages[0] == language

    assert len(book.publishers) == 1
    assert book.publishers[0] == publisher

    assert len(book.resources) == 1
    assert book.resources[0] == resource


