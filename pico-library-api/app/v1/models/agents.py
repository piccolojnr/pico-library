from app.v1 import db


class AgentType(db.Model):
    __tablename__ = "agent_type"
    name = db.Column(db.String, unique=True, primary_key=True)


book_agents_association = db.Table(
    "book_agents",
    
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column("agent_id", db.Integer, db.ForeignKey("agents.id", ondelete="CASCADE")),
    db.PrimaryKeyConstraint("book_id", "agent_id"),
)


class Agent(db.Model):
    """ """

    __tablename__ = "agents"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    alias = db.Column(db.String)
    birth_date = db.Column(db.String)
    death_date = db.Column(db.String)
    webpage = db.Column(db.String)
    type_name = db.Column(db.String, db.ForeignKey("agent_type.name", ondelete="CASCADE"), nullable=False)

    type = db.relationship("AgentType")
    books = db.relationship(
        "Book", secondary=book_agents_association, back_populates="agents"
    )

    def __repr__(self):
        return f"<Agent {self.name}>"

    def __init__(self, name, alias, birth_date, death_date, webpage, type_name):
        self.name = name
        self.alias = alias
        self.birth_date = birth_date
        self.death_date = death_date
        self.webpage = webpage
        self.type_name = type_name
