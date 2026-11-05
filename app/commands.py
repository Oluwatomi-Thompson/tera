"""
CLI commands, plus the seeding/sync-check logic the admin panel reuses.

`flask seed-db` (and the admin "Resync" button, which calls the same
`seed_all()`) make app/content/lessons/*.md the single source of truth for
lesson + quiz content. Upserts by `slug`, so re-running it after editing a
.md file updates the matching DB row instead of creating a duplicate. The
admin panel is NOT expected to edit content_body directly — see
ai-context/08-decisions.md (ADR-004) for why, and app/admin/routes.py for
what the admin panel does instead.
"""
from __future__ import annotations

import re
from pathlib import Path

import click
import yaml
from flask.cli import with_appcontext

CONTENT_DIR = Path(__file__).parent / "content" / "lessons"

QUESTION_RE = re.compile(r"^\d+\.\s+(?P<question>.+)$")
CHOICE_RE = re.compile(r"^\s*-\s*\[(?P<mark>[ xX])\]\s*(?P<choice>.+)$")


def _parse_lesson_file(path: Path) -> tuple[dict, str, list[dict]]:
    """
    Returns (frontmatter_dict, content_markdown, questions) where questions is
    [{"text": ..., "order_index": ..., "choices": [{"text": ..., "is_correct": bool}, ...]}]

    Expects the format in app/content/lessons/_TEMPLATE.md:
    ---
    slug: what-is-investing
    order: 1
    title: "..."
    is_published: false
    objective: "..."
    sources:
      - "..."
    ---
    ## Content
    ...
    ## Quiz
    1. Question?
       - [ ] wrong
       - [x] right
    """
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise ValueError(f"{path.name}: missing YAML frontmatter (must start with '---')")

    _, fm_raw, body = raw.split("---", 2)
    meta = yaml.safe_load(fm_raw) or {}

    for required in ("slug", "order", "title"):
        if required not in meta:
            raise ValueError(f"{path.name}: frontmatter missing required field '{required}'")

    content_match = re.search(r"##\s*Content\s*\n(.*?)(?=\n##\s*Quiz|\Z)", body, re.S)
    quiz_match = re.search(r"##\s*Quiz\s*\n(.*)", body, re.S)

    content_md = content_match.group(1).strip() if content_match else body.strip()
    questions: list[dict] = []

    if quiz_match:
        current = None
        order_index = 0
        for line in quiz_match.group(1).splitlines():
            q = QUESTION_RE.match(line)
            c = CHOICE_RE.match(line)
            if q:
                order_index += 1
                current = {"text": q.group("question").strip(), "order_index": order_index, "choices": []}
                questions.append(current)
            elif c and current is not None:
                current["choices"].append(
                    {
                        "text": c.group("choice").strip(),
                        "is_correct": c.group("mark").lower() == "x",
                    }
                )

    return meta, content_md, questions


def _lesson_files() -> list[Path]:
    return sorted(f for f in CONTENT_DIR.glob("*.md") if not f.name.startswith("_"))


def _lesson_differs(lesson, meta, content_md, questions) -> bool:
    """True if the DB row would change if we seeded this file right now —
    powers the admin "needs resync" indicator without duplicating a hash
    column that could itself go stale."""
    if lesson is None:
        return True
    if lesson.title != meta["title"]:
        return True
    if lesson.order_index != meta["order"]:
        return True
    if (lesson.content_body or "").strip() != content_md.strip():
        return True
    if len(lesson.questions) != len(questions):
        return True
    for existing_q, new_q in zip(lesson.questions, questions):
        if existing_q.text.strip() != new_q["text"].strip():
            return True
        if len(existing_q.choices) != len(new_q["choices"]):
            return True
        for existing_c, new_c in zip(existing_q.choices, new_q["choices"]):
            if existing_c.text.strip() != new_c["text"].strip() or existing_c.is_correct != new_c["is_correct"]:
                return True
    return False


def sync_report() -> list[dict]:
    """One row per .md file for the admin dashboard: does the DB match the
    file right now, or does someone need to hit "Resync"?"""
    from app.models import Lesson

    report = []
    for path in _lesson_files():
        try:
            meta, content_md, questions = _parse_lesson_file(path)
        except ValueError as exc:
            report.append({"path": path.name, "error": str(exc)})
            continue

        lesson = Lesson.query.filter_by(slug=meta["slug"]).first()
        report.append(
            {
                "path": path.name,
                "slug": meta["slug"],
                "title": meta["title"],
                "lesson": lesson,
                "is_stale": _lesson_differs(lesson, meta, content_md, questions),
                "question_count": len(questions),
            }
        )
    return report


def seed_all() -> int:
    """Upsert Lesson/Question/Choice rows from app/content/lessons/*.md by
    slug. Returns the number of files processed. Shared by `flask seed-db`
    and the admin panel's "Resync" button (app/admin/routes.py)."""
    from app.extensions import db
    from app.models import Choice, Lesson, Question

    files = _lesson_files()
    parsed = []  # [(lesson, meta, content_md, questions, source_path), ...]

    for path in files:
        try:
            meta, content_md, questions = _parse_lesson_file(path)
        except ValueError:
            continue  # already surfaced via sync_report()/CLI error output

        lesson = Lesson.query.filter_by(slug=meta["slug"]).first()
        if lesson is None:
            lesson = Lesson(slug=meta["slug"])
            db.session.add(lesson)
        source_path = str(path.relative_to(CONTENT_DIR.parent.parent.parent))
        parsed.append((lesson, meta, content_md, questions, source_path))

    # order_index is UNIQUE, and the admin panel's reorder control (see
    # app/admin/routes.py) can leave the DB's current values out of sync
    # with each file's `order:` frontmatter — e.g. an admin moved lesson A
    # above lesson B without touching their .md files. Writing the files'
    # target order_index values directly, one lesson at a time, then
    # collides with whatever the *next* lesson in the loop still holds,
    # because SQLAlchemy autoflushes the pending UPDATE as soon as the next
    # iteration's `Lesson.query.filter_by(...)` runs.
    #
    # Fix: stage every touched lesson onto a disjoint negative placeholder
    # first (can't collide with any real value or each other) and flush
    # that as its own step, then apply the real target values in a second
    # pass. Markdown stays authoritative — this only changes the order in
    # which writes land, not which values win.
    for i, (lesson, *_rest) in enumerate(parsed, start=1):
        lesson.order_index = -i
    db.session.flush()

    for lesson, meta, content_md, questions, source_path in parsed:
        lesson.title = meta["title"]
        lesson.order_index = meta["order"]
        lesson.content_body = content_md
        lesson.is_published = bool(meta.get("is_published", False))
        lesson.source_path = source_path

        # Replace questions/choices wholesale on every seed — simplest
        # correct behavior given markdown is authoritative; fine at this
        # content scale.
        lesson.questions = [
            Question(
                text=q["text"],
                order_index=q["order_index"],
                choices=[Choice(text=c["text"], is_correct=c["is_correct"]) for c in q["choices"]],
            )
            for q in questions
        ]

    db.session.commit()
    return len(parsed)


def seed_institutions() -> int:
    """Upsert Institution rows from app/content/institutions.yaml, matched
    by `name`. Institutions are NOT authored in the admin panel's Lesson
    sense — see ADR-004 — but seeding from a checked-in file still beats
    typing them into the DB by hand for the initial set; the admin CRUD
    form (app/admin/forms.py) is for day-to-day edits after that."""
    from app.extensions import db
    from app.models import Institution

    path = Path(__file__).parent / "content" / "institutions.yaml"
    if not path.exists():
        return 0

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    count = 0
    for row in data:
        inst = Institution.query.filter_by(name=row["name"]).first()
        if inst is None:
            inst = Institution(name=row["name"])
            db.session.add(inst)
        inst.description = row.get("description", "")
        inst.url = row["url"]
        inst.category = row.get("category")
        count += 1

    db.session.commit()
    return count


@click.command("seed-db")
@with_appcontext
def seed_db_command():
    """Upsert lessons (from markdown) and institutions (from yaml)."""
    n_lessons = seed_all()
    click.echo(f"Seeded {n_lessons} lesson file(s) from {CONTENT_DIR}.")
    n_inst = seed_institutions()
    click.echo(f"Seeded {n_inst} institution(s).")


@click.command("create-admin")
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@with_appcontext
def create_admin_command(email, password):
    """Create (or promote) a user as admin — the one piece of setup there's
    no self-serve UI for on purpose, since anyone could otherwise register
    their way into the admin panel."""
    from app.extensions import db
    from app.models import User, UserRole

    user = User.query.filter_by(email=email.lower()).first()
    if user is None:
        user = User(email=email.lower(), role=UserRole.ADMIN)
        user.set_password(password)
        db.session.add(user)
        click.echo(f"Created admin user {email}.")
    else:
        user.role = UserRole.ADMIN
        user.set_password(password)
        click.echo(f"Promoted existing user {email} to admin and reset their password.")
    db.session.commit()


@click.command("reset-progress")
@with_appcontext
def reset_progress_command():
    """Dev convenience only: wipes every UserProgress row so you can retest
    the quiz/dashboard flow without recreating the whole DB."""
    from app.extensions import db
    from app.models import UserProgress

    count = UserProgress.query.delete()
    db.session.commit()
    click.echo(f"Deleted {count} progress record(s).")
