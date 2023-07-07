from unittest.mock import MagicMock, patch, AsyncMock

import fastapi_limiter
import pytest

from src.conf import messages
from src.database.models import User
from src.services.auth import auth_service

CONTACT = {"fullname": "test_name",
           "lastname": "test_lastname",
           "email": "test@test.com",
           "phone_number": "+0123456789",
           "birthday": "01.01.1970"}


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("api/auth/signup", json=user)

    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("api/auth/login", data={"username": user.get("email"), "password": user.get("password")})
    data = response.json()
    return data["access_token"]


def test_create_contact(client, token):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        response = client.post("api/contact",
                               json=CONTACT,
                               headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 201, response.text
        data = response.json()
        assert "id" in data


def test_get_contacts(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get("api/contact", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]["fullname"] == CONTACT["fullname"]
