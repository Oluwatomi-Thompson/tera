from flask import jsonify, request

from app.api import bp
from app.api.schemas import parse_calculator_request
from app.lessons.utils import project_compound_growth


@bp.post("/calculator")
def calculator():
    """Used by static/js/calculator.js so the lessons/calculator.html page
    can update the projection live as the learner drags the sliders, without
    a full page reload. The server-rendered GET /lessons/calculator route
    still works standalone (progressive enhancement, not a hard dependency
    on JS)."""
    try:
        monthly_rwf, months, annual_rate = parse_calculator_request(request.get_json(silent=True) or {})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(project_compound_growth(monthly_rwf, months, annual_rate))
