from app.extensions import db


class UserProgress(db.Model):
    __tablename__ = "user_progress"
    __table_args__ = (
        db.UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson_progress"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id = db.Column(
        db.Integer, db.ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    completed = db.Column(db.Boolean, nullable=False, default=False)

    # Split out instead of a bare quiz_score int, so a score still means
    # something if the number of questions in a lesson's quiz ever changes.
    correct_count = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    completed_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="progress")
    lesson = db.relationship("Lesson", back_populates="progress_records")

    @property
    def quiz_score_pct(self):
        if not self.total_questions:
            return None
        return round(100 * self.correct_count / self.total_questions)

    def __repr__(self) -> str:
        return f"<UserProgress user={self.user_id} lesson={self.lesson_id}>"
