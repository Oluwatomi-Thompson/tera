"""
Pure-ish helper functions for the lessons blueprint: progress calculation,
quiz grading, and the compound-growth calculator (FR7, FR6, FR8).

Kept here instead of inline in routes.py so they're independently testable
without spinning up a request.
"""
from __future__ import annotations

from app.models import Lesson, UserProgress


def calculate_progress(user) -> dict:
    """Returns a learner's overall progress across published lessons (FR7)."""
    total = Lesson.query.filter_by(is_published=True).count()
    if total == 0:
        return {"completed": 0, "total": 0, "percent": 0}

    completed = (
        UserProgress.query.filter_by(user_id=user.id, completed=True)
        .join(Lesson)
        .filter(Lesson.is_published.is_(True))
        .count()
    )
    return {
        "completed": completed,
        "total": total,
        "percent": round(100 * completed / total),
    }


def grade_quiz(lesson, submitted_answers: dict[str, str]) -> dict:
    """Grade a quiz submission.

    `submitted_answers` maps str(question_id) -> str(choice_id), the shape
    Flask's `request.form` naturally gives us for fields named
    `question-<id>`.

    Returns {"correct_count", "total_questions", "results": [...]} where each
    result row carries enough for the template to show right/wrong + the
    correct answer without a second query.
    """
    results = []
    correct_count = 0

    for question in lesson.questions:
        selected_id = submitted_answers.get(str(question.id))
        correct_choice = next((c for c in question.choices if c.is_correct), None)
        is_correct = bool(selected_id) and selected_id.isdigit() and int(selected_id) == (
            correct_choice.id if correct_choice else None
        )
        if is_correct:
            correct_count += 1

        results.append(
            {
                "question": question,
                "selected_choice_id": int(selected_id) if selected_id and selected_id.isdigit() else None,
                "correct_choice_id": correct_choice.id if correct_choice else None,
                "is_correct": is_correct,
            }
        )

    return {
        "correct_count": correct_count,
        "total_questions": len(lesson.questions),
        "results": results,
    }


def project_compound_growth(
    monthly_rwf: float, months: int, annual_rate: float = 0.10
) -> dict:
    """What could `monthly_rwf` contributed every month become? (FR8)

    Simple monthly-compounding model: interest accrues on the running
    balance each month, then that month's contribution is added. This is an
    illustrative projection, not a guaranteed return — the template must
    make that caveat visible next to the number (NFR3/safety requirement in
    the SRS), since nothing here is an actual investment product.
    """
    monthly_rate = annual_rate / 12
    balance = 0.0
    schedule = []

    for month in range(1, months + 1):
        balance = balance * (1 + monthly_rate) + monthly_rwf
        schedule.append({"month": month, "balance": round(balance)})

    total_contributed = monthly_rwf * months
    total_value = round(balance)

    return {
        "schedule": schedule,
        "total_contributed": round(total_contributed),
        "total_value": total_value,
        "growth": total_value - round(total_contributed),
        "annual_rate": annual_rate,
        "months": months,
        "monthly_rwf": monthly_rwf,
    }
