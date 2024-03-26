from flask import render_template, redirect, url_for
from . import web_bp


# Homepage
@web_bp.route("/")
def index():
    return render_template("homepage.html")


# Book Listings
@web_bp.route("/books")
def book_listings():
    # Logic to fetch and display book listings
    return render_template("book_listings.html")


# Book Details
@web_bp.route("/books/<int:book_id>")
def book_details(book_id):
    # Logic to fetch and display book details for the given book_id
    return render_template("book_details.html", book_id=book_id)


@web_bp.route("/agents/<int:agent_id>")
def agent_details(agent_id):
    # Logic to fetch and display agent details for the given agent_id
    return render_template("agent_details.html", agent_id=agent_id)


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
