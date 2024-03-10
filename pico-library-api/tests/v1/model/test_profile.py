def test_create_profile(db_session, profile_factory):
    profile = profile_factory.create()
    db_session.add(profile)
    db_session.commit()

    assert profile.user_id is not None
    assert profile.first_name is not None
    assert profile.last_name is not None
    assert profile.bio is not None
    assert profile.created_at is not None
    assert profile.updated_at is not None
