"""Lessons blueprint: listing, detail, quiz, grading, progress (FR3-FR8)."""
from app.models import UserProgress


def _login(client, user):
    client.post("/auth/login", data={"email": user.email, "password": "correct-password"})


def test_list_shows_only_published_lessons(client, published_lesson, draft_lesson):
    resp = client.get("/lessons/")
    assert published_lesson.title.encode() in resp.data
    assert draft_lesson.title.encode() not in resp.data


def test_detail_visible_for_anonymous(client, published_lesson):
    resp = client.get(f"/lessons/{published_lesson.slug}")
    assert resp.status_code == 200
    assert published_lesson.title.encode() in resp.data


def test_detail_renders_markdown(client, published_lesson):
    resp = client.get(f"/lessons/{published_lesson.slug}")
    assert b"<strong>" in resp.data  # "**markdown**" in the fixture content


def test_draft_lesson_404s_for_anonymous(client, draft_lesson):
    resp = client.get(f"/lessons/{draft_lesson.slug}")
    assert resp.status_code == 404


def test_draft_lesson_404s_for_logged_in_learner(client, learner, draft_lesson):
    _login(client, learner)
    resp = client.get(f"/lessons/{draft_lesson.slug}")
    assert resp.status_code == 404


def test_draft_lesson_visible_to_admin(client, admin, draft_lesson):
    _login(client, admin)
    resp = client.get(f"/lessons/{draft_lesson.slug}")
    assert resp.status_code == 200


def test_unknown_slug_404s(client, db):
    resp = client.get("/lessons/does-not-exist")
    assert resp.status_code == 404


def test_quiz_requires_login(client, published_lesson):
    resp = client.get(f"/lessons/{published_lesson.slug}/quiz", follow_redirects=False)
    assert resp.status_code == 302


def test_quiz_page_lists_questions(client, learner, published_lesson):
    _login(client, learner)
    resp = client.get(f"/lessons/{published_lesson.slug}/quiz")
    assert resp.status_code == 200
    for q in published_lesson.questions:
        assert q.text.encode() in resp.data


def test_submit_quiz_grades_and_records_progress(client, learner, published_lesson):
    _login(client, learner)
    q1, q2 = published_lesson.questions
    correct_choice_q1 = next(c for c in q1.choices if c.is_correct)
    wrong_choice_q2 = next(c for c in q2.choices if not c.is_correct)

    resp = client.post(
        f"/lessons/{published_lesson.slug}/quiz",
        data={
            f"question-{q1.id}": str(correct_choice_q1.id),
            f"question-{q2.id}": str(wrong_choice_q2.id),
        },
    )
    assert resp.status_code == 200
    assert b"1 / 2" in resp.data

    progress = UserProgress.query.filter_by(
        user_id=learner.id, lesson_id=published_lesson.id
    ).first()
    assert progress is not None
    assert progress.completed is True
    assert progress.correct_count == 1
    assert progress.total_questions == 2
    assert progress.quiz_score_pct == 50


def test_resubmitting_quiz_overwrites_not_duplicates(client, learner, published_lesson):
    _login(client, learner)
    q1, q2 = published_lesson.questions
    correct1 = next(c for c in q1.choices if c.is_correct)
    correct2 = next(c for c in q2.choices if c.is_correct)
    wrong1 = next(c for c in q1.choices if not c.is_correct)

    client.post(
        f"/lessons/{published_lesson.slug}/quiz",
        data={f"question-{q1.id}": str(wrong1.id), f"question-{q2.id}": str(correct2.id)},
    )
    client.post(
        f"/lessons/{published_lesson.slug}/quiz",
        data={f"question-{q1.id}": str(correct1.id), f"question-{q2.id}": str(correct2.id)},
    )

    rows = UserProgress.query.filter_by(user_id=learner.id, lesson_id=published_lesson.id).all()
    assert len(rows) == 1
    assert rows[0].correct_count == 2


def test_calculator_defaults_and_clamps_input(client, db):
    resp = client.get("/lessons/calculator")
    assert resp.status_code == 200

    resp = client.get("/lessons/calculator?monthly_rwf=-500&months=0")
    assert resp.status_code == 200  # clamped, not a 500


def test_calculate_progress_counts_only_published_completed(client, learner, published_lesson, draft_lesson):
    from app.lessons.utils import calculate_progress

    result = calculate_progress(learner)
    assert result["total"] == 1  # draft_lesson excluded
    assert result["completed"] == 0
