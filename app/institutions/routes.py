from flask import render_template, request

from app.institutions import bp
from app.institutions.utils import CATEGORY_LABELS, filter_by_category
from app.models import Institution


@bp.get("/")
def directory():
    """FR9: the funnel's destination — real, licensed institutions, not a
    Tera product. Every page in this blueprint should read as "go here
    next," never as "do this inside Tera."""
    category = request.args.get("category")
    institutions = filter_by_category(category)
    return render_template(
        "institutions/directory.html",
        institutions=institutions,
        categories=CATEGORY_LABELS,
        active_category=category,
    )


@bp.get("/<int:institution_id>")
def detail(institution_id):
    institution = Institution.query.get_or_404(institution_id)
    return render_template("institutions/detail.html", institution=institution)
