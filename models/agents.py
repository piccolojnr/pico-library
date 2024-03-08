from . import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, PrimaryKeyConstraint
from sqlalchemy.orm import relationship


class AgentType(Base):
    __tablename__ = "agent_type"
    id = Column(Integer, primary_key=True)
    name = Column(String)

book_agents_association = Table(
    'book_agents',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id', ondelete="CASCADE")),
    Column('agent_id', Integer, ForeignKey('agents.id', ondelete="CASCADE")),
    PrimaryKeyConstraint('book_id', 'agent_id')
)

class Agent(Base):
    """
    
    """
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    alias = Column(String)
    birth_date = Column(String)
    death_date = Column(String)
    webpage = Column(String)
    type_id = Column(Integer, ForeignKey("agent_type.id", ondelete="CASCADE"))

    type = relationship("AgentType")
    books = relationship("Book", secondary=book_agents_association, back_populates="agents")


    def __repr__(self):
        return f"<Agent {self.name}>"
    
    def __init__(self, name, alias, birth_date, death_date, webpage, type_id):
        self.name = name
        self.alias = alias
        self.birth_date = birth_date
        self.death_date = death_date
        self.webpage = webpage
        self.type_id = type_id
    
