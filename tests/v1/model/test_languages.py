def test_create_language(language_factory, db_session):
    language = language_factory.create()
    db_session.add(language)
    db_session.commit()

    assert language.code is not None
