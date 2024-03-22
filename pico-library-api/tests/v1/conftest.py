"""Global pytest fixtures."""

import pandas as pd
import pytest
import tqdm

from app.v1 import create_app, db as database
from app.v1.models import (
    Book,
    Agent,
    AgentType,
    Bookshelf,
    Language,
    Publisher,
    Resource,
    ResourceType,
    Subject,
    User,
    UserGender,
    Bookmark,
    BookmarkStatus,
    Comment,
    CommentType,
    CommentVote,
    CommentVoteType,
    Profile,
    Rating,
)
import factory

from seed.seed import add_book, read_partial_csv_gz


@pytest.fixture
def app():
    app = create_app("testing")
    return app


@pytest.fixture
def db_session(app):
    with app.app_context():
        database.create_all()
        yield database.session
        database.session.remove()
        database.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def seed_books():
    books_df = read_partial_csv_gz("books_df.csv.gz", 50)

    books_df["resources"] = books_df["resources"].apply(lambda x: eval(x))
    books_df["agents"] = books_df["agents"].apply(lambda x: eval(x))
    books_df["languages"] = books_df["languages"].apply(lambda x: eval(x))
    books_df["subjects"] = books_df["subjects"].apply(lambda x: eval(x))
    books_df["publishers"] = books_df["publishers"].apply(lambda x: eval(x))
    books_df["bookshelves"] = books_df["bookshelves"].apply(lambda x: eval(x))
    books_df["description"] = books_df["description"].apply(
        lambda x: x if type(x) == str else ""
    )

    books = books_df.to_dict("records")

    for i in range(len(books)):
        book = books[i]
        add_book(book)


@pytest.fixture
def user_factory(db_session):
    class UserFactory(factory.Factory):
        class Meta:
            model = User

        email = factory.Faker("email")
        password = factory.Faker("password")

    return UserFactory


@pytest.fixture
def user(db_session, user_factory):
    user = user_factory.create()
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def book_factory(db_session):
    class BookFactory(factory.Factory):
        class Meta:
            model = Book

        id = factory.Faker("random_int", min=1, max=1000)
        format = factory.Faker("file_extension")
        title = factory.Faker("sentence", nb_words=4)
        description = factory.Faker("paragraph", nb_sentences=3)
        downloads = factory.Faker("random_int", min=100, max=1000)
        license = factory.Faker("word")

    return BookFactory


@pytest.fixture
def agent_type_factory(db_session):
    class AgentTypeFactory(factory.Factory):
        class Meta:
            model = AgentType

        name = factory.Faker("word")

    return AgentTypeFactory


@pytest.fixture
def agent_factory(db_session, agent_type_factory):
    agent_type = agent_type_factory.create()
    db_session.add(agent_type)
    db_session.commit()

    class AgentFactory(factory.Factory):
        class Meta:
            model = Agent

        name = factory.Faker("name")
        alias = factory.Faker("user_name")
        birth_date = factory.Faker("date_of_birth")
        death_date = factory.Faker("date_of_birth")
        webpage = factory.Faker("url")
        type_name = agent_type.name

    return AgentFactory


@pytest.fixture
def bookshelf_factory(db_session):
    class BookshelfFactory(factory.Factory):
        class Meta:
            model = Bookshelf

        name = factory.Faker("name")

    return BookshelfFactory


@pytest.fixture
def language_factory(db_session):
    class LanguageFactory(factory.Factory):
        class Meta:
            model = Language

        code = factory.Faker("language_code")

    return LanguageFactory


@pytest.fixture
def publisher_factory(db_session):
    class PublisherFactory(factory.Factory):
        class Meta:
            model = Publisher

        name = factory.Faker("company")

    return PublisherFactory


@pytest.fixture
def resource_type_factory(db_session):
    class ResourceTypeFactory(factory.Factory):
        class Meta:
            model = ResourceType

        name = factory.Faker("word")

    return ResourceTypeFactory


@pytest.fixture
def resource_factory(db_session, resource_type_factory):
    resource_type = resource_type_factory.create()
    db_session.add(resource_type)
    db_session.commit()

    class ResourceFactory(factory.Factory):
        class Meta:
            model = Resource

        url = factory.Faker("url")
        size = factory.Faker("random_int", min=100, max=1000)
        modified = factory.Faker("date_time")
        type_name = resource_type.name

    return ResourceFactory


@pytest.fixture
def subject_factory(db_session):
    class SubjectFactory(factory.Factory):
        class Meta:
            model = Subject

        name = factory.Faker("word")

    return SubjectFactory


@pytest.fixture
def bookmark_factory(db_session, user_factory, book_factory):
    user = user_factory.create()
    book = book_factory.create()
    db_session.add(user)
    db_session.add(book)
    db_session.commit()

    class BookmarkFactory(factory.Factory):
        class Meta:
            model = Bookmark

        user_id = user.id
        book_id = book.id
        status = factory.Faker("random_element", elements=BookmarkStatus)

    return BookmarkFactory


@pytest.fixture
def comment_book_factory(db_session, user_factory, book_factory):
    user = user_factory.create()
    book = book_factory.create()
    db_session.add(user)
    db_session.add(book)
    db_session.commit()

    class CommentFactory(factory.Factory):
        class Meta:
            model = Comment

        user_id = user.id
        book_id = book.id
        type = CommentType.COMMENT
        content = factory.Faker("sentence", nb_words=4)

    return CommentFactory


@pytest.fixture
def comment_comment_factory(db_session, user_factory, comment_book_factory):
    user = user_factory.create()
    comment = comment_book_factory.create()
    db_session.add(user)
    db_session.add(comment)
    db_session.commit()

    class CommentFactory(factory.Factory):
        class Meta:
            model = Comment

        user_id = user.id
        parent_id = comment.id
        type = CommentType.REPLY
        content = factory.Faker("sentence", nb_words=4)

    return CommentFactory


@pytest.fixture
def comment_review_factory(db_session, user_factory, book_factory):
    user = user_factory.create()
    book = book_factory.create()
    db_session.add(user)
    db_session.add(book)
    db_session.commit()

    class CommentFactory(factory.Factory):
        class Meta:
            model = Comment

        user_id = user.id
        book_id = book.id
        type = CommentType.REVIEW
        content = factory.Faker("sentence", nb_words=4)

    return CommentFactory


@pytest.fixture
def comment_vote_factory(db_session, user_factory, comment_book_factory):
    user = user_factory.create()
    comment = comment_book_factory.create()
    db_session.add(user)
    db_session.add(comment)
    db_session.commit()

    class CommentVoteFactory(factory.Factory):

        class Meta:
            model = CommentVote

        user_id = user.id
        comment_id = comment.id
        vote = factory.Faker("random_element", elements=CommentVoteType)

    return CommentVoteFactory


@pytest.fixture
def profile_factory(db_session, user_factory):
    user = user_factory.create()
    db_session.add(user)
    db_session.commit()

    class ProfileFactory(factory.Factory):
        class Meta:
            model = Profile

        user_id = user.id
        gender = factory.Faker("random_element", elements=UserGender)
        first_name = factory.Faker("name")
        last_name = factory.Faker("name")
        location = factory.Faker("city")
        bio = factory.Faker("sentence", nb_words=4)

    return ProfileFactory


@pytest.fixture
def rating_factory(db_session, user_factory, book_factory):
    user = user_factory.create()
    book = book_factory.create()
    db_session.add(user)
    db_session.add(book)
    db_session.commit()

    class RatingFactory(factory.Factory):
        class Meta:
            model = Rating

        user_id = user.id
        book_id = book.id
        rating = factory.Faker("random_int", min=1, max=5)

    return RatingFactory
