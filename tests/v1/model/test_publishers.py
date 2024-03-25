def test_create_publisher(publisher_factory, db_session):
    publisher = publisher_factory.create()
    db_session.add(publisher)
    db_session.commit()

    assert publisher.name is not None
