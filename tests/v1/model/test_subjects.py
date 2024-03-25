def test_create_subject(subject_factory, db_session):
    subject = subject_factory.create()
    db_session.add(subject)
    db_session.commit()

    assert subject.name is not None
    assert subject.score == 0
