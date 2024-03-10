import pytest


def test_create_user(db_session, user_factory):
    user = user_factory.create()
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.email is not None
    with pytest.raises(AttributeError):
        user.password

    assert user.check_password("password") is False


def test_user_encode_auth_token(user):
    auth_: dict[str, bytes] | Exception = user.encode_auth_token()
    assert isinstance(auth_["auth_token"], bytes)
    assert isinstance(auth_["refresh_token"], bytes)


# def test_auth_token_expires(user):megamind 2

#     auth_ = user.encode_auth_token()
#     assert isinstance(auth_["auth_token"], bytes)
#     assert isinstance(auth_["refresh_token"], bytes)

#     time.sleep(5)
#     decoded_auth_token = user.decode_auth_token(auth_token)
#     assert decoded_auth_token["success"] == False
#     assert decoded_auth_token["error"] == "Signature expired. Please log in again."


# def test_auth_token_invalid(user):
#     auth_token = user.encode_auth_token()
#     assert isinstance(auth_token, bytes)

#     decoded_auth_token = user.decode_auth_token(auth_token + b"a")
#     assert decoded_auth_token["success"] == False
#     assert decoded_auth_token["error"] == "Invalid token. Please log in again."


# def test_auth_token_missing(user):
#     decoded_auth_token = user.decode_auth_token(b"")
#     assert decoded_auth_token["success"] == False
#     assert decoded_auth_token["error"] == "Invalid token. Please log in again."
#     assert "token" not in decoded_auth_token


# def test_auth_token_blacklisted(user):
#     auth_token = user.encode_auth_token()
#     assert isinstance(auth_token, bytes)

#     res = User.blacklist_token(auth_token)
#     assert res["success"] is True
#     decoded_auth_token = user.decode_auth_token(auth_token)
#     assert decoded_auth_token["success"] == False
#     assert decoded_auth_token["error"] == "Token blacklisted. Please log in again."
#     assert "token" not in decoded_auth_token
