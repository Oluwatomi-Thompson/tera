"""
Request/response shapes for the API blueprint. Kept as plain functions
rather than a schema library (Marshmallow etc.) — the surface area here is
one endpoint, so a dependency for validation would be heavier than the
problem.

POST /api/v1/calculator
  Request JSON:  {"monthly_rwf": int, "months": int, "annual_rate": float?}
  Response JSON: {"schedule": [{"month": int, "balance": int}, ...],
                   "total_contributed": int, "total_value": int,
                   "growth": int, "annual_rate": float, "months": int,
                   "monthly_rwf": int}
  Errors: 400 {"error": "..."} for bad/missing input.
"""


def parse_calculator_request(payload: dict) -> tuple[int, int, float]:
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")

    try:
        monthly_rwf = int(payload.get("monthly_rwf", 2000))
        months = int(payload.get("months", 24))
    except (TypeError, ValueError):
        raise ValueError("monthly_rwf and months must be numbers.")

    annual_rate = payload.get("annual_rate", 0.10)
    try:
        annual_rate = float(annual_rate)
    except (TypeError, ValueError):
        raise ValueError("annual_rate must be a number.")

    if monthly_rwf < 0 or monthly_rwf > 10_000_000:
        raise ValueError("monthly_rwf must be between 0 and 10,000,000.")
    if months < 1 or months > 480:
        raise ValueError("months must be between 1 and 480.")
    if annual_rate < 0 or annual_rate > 1:
        raise ValueError("annual_rate must be between 0 and 1 (e.g. 0.10 for 10%).")

    return monthly_rwf, months, annual_rate
