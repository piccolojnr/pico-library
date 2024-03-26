from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, Nested, List, Raw
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import positive
from app.v1.api.agents.dto import short_agent_model
from app.v1.api.bookshelves.dto import short_bookshelf_model
from app.v1.api.subjects.dto import subject_model
from app.v1.api.languages.dto import langauge_model
from app.v1.api.resources.dto import short_resource_model, create_resource_model
from app.v1.api.publishers.dto import publisher_model

book_model_short = Model(
    "BookShort",
    {
        "id": Integer,
        "title": String,
        "format": String,
        "description": String,
        "license": String,
        "downloads": Integer,
        "image": String,
        "created_at": String(attribute="created_at_str"),
        "updated_at": String(attribute="updated_at_str"),
    },
)
book_model = Model(
    "Book",
    {
        "id": Integer,
        "title": String,
        "format": String,
        "description": String,
        "license": String,
        "downloads": Integer,
        "publishers": List(Nested(publisher_model)),
        "subjects": List(Nested(subject_model)),
        "languages": List(Nested(langauge_model)),
        "bookshelves": List(Nested(short_bookshelf_model)),
        "agents": List(Nested(short_agent_model)),
        "resources": List(Nested(short_resource_model)),
        "created_at": String(attribute="created_at_str"),
        "updated_at": String(attribute="updated_at_str"),
    },
)


books_search_reqparse = RequestParser(bundle_errors=True)
books_search_reqparse.add_argument("q", type=str, required=False, help="Search query")
books_search_reqparse.add_argument(
    "criteria",
    type=str,
    choices=["title", "author", "subject", "shelf"],
    default="title",
    required=False,
)
books_search_reqparse.add_argument("page", type=positive, default=1, required=False)
books_search_reqparse.add_argument(
    "per_page", type=positive, default=10, required=False
)


recommendation_pagination_reqparse = RequestParser(bundle_errors=True)
recommendation_pagination_reqparse.add_argument(
    "page", type=positive, default=1, required=False
)
recommendation_pagination_reqparse.add_argument(
    "per_page", type=positive, default=10, required=False
)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)
book_pagination_model = Model(
    "BookPagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer,
        "items_per_page": Integer,
        "total_items": Integer,
        "items": List(Nested(book_model_short)),
    },
)


create_book_model = Model(
    "CreateBook",
    {
        "id": Integer,
        "title": String,
        "format": String,
        "description": String,
        "license": String,
        "downloads": Integer,
        "publishers": List(Integer),
        "subjects": List(Integer),
        "languages": List(Integer),
        "bookshelves": List(Integer),
        "agents": List(Integer),
        "resources": List(Nested(create_resource_model)),
    },
)

update_book_model = Model(
    "UpdateBook",
    {
        "title": String,
        "format": String,
        "description": String,
        "license": String,
        "downloads": Integer,
        "publishers": List(String),
        "subjects": List(Integer),
        "languages": List(Integer),
        "bookshelves": List(Integer),
        "agents": List(Integer),
        "resources": List(Nested(create_resource_model)),
    },
)
