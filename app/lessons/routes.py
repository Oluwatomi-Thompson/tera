from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.lessons import bp
from app.lessons.utils import calculate_progress, grade_quiz, project_compound_growth
from app.models import Lesson, UserProgress


def _get_visible_lesson_or_404(slug: str) -> Lesson:
    """A draft lesson (is_published=False) is 404 to everyone except admins,
    so a half-written lesson never leaks to a learner who guesses/bookmarks
    its URL — same behavior whether they're logged out or logged in."""
    lesson = Lesson.query.filter_by(slug=slug).first_or_404()
    if not lesson.is_published and not (current_user.is_authenticated and current_user.is_admin):
        abort(404)
    return lesson


@bp.get("/")
def list_lessons():
    """FR3: ordered lesson list, with each lesson's completion state for the
    signed-in learner so the list doubles as a lightweight progress view."""
    lessons = Lesson.query.filter_by(is_published=True).order_by(Lesson.order_index).all()

    progress_by_lesson = {}
    if current_user.is_authenticated:
        rows = UserProgress.query.filter_by(user_id=current_user.id).all()
        progress_by_lesson = {row.lesson_id: row for row in rows}

    return render_template("lessons/list.html", lessons=lessons, progress_by_lesson=progress_by_lesson)


@bp.get("/<slug>")
def detail(slug):
    """FR4: full lesson content, rendered from markdown at request time."""
    lesson = _get_visible_lesson_or_404(slug)

    progress = None
    if current_user.is_authenticated:
        progress = UserProgress.query.filter_by(
            user_id=current_user.id, lesson_id=lesson.id
        ).first()

    return render_template("lessons/detail.html", lesson=lesson, progress=progress)


@bp.get("/<slug>/quiz")
@login_required
def quiz(slug):
    """FR5: quiz-taking view. Login required since a result has to be saved
    to *someone* — there's no meaningful anonymous quiz attempt here."""
    lesson = _get_visible_lesson_or_404(slug)
    if not lesson.questions:
        flash("This lesson doesn't have a quiz yet.", "info")
        return redirect(url_for("lessons.detail", slug=slug))

    return render_template("lessons/quiz.html", lesson=lesson)


@bp.post("/<slug>/quiz")
@login_required
def submit_quiz(slug):
    """FR6 + FR7: grade the submission and upsert the learner's UserProgress
    row (one per user per lesson — resubmitting a quiz overwrites the
    previous attempt's score rather than creating a duplicate)."""
    lesson = _get_visible_lesson_or_404(slug)
    if not lesson.questions:
        abort(404)

    submitted = {
        key.removeprefix("question-"): value
        for key, value in request.form.items()
        if key.startswith("question-")
    }
    result = grade_quiz(lesson, submitted)

    progress = UserProgress.query.filter_by(
        user_id=current_user.id, lesson_id=lesson.id
    ).first()
    if progress is None:
        progress = UserProgress(user_id=current_user.id, lesson_id=lesson.id)
        db.session.add(progress)

    progress.completed = True
    progress.correct_count = result["correct_count"]
    progress.total_questions = result["total_questions"]
    from datetime import datetime

    progress.completed_at = datetime.utcnow()
    db.session.commit()

    return render_template("lessons/result.html", lesson=lesson, result=result, progress=progress)


@bp.get("/calculator")
def calculator():
    """FR8: compound-growth calculator. Public — no account needed to play
    with the numbers, since this is meant to hook curiosity, not gate it."""
    monthly_rwf = request.args.get("monthly_rwf", default=2000, type=int)
    months = request.args.get("months", default=24, type=int)

    monthly_rwf = max(0, min(monthly_rwf, 10_000_000))
    months = max(1, min(months, 480))  # cap at 40 years, keeps the chart sane

    projection = project_compound_growth(monthly_rwf, months)
    return render_template("lessons/calculator.html", projection=projection)
