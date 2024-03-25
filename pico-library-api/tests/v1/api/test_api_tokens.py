from tests.v1.util import login_user, logout_user, clear_token, ADMIN_EMAIL
from app.v1.models import BlacklistedToken
from datetime import datetime, timedelta
from pprint import pprint
from time import sleep


def test_clear_tokens(db_session, client, admin_user):
    response = login_user(client, ADMIN_EMAIL)
    assert response.status_code == 200

    auth_token = response.json["auth"]["auth_token"]

    expires_at = datetime.utcnow() + timedelta(seconds=2)

    token = BlacklistedToken(token=auth_token, expires_at=expires_at.timestamp())
    db_session.add(token)
    db_session.commit()

    blacklisted_tokens = BlacklistedToken.query.all()
    assert len(blacklisted_tokens) == 1
    sleep(2)
    response = clear_token(client, auth_token)
    assert response.status_code == 200

    blacklisted_tokens = BlacklistedToken.query.all()
    assert len(blacklisted_tokens) == 0
