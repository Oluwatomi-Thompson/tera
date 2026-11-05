from flask import Blueprint

bp = Blueprint("institutions", __name__)

from app.institutions import routes  # noqa: E402,F401
