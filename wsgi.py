"""Production entry point: gunicorn wsgi:app (run.py is dev-only)."""
from app import create_app
from app.config import ProdConfig

app = create_app(ProdConfig) # type: ignore
