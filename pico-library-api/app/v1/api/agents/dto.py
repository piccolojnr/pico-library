from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, Nested, List
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import positive


agent_pagination_reqparse = RequestParser(bundle_errors=True)
agent_pagination_reqparse.add_argument(
    "page", type=positive, required=False, default=1, help="Page number"
)
agent_pagination_reqparse.add_argument(
    "per_page",
    type=positive,
    required=False,
    choices=[5, 10, 25, 50, 100],
    default=10,
    help="Items per page",
)
agent_pagination_reqparse.add_argument(
    "type",
    type=str,
    choices=[
        "ANNOTATOR",
        "AUTHOR",
        "COMMENTATOR",
        "COMPILER",
        "COMPOSER",
        "CONTRIBUTOR",
        "EDITOR",
        "ILLUSTRATOR",
        "OTHER",
        "PHOTOGRAPHER",
        "TRANSLATOR",
        "null",
    ],
    required=False,
    default="null",
    help="Agent type",
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
        "agent_type": String,
    },
)


create_agent_reqparse = RequestParser(bundle_errors=True)
create_agent_reqparse.add_argument(
    "name", type=str, required=True, help="Agent name is required"
)
create_agent_reqparse.add_argument(
    "alias",
    type=str,
    required=False,
)
create_agent_reqparse.add_argument(
    "birth_date",
    type=str,
    required=False,
)
create_agent_reqparse.add_argument(
    "death_date", type=str, required=False, help="Agent death date is optional"
)
create_agent_reqparse.add_argument(
    "webpage", type=str, required=False, help="Agent webpage is optional"
)
create_agent_reqparse.add_argument(
    "type",
    type=str,
    choices=[
        "ANNOTATOR",
        "AUTHOR",
        "COMMENTATOR",
        "COMPILER",
        "COMPOSER",
        "CONTRIBUTOR",
        "EDITOR",
        "ILLUSTRATOR",
        "OTHER",
        "PHOTOGRAPHER",
        "TRANSLATOR",
        "null",
    ],
    default="null",
    required=False,
)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)

agent_pagination_model = Model(
    "AgentPagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer,
        "items_per_page": Integer,
        "total_items": Integer,
        "items": List(Nested(agent_model)),
    },
)
