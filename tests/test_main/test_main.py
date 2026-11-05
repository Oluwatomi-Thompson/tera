"""Main blueprint: landing, about, dashboard."""


def test_index_loads(client, db):
    resp = client.get("/")
    assert resp.status_code == 200


def test_about_loads(client):
    resp = client.get("/about")
    assert resp.status_code == 200


def test_dashboard_requires_login(client):
    resp = client.get("/dashboard", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers["Location"]


def test_dashboard_shows_progress_for_logged_in_user(client, learner, published_lesson):
    client.post("/auth/login", data={"email": learner.email, "password": "correct-password"})
    resp = client.get("/dashboard")
    assert resp.status_code == 200
    assert published_lesson.title.encode() in resp.data
