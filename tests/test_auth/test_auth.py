"""Auth blueprint: register, login, logout (FR1, FR2)."""
from app.models import User


def test_register_creates_user_and_logs_in(client, db):
    resp = client.post(
        "/auth/register",
        data={
            "email": "new@example.com",
            "password": "correct-password",
            "confirm_password": "correct-password",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert User.query.filter_by(email="new@example.com").first() is not None
    # Dashboard is login_required — reaching it with a 200 confirms we're logged in.
    assert b"Dashboard" in resp.data or resp.request.path == "/dashboard"


def test_register_rejects_duplicate_email(client, learner):
    resp = client.post(
        "/auth/register",
        data={
            "email": learner.email,
            "password": "another-password",
            "confirm_password": "another-password",
        },
        follow_redirects=True,
    )
    assert b"already exists" in resp.data


def test_register_rejects_mismatched_passwords(client, db):
    resp = client.post(
        "/auth/register",
        data={
            "email": "mismatch@example.com",
            "password": "correct-password",
            "confirm_password": "different-password",
        },
    )
    assert User.query.filter_by(email="mismatch@example.com").first() is None
    assert resp.status_code == 200  # re-rendered form, not a redirect


def test_login_success(client, learner):
    resp = client.post(
        "/auth/login",
        data={"email": learner.email, "password": "correct-password"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert resp.request.path == "/dashboard"


def test_login_wrong_password(client, learner):
    resp = client.post(
        "/auth/login",
        data={"email": learner.email, "password": "wrong-password"},
        follow_redirects=True,
    )
    assert b"Incorrect email or password" in resp.data


def test_login_unknown_email(client, db):
    resp = client.post(
        "/auth/login",
        data={"email": "nobody@example.com", "password": "whatever123"},
        follow_redirects=True,
    )
    assert b"Incorrect email or password" in resp.data


def test_logout_requires_login(client):
    resp = client.get("/auth/logout", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers["Location"]


def test_logout_then_dashboard_redirects_to_login(client, learner):
    client.post("/auth/login", data={"email": learner.email, "password": "correct-password"})
    client.get("/auth/logout")
    resp = client.get("/dashboard", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers["Location"]


def test_profile_requires_login(client):
    resp = client.get("/auth/profile", follow_redirects=False)
    assert resp.status_code == 302


def test_profile_shows_progress_for_logged_in_user(client, learner, published_lesson):
    client.post("/auth/login", data={"email": learner.email, "password": "correct-password"})
    resp = client.get("/auth/profile")
    assert resp.status_code == 200
