"""
InstitutionForm — Institutions are NOT sourced from markdown (see ADR-004),
so this one *is* a real CRUD form, unlike lessons.

No LessonForm / QuestionForm here on purpose — lesson content is authored
in app/content/lessons/*.md, not through the admin panel. The admin panel's
lesson-related powers are: publish/unpublish, reorder, and resync (see
routes.py).
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, URL

CATEGORY_CHOICES = [
    ("regulator", "Regulator"),
    ("exchange", "Exchange"),
    ("unit_trust", "Unit Trust"),
    ("broker", "Licensed Broker"),
]


class InstitutionForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    description = TextAreaField("Description", validators=[Optional()])
    url = StringField("Website URL", validators=[DataRequired(), URL()])
    category = SelectField("Category", choices=CATEGORY_CHOICES, validators=[DataRequired()])
