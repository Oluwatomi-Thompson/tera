"""
Replaces the old quizzes table: a lesson's questions ARE its quiz, so
Question points straight at Lesson. If you ever need multiple quizzes per
lesson or per-quiz settings, reintroduce a quizzes table then — cheap
migration, not worth paying for now.
"""
from app.extensions import db


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(
        db.Integer, db.ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    text = db.Column(db.Text, nullable=False)
    order_index = db.Column(db.Integer)

    lesson = db.relationship("Lesson", back_populates="questions")
    choices = db.relationship(
        "Choice", back_populates="question", cascade="all, delete-orphan", order_by="Choice.id"
    )

    def __repr__(self) -> str:
        return f"<Question {self.id} lesson={self.lesson_id}>"


class Choice(db.Model):
    __tablename__ = "choices"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)

    question = db.relationship("Question", back_populates="choices")

    def __repr__(self) -> str:
        return f"<Choice {self.id} correct={self.is_correct}>"
