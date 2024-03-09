def test_create_user(db_session, user_factory):
    user = user_factory.create()
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.email is not None
