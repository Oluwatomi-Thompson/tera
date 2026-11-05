from datetime import datetime

from app.extensions import db


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    order_index = db.Column(db.Integer, nullable=False, unique=True)
    content_body = db.Column(db.Text)  # raw markdown, seeded from app/content/lessons/*.md
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # source_path: which .md file this row was last seeded from — makes the
    # "resync" admin view possible without guessing filenames from titles.
    source_path = db.Column(db.String(500))

    questions = db.relationship(
        "Question",
        back_populates="lesson",
        cascade="all, delete-orphan",
        order_by="Question.order_index",
    )
    progress_records = db.relationship(
        "UserProgress", back_populates="lesson", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Lesson {self.slug}>"
