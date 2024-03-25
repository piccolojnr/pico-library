def test_create_agent(agent_factory, db_session):
    agent = agent_factory.create()
    db_session.add(agent)
    db_session.commit()

    assert agent.id is not None
    assert agent.name is not None
    assert agent.alias is not None
    assert agent.birth_date is not None
    assert agent.death_date is not None
    assert agent.webpage is not None
    assert agent.type is not None
