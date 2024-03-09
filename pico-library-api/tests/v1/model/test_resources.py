def test_create_resource_type(resource_type_factory, db_session):
    resource_type = resource_type_factory.create()
    db_session.add(resource_type)
    db_session.commit()

    assert resource_type.name is not None

def test_create_resource(resource_factory, db_session):
    resource = resource_factory.create()
    db_session.add(resource)
    db_session.commit()

    assert resource.url is not None
    assert resource.size is not None
    assert resource.modified is not None
    assert resource.type is not None