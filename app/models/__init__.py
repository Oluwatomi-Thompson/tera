# Import every model here so Alembic (flask-migrate) can detect them.
from app.models.user import User, UserRole  # noqa: F401
from app.models.lesson import Lesson  # noqa: F401
from app.models.question import Question, Choice  # noqa: F401
from app.models.progress import UserProgress  # noqa: F401
from app.models.institution import Institution  # noqa: F401
