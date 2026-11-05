"""
Config classes for each environment.
"""
import os
import secrets

from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# A dev-only fallback so `flask run` works right after cloning without an
# .env file. Never relied on in production — ProdConfig has no default and
# will error loudly if SECRET_KEY isn't set in the real environment.
_DEV_FALLBACK_SECRET = secrets.token_hex(16)


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", _DEV_FALLBACK_SECRET)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, '..', 'dev.db')}"
    )


class ProdConfig(BaseConfig):
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
        db_url = os.environ["DATABASE_URL"]
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
