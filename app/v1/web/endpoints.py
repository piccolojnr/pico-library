from flask import render_template, redirect, url_for
from . import web_bp
from flask import request, abort
import requests


def get_resource(api_url):
    base_url = request.url_root
    response = requests.get(base_url + api_url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        abort(404)
    else:
        abort(500)  # Handle API request errors gracefully


def get_breadcrumb_data(resource_name, resource_id, url_name):
    if resource_id:
        resource = get_resource(f"api/v1/{resource_name}/{resource_id}")
        if resource:
            return {
                "name": f"{resource_name.capitalize()}: {resource['name']}",
                "url": url_for("site.books", **{url_name: resource_id}),
                "active": "",
            }
    return None


# Homepage
@web_bp.route("/", endpoint="index", methods=["GET"])
def index():
    popular_books = get_resource("api/v1/books/popular?per_page=3")
    popular_agents = get_resource("api/v1/agents/popular?per_page=3")
    bookshelves = get_resource("api/v1/bookshelves?per_page=10")
    subjects = get_resource("api/v1/subjects?per_page=10")

    return render_template(
        "homepage.html",
        popular_books=popular_books,
        popular_agents=popular_agents,
        bookshelves=bookshelves,
        subjects=subjects,
    )


# Book Listings
@web_bp.route("/books", endpoint="books", methods=["GET"])
def book_listings():
    # Get parameters
    page = request.args.get("page", 1, type=int)
    lan = request.args.get("lan", None, type=str)
    q = request.args.get("q", None, type=str)
    agent_id = request.args.get("agent", None, type=str)
    subject_id = request.args.get("subject", None, type=str)
    bookshelf_id = request.args.get("bookshelf", None, type=str)
    # Get breadcrumb data
    breadcrumbs = [
        {"name": "Home", "url": url_for("site.index"), "active": ""},
        {"name": "Books", "url": url_for("site.books"), "active": ""},
    ]
    breadcrumbs.extend(
        [
            get_breadcrumb_data("agents", agent_id, "agent"),
            get_breadcrumb_data("subjects", subject_id, "subject"),
            get_breadcrumb_data("bookshelves", bookshelf_id, "bookshelf"),
            (
                {
                    "name": f"Query: {q}",
                    "url": url_for("site.books", q=q),
                    "active": "",
                }
                if q
                else None
            ),
        ]
    )
    breadcrumbs = [b for b in breadcrumbs if b]  # Remove None values

    lan_ = f"&lan={lan}" if lan and lan != "all" else ""
    q_ = f"&q={q}" if q else ""
    agent_id = f"&agent={agent_id}" if agent_id else ""
    subject_id = f"&subject={subject_id}" if subject_id else ""
    bookshelf_id = f"&bookshelf={bookshelf_id}" if bookshelf_id else ""
    # Get pagination data
    pagination = get_resource(
        f"api/v1/books?page={page}&per_page=10{lan_}{q_}{agent_id}{subject_id}{bookshelf_id}"
    )
    languages = get_resource("api/v1/languages")

    # Mark active breadcrumb
    breadcrumbs[-1]["active"] = "active"

    return render_template(
        "listings/book_listings.html",
        pagination=pagination,
        languages=languages,
        lan=lan,
        breadcrumbs=breadcrumbs,
    )


@web_bp.route("/agents", endpoint="agents", methods=["GET"])
def agent_listings():
    # get parameters page

    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", None, type=str)

    breadcrumbs = [
        {"name": "Home", "url": url_for("site.index"), "active": ""},
        {"name": "Agents", "url": url_for("site.agents"), "active": ""},
        (
            {
                "name": f"Query: {q}",
                "url": url_for("site.agents", q=q),
                "active": "",
            }
            if q
            else None
        ),
    ]
    breadcrumbs = [b for b in breadcrumbs if b]  # Remove None values
    breadcrumbs[-1]["active"] = "active"

    q = f"&q={q}" if q else ""
    agent_type = request.args.get("agent_type", None, type=str)

    agent_type_ = f"&type={agent_type}" if agent_type and agent_type != "all" else ""

    pagination = get_resource(f"api/v1/agents?page={page}&per_page=10{agent_type_}{q}")

    return render_template(
        "listings/agent_listings.html",
        pagination=pagination,
        agent_type=agent_type,
        breadcrumbs=breadcrumbs,
    )


@web_bp.route("/subjects", endpoint="subjects", methods=["GET"])
def subject_listings():
    # get parameters page
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", None, type=str)

    breadcrumbs = [
        {"name": "Home", "url": url_for("site.index"), "active": ""},
        {"name": "Subjects", "url": url_for("site.subjects"), "active": ""},
        (
            {
                "name": f"Query: {q}",
                "url": url_for("site.subjects", q=q),
                "active": "",
            }
            if q
            else None
        ),
    ]
    breadcrumbs = [b for b in breadcrumbs if b]  # Remove None values
    breadcrumbs[-1]["active"] = "active"

    q = f"&q={q}" if q else ""
    # Logic to fetch and display book listings
    pagination = get_resource(f"api/v1/subjects?page={page}&per_page=30{q}")

    return render_template(
        "listings/subject_listings.html", pagination=pagination, breadcrumbs=breadcrumbs
    )


@web_bp.route("/bookshelves", endpoint="bookshelves", methods=["GET"])
def bookshelf_listings():
    # get parameters page
    page = request.args.get("page", 1, type=int)

    q = request.args.get("q", None, type=str)

    breadcrumbs = [
        {"name": "Home", "url": url_for("site.index"), "active": ""},
        {"name": "Bookshelves", "url": url_for("site.bookshelves"), "active": ""},
        (
            {
                "name": f"Query: {q}",
                "url": url_for("site.bookshelves", q=q),
                "active": "",
            }
            if q
            else None
        ),
    ]
    breadcrumbs = [b for b in breadcrumbs if b]  # Remove None values
    breadcrumbs[-1]["active"] = "active"

    q = f"&q={q}" if q else ""
    # Logic to fetch and display book listings
    pagination = get_resource(f"api/v1/bookshelves?page={page}&per_page=30{q}")

    return render_template(
        "listings/bookshelf_listings.html",
        pagination=pagination,
        breadcrumbs=breadcrumbs,
    )


# Book Details
@web_bp.route("/books/<int:book_id>")
def book_details(book_id):

    book_data = get_resource(f"api/v1/books/{book_id}")

    # Logic to fetch and display book details for the given book_id
    return render_template(
        "details/book_details.html", book_id=book_id, book_data=book_data
    )


@web_bp.route("/agents/<int:agent_id>")
def agent_details(agent_id):
    # Logic to fetch and display agent details for the given agent_id
    agent_data = get_resource(f"api/v1/agents/{agent_id}")

    return render_template(
        "details/agent_details.html", agent_data=agent_data, agent_id=agent_id
    )


# User Authentication
@web_bp.route("/login")
def login():
    return render_template("authentication/login.html")


@web_bp.route("/register")
def register():
    return render_template("authentication/registration.html")


# User Profile
@web_bp.route("/profile/<username>")
def user_profile(username):
    # Logic to fetch and display user profile for the given username
    return render_template("user/user_profile.html", username=username)


# Bookshelves Management
@web_bp.route("admin/bookshelves")
def bookshelves_management():
    # Logic to manage bookshelves
    return render_template("admin/bookshelves_management.html")


# Bookmarks Management
@web_bp.route("admin/bookmarks")
def bookmarks_management():
    # Logic to manage bookmarks
    return render_template("admin/bookmarks_management.html")


# Recommendations
@web_bp.route("/recommendations")
def recommendations():
    # Logic to provide book recommendations
    return render_template("user/recommendations.html")


# Admin Panel
@web_bp.route("/admin")
def admin_panel():
    # Logic for admin panel (authentication required)
    return render_template("admin/admin_panel.html")


@web_bp.route("/404")
def page_not_found():
    return render_template("errors/404.html")


@web_bp.route("/500")
def internal_server_error():
    return render_template("errors/500.html")
