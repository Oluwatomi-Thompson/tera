"""
Shared pytest fixtures. TestConfig (app/config.py) points at an in-memory
SQLite DB and disables CSRF, so each test gets a fresh schema with no files
touched on disk and no need to fight Flask-WTF's CSRF token in test clients.
"""
from __future__ import annotations

import pytest

from app import create_app
from app.config import TestConfig
from app.extensions import db as _db
from app.models import Institution, Lesson, Question, Choice, User, UserRole


@pytest.fixture()
def app():
    application = create_app(TestConfig)

    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def db(app):
    return _db


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def learner(db):
    """A registered, non-admin user — the common case for most tests."""
    user = User(email="learner@example.com", role=UserRole.LEARNER)
    user.set_password("correct-password")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def admin(db):
    user = User(email="admin@example.com", role=UserRole.ADMIN)
    user.set_password("correct-password")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def published_lesson(db):
    """One published lesson with a 2-question quiz — enough to exercise
    detail/quiz/submit_quiz/progress without needing the real markdown
    content pipeline in every test."""
    lesson = Lesson(
        slug="test-lesson",
        title="Test Lesson",
        order_index=1,
        content_body="Some **markdown** content.",
        is_published=True,
    )
    q1 = Question(
        text="2 + 2?",
        order_index=1,
        choices=[
            Choice(text="3", is_correct=False),
            Choice(text="4", is_correct=True),
        ],
    )
    q2 = Question(
        text="Capital of Rwanda?",
        order_index=2,
        choices=[
            Choice(text="Kigali", is_correct=True),
            Choice(text="Nairobi", is_correct=False),
        ],
    )
    lesson.questions = [q1, q2]
    db.session.add(lesson)
    db.session.commit()
    return lesson


@pytest.fixture()
def draft_lesson(db):
    lesson = Lesson(
        slug="draft-lesson",
        title="Draft Lesson",
        order_index=2,
        content_body="Not fact-checked yet.",
        is_published=False,
    )
    db.session.add(lesson)
    db.session.commit()
    return lesson


@pytest.fixture()
def institution(db):
    inst = Institution(
        name="Test Regulator",
        description="A test institution.",
        url="https://example.com",
        category="regulator",
    )
    db.session.add(inst)
    db.session.commit()
    return inst


def login(client, email, password):
    return client.post(
        "/auth/login", data={"email": email, "password": password}, follow_redirects=True
    )
