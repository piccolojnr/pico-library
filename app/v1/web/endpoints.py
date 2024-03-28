from flask import render_template, redirect, url_for
from . import web_bp
from flask import request
import requests


# Homepage
@web_bp.route("/")
def index():
    try:
        base_url = request.url_root
        response = requests.get(base_url + "api/v1/books/popular?per_page=3")
        popular_books = response.json()
        response = requests.get(base_url + "api/v1/agents/popular?per_page=3")
        popular_agents = response.json()
        response = requests.get(base_url + "api/v1/bookshelves?per_page=10")
        bookshelves = response.json()
        response = requests.get(base_url + "api/v1/subjects?per_page=10")
        subjects = response.json()

        return render_template(
            "homepage.html",
            popular_books=popular_books,
            popular_agents=popular_agents,
            bookshelves=bookshelves,
            subjects=subjects,
        )
    except Exception as e:
        print(e)
        return redirect(url_for("site.internal_server_error"))


# Book Listings
@web_bp.route("/books")
def book_listings():
    # get parameters page
    page = request.args.get("page", 1, type=int)
    lan = request.args.get("lan", "all", type=str)

    # Logic to fetch and display book listings
    base_url = request.url_root
    response = requests.get(
        base_url + f"api/v1/books?page={page}&per_page=10&lan={lan}"
    )
    pagination = response.json()
    response = requests.get(base_url + "api/v1/languages")
    languages = response.json()
    return render_template(
        "book_listings.html", pagination=pagination, languages=languages, lan=lan
    )


@web_bp.route("/agents")
def agent_listings():
    # get parameters page

    page = request.args.get("page", 1, type=int)
    agent_type = request.args.get("agent_type", "all", type=str)
    agent_type = f"&type={agent_type}" if agent_type and agent_type != "all" else ""
    # Logic to fetch and display book listings
    base_url = request.url_root
    response = requests.get(
        base_url + f"api/v1/agents?page={page}&per_page=10" + agent_type
    )
    pagination = response.json()
    return render_template(
        "agent_listings.html", pagination=pagination, agent_type=agent_type
    )


@web_bp.route("/subjects")
def subject_listings():
    # get parameters page
    page = request.args.get("page", 1, type=int)
    # Logic to fetch and display book listings
    base_url = request.url_root
    response = requests.get(base_url + f"api/v1/subjects?page={page}&per_page=30")
    pagination = response.json()

    return render_template("subject_listings.html", pagination=pagination)


@web_bp.route("/subjects/<int:subject_id>/books")
def subject_book_listings(subject_id):
    # get parameters page
    lan = request.args.get("lan", "all", type=str)

    page = request.args.get("page", 1, type=int)
    # Logic to fetch and display book listings
    base_url = request.url_root
    response = requests.get(
        base_url
        + f"api/v1/subjects/{subject_id}/books?page={page}&per_page=10&lan={lan}"
    )
    pagination = response.json()
    response = requests.get(base_url + "api/v1/languages")
    languages = response.json()
    return render_template(
        "subject_book_listings.html",
        subject_id=subject_id,
        pagination=pagination,
        languages=languages,
        lan=lan,
    )


# Book Details
@web_bp.route("/books/<int:book_id>")
def book_details(book_id):

    url = request.url_root + "api/v1/books/" + str(book_id)
    response = requests.get(url)
    if response.status_code != 200:
        return redirect(url_for("web.book_listings"))
    book_data = response.json()

    # Logic to fetch and display book details for the given book_id
    return render_template("book_details.html", book_id=book_id, book_data=book_data)


@web_bp.route("/agents/<int:agent_id>")
def agent_details(agent_id):
    # Logic to fetch and display agent details for the given agent_id
    url = request.url_root + "api/v1/agents/" + str(agent_id)
    response = requests.get(url)
    if response.status_code != 200:
        return redirect(url_for("web.book_listings"))
    agent_data = response.json()
    print(agent_data)

    return render_template(
        "agent_details.html", agent_data=agent_data, agent_id=agent_id
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
    return render_template("user_profile.html", username=username)


# Bookshelves Management
@web_bp.route("/bookshelves")
def bookshelves_management():
    # Logic to manage bookshelves
    return render_template("bookshelves_management.html")


@web_bp.route("/bookshelves/<int:bookshelf_id>")
def bookshelf(bookshelf_id):
    # Logic to fetch and display book details for the given bookshelf_id
    return render_template("bookshelf.html", bookshelf_id=bookshelf_id)


# Bookmarks Management
@web_bp.route("/bookmarks")
def bookmarks_management():
    # Logic to manage bookmarks
    return render_template("bookmarks_management.html")


# Recommendations
@web_bp.route("/recommendations")
def recommendations():
    # Logic to provide book recommendations
    return render_template("recommendations.html")


# Admin Panel
@web_bp.route("/admin")
def admin_panel():
    # Logic for admin panel (authentication required)
    return render_template("admin_panel.html")


@web_bp.route("/404")
def page_not_found():
    print("this is a 404 page")
    return render_template("errors/404.html")


@web_bp.route("/500")
def internal_server_error():
    return render_template("errors/500.html")
