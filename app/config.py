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
    """
    No fallback for SECRET_KEY/DATABASE_URL — but read lazily via init_app(),
    not as class attributes. A class attribute here would be evaluated the
    moment this module is *imported* (e.g. `from app.config import DevConfig`
    at the top of app/__init__.py), which would crash DevConfig/TestConfig
    runs too, since Python imports the whole module regardless of which
    class is actually used. init_app() only runs when ProdConfig itself is
    selected, so the loud failure happens exactly when it should: a real
    deploy missing its env vars, not `flask run` locally.
    """
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
        url = os.environ["DATABASE_URL"]
        # Hosts may hand out "postgres://" (rejected by SQLAlchemy) or a bare
        # "postgresql://" (SQLAlchemy 2.1 defaults that to psycopg v3, but we
        # ship psycopg2). Pin the driver we actually install.
        for prefix in ("postgres://", "postgresql://"):
            if url.startswith(prefix):
                url = "postgresql+psycopg2://" + url[len(prefix):]
                break
        app.config["SQLALCHEMY_DATABASE_URI"] = url

        # Free Postgres hosts drop idle connections (and the app itself
        # sleeps after 15 idle minutes), so test each pooled connection
        # before using it instead of failing the first request after a nap.
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

        # The site is served over HTTPS in production: keep the login and
        # "remember me" cookies off plain HTTP and away from page scripts.
        app.config["SESSION_COOKIE_SECURE"] = True
        app.config["SESSION_COOKIE_HTTPONLY"] = True
        app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
        app.config["REMEMBER_COOKIE_SECURE"] = True
        app.config["REMEMBER_COOKIE_HTTPONLY"] = True
        app.config["REMEMBER_COOKIE_SAMESITE"] = "Lax"

        # The host's load balancer terminates HTTPS and forwards plain HTTP
        # to gunicorn. Trust its X-Forwarded-* headers (one proxy hop) so
        # Flask knows the real scheme and host.
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
