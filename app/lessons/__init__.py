from flask import Blueprint

bp = Blueprint("lessons", __name__)

from app.lessons import routes  # noqa: E402,F401
