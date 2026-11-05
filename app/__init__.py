from datetime import datetime

from flask import Flask, render_template

from app.config import DevConfig
from app.extensions import db, login_manager, migrate


def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    if hasattr(config_class, "init_app"):
        config_class.init_app(app)

    _init_extensions(app)
    _register_blueprints(app)
    _register_cli(app)
    _register_error_handlers(app)
    _register_template_helpers(app)

    return app


def _init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import models so they're registered with SQLAlchemy/Alembic before
    # `flask db migrate` runs.
    from app import models  # noqa: F401


def _register_blueprints(app):
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp
    from app.lessons import bp as lessons_bp
    from app.institutions import bp as institutions_bp
    from app.admin import bp as admin_bp
    from app.api import bp as api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(lessons_bp, url_prefix="/lessons")
    app.register_blueprint(institutions_bp, url_prefix="/institutions")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api/v1")


def _register_cli(app):
    from app.commands import create_admin_command, reset_progress_command, seed_db_command

    app.cli.add_command(seed_db_command)
    app.cli.add_command(create_admin_command)
    app.cli.add_command(reset_progress_command)


def _register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_error):
        db.session.rollback()  # clear any half-committed transaction before rendering
        return render_template("errors/500.html"), 500


def _register_template_helpers(app):
    from app.utils import render_markdown

    app.jinja_env.filters["render_markdown"] = render_markdown

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.utcnow().year, "app_name": "Tera"}
