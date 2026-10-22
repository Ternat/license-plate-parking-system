from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints.auth import router as auth_router
from app.core.config import settings
from app.core.security import create_access_token, decode_access_token


def _client():
    app = FastAPI()
    app.include_router(auth_router, prefix="/api/v1/auth")
    return TestClient(app)


def test_login_success_returns_token():
    client = _client()
    resp = client.post(
        "/api/v1/auth/login",
        json={
            "username": settings.ADMIN_USERNAME,
            "password": settings.ADMIN_PASSWORD,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["code"] == 200
    assert body["data"]["access_token"]
    assert body["data"]["token_type"] == "bearer"


def test_login_wrong_password_rejected():
    client = _client()
    resp = client.post(
        "/api/v1/auth/login",
        json={
            "username": settings.ADMIN_USERNAME,
            "password": settings.ADMIN_PASSWORD + "__definitely_wrong__",
        },
    )
    assert resp.status_code == 401


def test_login_wrong_username_rejected():
    client = _client()
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": "__no_such_user__", "password": settings.ADMIN_PASSWORD},
    )
    assert resp.status_code == 401


def test_jwt_roundtrip_and_invalid_token():
    token = create_access_token({"sub": "admin"})
    payload = decode_access_token(token)
    assert payload["sub"] == "admin"
    assert decode_access_token("not-a-valid-token") is None
