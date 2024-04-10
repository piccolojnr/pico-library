#!./venv/bin/python
"""_summary_

    Returns:
        _type_: _description_
    """

import datetime
import pandas as pd
from app.models import (
    Publisher,
    Resource,
    ResourceType,
    Agent,
    AgentType,
    Language,
    Bookshelf,
    Book,
    Subject,
)
from app import db, create_app
from tqdm import tqdm
import sys
import argparse
import gzip


def add_resource_type(resource_type):
    new_type = ResourceType.query.filter(ResourceType.name == resource_type).first()
    if not new_type:
        new_type = ResourceType(name=resource_type)
        db.session.add(new_type)
    return new_type


def add_resources(resources):
    new_resources = []
    for resource in resources:
        resource_type = resource["type"]
        if resource_type:
            new_type = add_resource_type(resource_type)
        url = resource["url"]
        size = resource["size"]
        modified = (
            datetime.datetime.fromisoformat(resource["modified"])
            if resource["modified"]
            else None
        )
        new_resource = Resource.query.filter(Resource.url == url).first()
        if not new_resource:
            new_resource = Resource(
                url=url, size=size, type_name=new_type.name, modified=modified
            )
            db.session.add(new_resource)
        new_resources.append(new_resource)
    return new_resources


def add_agents(agents):
    new_agents = []
    for k in agents:
        if k:
            type_ = k.upper() if k and type(k) == str else None
            new_type = AgentType.OTHER
            if type_:
                new_type = AgentType.__members__.get(type_)
            for agent in agents[k]:
                name = agent["name"]
                alias = agent["alias"]
                birth_date = agent["birth_date"]
                death_date = agent["death_date"]
                webpage = agent["webpage"]
                new_agent = Agent.query.filter(Agent.name == name).first()
                if not new_agent:
                    new_agent = Agent(
                        name=name,
                        alias=alias,
                        birth_date=birth_date,
                        death_date=death_date,
                        webpage=webpage,
                        type=new_type,
                    )
                    db.session.add(new_agent)
                new_agents.append(new_agent)
    return new_agents


def add_languages(languages):
    new_languages = []
    for language in languages:
        new_language = Language.query.filter(Language.code == language).first()
        if not new_language:
            new_language = Language(code=language)
            db.session.add(new_language)
        new_languages.append(new_language)
    return new_languages


def add_bookshelves(bookshelves):
    new_bookshelves = []
    for bookshelf in bookshelves:
        new_bookshelf = Bookshelf.query.filter(Bookshelf.name == bookshelf).first()
        if not new_bookshelf:
            new_bookshelf = Bookshelf(name=bookshelf)
            db.session.add(new_bookshelf)
        new_bookshelves.append(new_bookshelf)
    return new_bookshelves


def add_subjects(subjects):
    new_subjects = []
    for subject in subjects:
        new_subject = Subject.query.filter(Subject.name == subject).first()
        if not new_subject:
            new_subject = Subject(name=subject)
            db.session.add(new_subject)
        new_subjects.append(new_subject)
    return new_subjects


def add_publishers(publishers):
    new_publishers = []
    for publisher in publishers:
        new_publisher = Publisher.query.filter(Publisher.name == publisher).first()
        if not new_publisher:
            new_publisher = Publisher(name=publisher)
            db.session.add(new_publisher)
        new_publishers.append(new_publisher)
    return new_publishers


def add_book(book):
    resources = book["resources"]
    agents = book["agents"]
    languages = book["languages"]
    bookshelves = book["bookshelves"]
    subjects = book["subjects"]
    publishers = book["publishers"]

    new_resources = add_resources(resources)
    new_agents = add_agents(agents)
    new_languages = add_languages(languages)
    new_bookshelves = add_bookshelves(bookshelves)
    new_subjects = add_subjects(subjects)
    new_publishers = add_publishers(publishers)
    db.session.commit()
    data = dict(
        id=book["id"],
        format=book["format"],
        title=book["title"],
        publishers=new_publishers,
        description=book["description"],
        downloads=book["downloads"],
        license=book["license"],
        subjects=new_subjects,
        resources=new_resources,
        languages=new_languages,
        bookshelves=new_bookshelves,
        agents=new_agents,
    )
    book = Book.query.filter(Book.id == book["id"]).first()
    if book:
        return None
    book = Book(**data)
    db.session.add(book)
    db.session.commit()

    return book


def read_partial_csv_gz(file_path, nrows):
    with gzip.open(file_path, "rt") as gz_file:
        # Use pandas to read the CSV file up to nrows
        df = pd.read_csv(gz_file, nrows=nrows)
    return df


def start_seeding(flask_env, file_path, num=None):
    print(f"Seeding with {file_path}...")

    print("preparing data...")

    if num:
        books_df = read_partial_csv_gz(file_path, num)
    else:
        books_df = pd.read_csv(file_path, compression="gzip")

    books_df["resources"] = books_df["resources"].apply(lambda x: eval(x))
    books_df["agents"] = books_df["agents"].apply(lambda x: eval(x))
    books_df["languages"] = books_df["languages"].apply(lambda x: eval(x))
    books_df["subjects"] = books_df["subjects"].apply(lambda x: eval(x))
    books_df["publishers"] = books_df["publishers"].apply(lambda x: eval(x))
    books_df["bookshelves"] = books_df["bookshelves"].apply(lambda x: eval(x))
    books_df["description"] = books_df["description"].apply(
        lambda x: x if type(x) == str else ""
    )

    print("creating app...")
    app = create_app(flask_env)
    app.app_context().push()
    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()

    books = books_df.to_dict("records")

    print(f"Seeding with {len(books)} books...")
    for i in tqdm(range(len(books))):
        book = books[i]
        add_book(book)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Seed the database with data from a CSV file."
    )
    parser.add_argument(
        "-i", "--input", help="The input csv.gz file.", default="books_df.csv.gz"
    )
    parser.add_argument(
        "-e", "--env", help="The environment to use.", default="development"
    )
    parser.add_argument(
        "-n", "--num", help="The number of books to seed.", default=None
    )
    args = parser.parse_args()
    file_path = args.input
    flask_env = args.env
    num = int(args.num) if args.num else None

    if not file_path:
        print("Please provide an input file.")
        sys.exit(1)

    start_seeding(flask_env, file_path, num)
