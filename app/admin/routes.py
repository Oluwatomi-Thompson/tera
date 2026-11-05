from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from app.admin import bp
from app.admin.forms import InstitutionForm
from app.commands import seed_all, sync_report
from app.extensions import db
from app.models import Institution, Lesson
from app.utils import admin_required


# Scope note: lesson CONTENT is authored in app/content/lessons/*.md and
# loaded via `flask seed-db` / the Resync button below (see
# ai-context/08-decisions.md, ADR-004). This blueprint does NOT edit
# content_body — it manages what has no natural home in a .md file.


@bp.get("/")
@login_required
@admin_required
def dashboard():
    lessons = Lesson.query.order_by(Lesson.order_index).all()
    institutions = Institution.query.order_by(Institution.category, Institution.name).all()
    report = sync_report()
    return render_template(
        "admin/dashboard.html", lessons=lessons, institutions=institutions, report=report
    )


@bp.post("/lessons/<int:lesson_id>/publish")
@login_required
@admin_required
def toggle_publish(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    lesson.is_published = not lesson.is_published
    db.session.commit()
    flash(f"'{lesson.title}' is now {'published' if lesson.is_published else 'unpublished'}.", "success")
    return redirect(url_for("admin.dashboard"))


@bp.post("/lessons/<int:lesson_id>/reorder/<direction>")
@login_required
@admin_required
def reorder_lesson(lesson_id, direction):
    """Swap this lesson's order_index with its neighbor's — keeps
    order_index unique at all times (the DB constraint requires it) instead
    of renumbering the whole list on every move."""
    if direction not in ("up", "down"):
        flash("Invalid reorder direction.", "error")
        return redirect(url_for("admin.dashboard"))

    lesson = Lesson.query.get_or_404(lesson_id)
    neighbor_query = Lesson.query.filter(
        Lesson.order_index < lesson.order_index
        if direction == "up"
        else Lesson.order_index > lesson.order_index
    ).order_by(Lesson.order_index.desc() if direction == "up" else Lesson.order_index.asc())
    neighbor = neighbor_query.first()

    if neighbor is None:
        flash(f"'{lesson.title}' is already at the {'top' if direction == 'up' else 'bottom'}.", "info")
        return redirect(url_for("admin.dashboard"))

    # order_index is UNIQUE and SQLite enforces that immediately (not
    # deferred), so writing both new values in one flush can collide with
    # whatever value is still on the *other* row at the instant either
    # single UPDATE executes. Route one side through a temporary value
    # that can't collide with anything, flushing between steps, then land
    # both rows on their final values in a last flush.
    lesson_target, neighbor_target = neighbor.order_index, lesson.order_index
    lesson.order_index = -1
    db.session.flush()
    neighbor.order_index = neighbor_target
    db.session.flush()
    lesson.order_index = lesson_target
    db.session.commit()
    return redirect(url_for("admin.dashboard"))


@bp.post("/resync")
@login_required
@admin_required
def resync():
    """Runs the same upsert `flask seed-db` does, triggered from the UI
    instead of a shell — for when you've edited a .md file and want it live
    without SSH access to wherever this is deployed."""
    count = seed_all()
    flash(f"Resynced {count} lesson file(s) from app/content/lessons/.", "success")
    return redirect(url_for("admin.dashboard"))


@bp.route("/institutions/new", methods=["GET", "POST"])
@login_required
@admin_required
def new_institution():
    form = InstitutionForm()
    if form.validate_on_submit():
        institution = Institution(
            name=form.name.data,
            description=form.description.data,
            url=form.url.data,
            category=form.category.data,
        )
        db.session.add(institution)
        db.session.commit()
        flash(f"Added '{institution.name}' to the directory.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/institution_form.html", form=form, institution=None)


@bp.route("/institutions/<int:institution_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_institution(institution_id):
    institution = Institution.query.get_or_404(institution_id)
    form = InstitutionForm(obj=institution)
    if form.validate_on_submit():
        form.populate_obj(institution)
        db.session.commit()
        flash(f"Updated '{institution.name}'.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/institution_form.html", form=form, institution=institution)


@bp.post("/institutions/<int:institution_id>/delete")
@login_required
@admin_required
def delete_institution(institution_id):
    institution = Institution.query.get_or_404(institution_id)
    db.session.delete(institution)
    db.session.commit()
    flash(f"Removed '{institution.name}' from the directory.", "info")
    return redirect(url_for("admin.dashboard"))
