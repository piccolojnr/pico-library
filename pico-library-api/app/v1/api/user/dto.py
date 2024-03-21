from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, DateTime, Float, Nested, List
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import positive

user_model = Model("User", {"email": String, "public_id": String})


profile_model = Model(
    "Profile",
    {
        "first_name": String,
        "last_name": String,
        "gender": String(attribute="gender_str"),
        "bio": String,
        "location": String,
        "created_at": String(attribute="created_at_str"),
        "updated_at": String(attribute="updated_at_str"),
        "user": Nested(user_model),
    },
)
agent_model = Model(
    "Agent",
    {
        "id": Integer,
        "name": String,
        "alias": String,
        "birth_date": String,
        "death_date": String,
        "webpage": String,
        "type": String(attribute="type_name"),
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
        "agents": List(Nested(agent_model)),
        "created_at": String(attribute="created_at_str"),
        "updated_at": String(attribute="updated_at_str"),
    },
)

recommendation_pagination_reqparse = RequestParser(bundle_errors=True)
recommendation_pagination_reqparse.add_argument(
    "page", type=positive, default=1, required=False
)
recommendation_pagination_reqparse.add_argument(
    "per_page", type=positive, choices=[5, 10, 25, 50, 100], default=10, required=False
)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)
book_pagination_model = Model(
    "ItemPagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer,
        "items_per_page": Integer,
        "total_items": Integer,
        "items": List(Nested(book_model)),
    },
)
