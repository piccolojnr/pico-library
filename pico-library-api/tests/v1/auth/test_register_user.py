from tests.v1.util import register_user
from pprint import pprint


def test_register_user(db_session, app, client):
    with app.app_context():
        response = register_user(client)
        print()
        pprint(response.json)
        # assert User.query.count() == 1
        # user = User.query.first()
        # assert user.email == 'test@example.com'
        # assert user.password_hash is not None
        # assert user.username == 'testuser'
        # assert user.bio is None
        # assert user.image is None
        # assert user.following == 0
        # assert user.followers == 0
        # assert user.created_at is not None
        # assert user.updated_at is not None


#     # assert response.status_code == 201
#     # assert response.json['message'] == 'User created successfully'
#     # assert 'token' in response.json
#     # assert 'user' in response.json
#     # assert 'id' in response.json['user']
#     # assert 'email' in response.json['user']
#     # assert 'password' in response.json['user']
#     # assert 'username' in response.json['user']
#     # assert 'bio' in response.json['user']
#     # assert 'image' in response.json['user']
#     # assert 'following' in response.json['user']
#     # assert 'followers' in response.json['user']
#     # assert 'created_at' in response.json['user']
#     # assert 'updated_at' in response.json['user']
#     # assert 'token' in response.json
#     # assert 'user' in response.json
#     # assert 'id' in response.json['user']
#     # assert 'email' in response.json['user']
#     # assert 'password' in response.json['user']
