"""Admin blueprint: FR10 as scoped by ADR-004 — publish/reorder/resync for
lessons (no content_body edit form), full CRUD for institutions."""
from app.models import Institution, Lesson


def _login(client, user):
    client.post("/auth/login", data={"email": user.email, "password": "correct-password"})


def test_dashboard_requires_login(client):
    resp = client.get("/admin/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers["Location"]


def test_dashboard_forbidden_for_non_admin(client, learner):
    _login(client, learner)
    resp = client.get("/admin/")
    assert resp.status_code == 403


def test_dashboard_accessible_for_admin(client, admin, published_lesson):
    _login(client, admin)
    resp = client.get("/admin/")
    assert resp.status_code == 200
    assert published_lesson.title.encode() in resp.data


def test_toggle_publish(client, admin, draft_lesson):
    _login(client, admin)
    assert draft_lesson.is_published is False
    client.post(f"/admin/lessons/{draft_lesson.id}/publish", follow_redirects=True)
    assert Lesson.query.get(draft_lesson.id).is_published is True


def test_toggle_publish_forbidden_for_learner(client, learner, draft_lesson):
    _login(client, learner)
    resp = client.post(f"/admin/lessons/{draft_lesson.id}/publish")
    assert resp.status_code == 403
    assert Lesson.query.get(draft_lesson.id).is_published is False


def test_reorder_swaps_order_index(client, admin, db, published_lesson, draft_lesson):
    _login(client, admin)
    assert published_lesson.order_index == 1
    assert draft_lesson.order_index == 2

    client.post(f"/admin/lessons/{draft_lesson.id}/reorder/up", follow_redirects=True)

    db.session.refresh(published_lesson)
    db.session.refresh(draft_lesson)
    assert draft_lesson.order_index == 1
    assert published_lesson.order_index == 2


def test_reorder_at_top_is_a_noop(client, admin, published_lesson):
    _login(client, admin)
    resp = client.post(
        f"/admin/lessons/{published_lesson.id}/reorder/up", follow_redirects=True
    )
    assert b"already at the top" in resp.data


def test_reorder_rejects_invalid_direction(client, admin, published_lesson):
    _login(client, admin)
    resp = client.post(
        f"/admin/lessons/{published_lesson.id}/reorder/sideways", follow_redirects=True
    )
    assert b"Invalid reorder direction" in resp.data


def test_institution_crud_cycle(client, admin, db):
    _login(client, admin)

    resp = client.post(
        "/admin/institutions/new",
        data={
            "name": "New Broker",
            "description": "A test broker.",
            "url": "https://example.com",
            "category": "broker",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    inst = Institution.query.filter_by(name="New Broker").first()
    assert inst is not None

    client.post(
        f"/admin/institutions/{inst.id}/edit",
        data={
            "name": "Renamed Broker",
            "description": inst.description,
            "url": inst.url,
            "category": inst.category,
        },
        follow_redirects=True,
    )
    assert Institution.query.get(inst.id).name == "Renamed Broker"

    client.post(f"/admin/institutions/{inst.id}/delete", follow_redirects=True)
    assert Institution.query.get(inst.id) is None


def test_institution_crud_forbidden_for_learner(client, learner):
    _login(client, learner)
    resp = client.get("/admin/institutions/new")
    assert resp.status_code == 403
