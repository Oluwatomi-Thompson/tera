# API Contract

The current API blueprint contains one endpoint. It is used by the calculator page for live updates; the regular server-rendered calculator route remains available as a fallback.

## `POST /api/v1/calculator`

**Request:** JSON object. All keys are optional; defaults are applied server-side.

| Key | Type | Default | Accepted range |
|---|---|---:|---|
| `monthly_rwf` | integer-coercible number | `2000` | 0–10,000,000 |
| `months` | integer-coercible number | `24` | 1–480 |
| `annual_rate` | number | `0.10` | 0–1 (e.g. `0.10` means 10%) |

Example:

```json
{"monthly_rwf": 5000, "months": 12, "annual_rate": 0.05}
```

**Success (`200`):**

```json
{
  "schedule": [{"month": 1, "balance": 5021}],
  "total_contributed": 60000,
  "total_value": 61500,
  "growth": 1500,
  "annual_rate": 0.05,
  "months": 12,
  "monthly_rwf": 5000
}
```

The numbers above illustrate the response shape only. Actual `schedule` contains one row per month; values depend on inputs and the compound-growth calculation in `app/lessons/utils.py`.

**Invalid input (`400`):** `{"error": "..."}`. Examples include non-object JSON, non-numeric values, and values outside the accepted ranges. Missing or invalid JSON is treated as an empty object by the route, so defaults are used for that case.

**Implementation:** `app/api/routes.py`, validation in `app/api/schemas.py`, tests in `tests/test_api/test_api.py`. No other API endpoints are currently registered in this blueprint. The calculator is an educational illustration, not a guaranteed return estimate or financial recommendation.
