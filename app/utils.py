"""
Small app-wide helpers that don't belong to one blueprint.
"""
from functools import wraps

import markdown as _markdown
from flask import abort
from flask_login import current_user


def render_markdown(text: str) -> str:
    """Jinja filter: `{{ lesson.content_body | render_markdown }}`.

    lessons.content_body stores RAW markdown (the single source of truth
    lives in app/content/lessons/*.md — see ai-context/08-decisions.md,
    ADR-004). We convert to HTML at render time instead of at seed time so
    the DB never holds a second, driftable copy of the rendered output.
    """
    if not text:
        return ""
    return _markdown.markdown(text, extensions=["fenced_code", "tables"])


def admin_required(view):
    """Route decorator: 403s anyone who isn't logged in as an admin.

    Use *after* @login_required so an anonymous visitor gets redirected to
    login first (nicer UX) rather than a bare 403.
    """

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapped
