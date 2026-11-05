"""Institutions blueprint: resource directory (FR9)."""
from app.models import Institution


def test_directory_lists_institutions(client, institution):
    resp = client.get("/institutions/")
    assert resp.status_code == 200
    assert institution.name.encode() in resp.data


def test_directory_filters_by_category(client, db):
    reg = Institution(name="Reg Co", url="https://example.com", category="regulator")
    broker = Institution(name="Broker Co", url="https://example.com", category="broker")
    db.session.add_all([reg, broker])
    db.session.commit()

    resp = client.get("/institutions/?category=regulator")
    assert b"Reg Co" in resp.data
    assert b"Broker Co" not in resp.data


def test_directory_ignores_unknown_category(client, institution):
    resp = client.get("/institutions/?category=not-a-real-category")
    assert resp.status_code == 200
    assert institution.name.encode() in resp.data


def test_detail_page(client, institution):
    resp = client.get(f"/institutions/{institution.id}")
    assert resp.status_code == 200
    assert institution.name.encode() in resp.data


def test_detail_404_for_unknown_id(client, db):
    resp = client.get("/institutions/99999")
    assert resp.status_code == 404
