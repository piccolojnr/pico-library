from app.v1.models import Agent, AgentType, Book


def get_featured_authors(page=1, per_page=10):
    agents = Agent.query.filter(
        Agent.agent_type == AgentType.AUTHOR, Agent.books.any(Book.downloads > 20)
    ).paginate(page, per_page, error_out=False)
    return agents
