import functools

from flask import redirect, session, url_for, request
import requests


def login_required(func):
    """
    Custom decorator to check if the user is logged in.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if is_logged_in():
            return func(*args, **kwargs)
        return redirect(url_for("site.login"))

    return wrapper


def is_logged_in():
    if "auth_token" in session:
        base_url = request.url_root
        response = requests.get(
            base_url + url_for("api.protected_route"),
            headers={"Authorization": "Bearer " + session["auth_token"]},
        )
        if response.status_code == 200:
            return True
        else:
            if "refresh_token" in session:
                response = requests.post(
                    base_url + url_for("api.auth_refresh"),
                    headers={"Authorization": "Bearer " + session["refresh_token"]},
                )
                if response.status_code == 200:
                    session["auth_token"] = response.json()["auth_token"]
                    return True

    return False
