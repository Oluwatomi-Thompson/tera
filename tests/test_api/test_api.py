"""API blueprint: POST /api/v1/calculator (used by static/js/calculator.js)."""


def test_calculator_api_default_payload(client):
    resp = client.post("/api/v1/calculator", json={})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["monthly_rwf"] == 2000
    assert body["months"] == 24
    assert len(body["schedule"]) == 24


def test_calculator_api_custom_payload(client):
    resp = client.post(
        "/api/v1/calculator", json={"monthly_rwf": 5000, "months": 12, "annual_rate": 0.05}
    )
    body = resp.get_json()
    assert body["total_contributed"] == 60000
    assert body["total_value"] > body["total_contributed"]


def test_calculator_api_rejects_out_of_range_months(client):
    resp = client.post("/api/v1/calculator", json={"months": 1000})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_calculator_api_rejects_non_numeric(client):
    resp = client.post("/api/v1/calculator", json={"monthly_rwf": "a lot"})
    assert resp.status_code == 400


def test_calculator_api_rejects_non_object_body(client):
    resp = client.post("/api/v1/calculator", json=[1, 2, 3])
    assert resp.status_code == 400
