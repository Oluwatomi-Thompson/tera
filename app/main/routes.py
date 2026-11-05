from flask import render_template
from flask_login import current_user, login_required

from app.lessons.utils import calculate_progress
from app.main import bp
from app.models import Lesson


@bp.get("/")
def index():
    lesson_count = Lesson.query.filter_by(is_published=True).count()
    return render_template("main/index.html", lesson_count=lesson_count)


@bp.get("/about")
def about():
    return render_template("main/about.html")


@bp.get("/dashboard")
@login_required
def dashboard():
    progress = calculate_progress(current_user)
    lessons = Lesson.query.filter_by(is_published=True).order_by(Lesson.order_index).all()

    from app.models import UserProgress

    progress_by_lesson = {
        row.lesson_id: row
        for row in UserProgress.query.filter_by(user_id=current_user.id).all()
    }

    return render_template(
        "main/dashboard.html",
        progress=progress,
        lessons=lessons,
        progress_by_lesson=progress_by_lesson,
    )
