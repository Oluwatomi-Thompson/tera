# Architecture

## Application setup

`run.py` exposes the Flask app factory from `app/__init__.py`. `create_app()` loads a config, initializes shared extensions from `app/extensions.py`, registers blueprints and CLI commands, and installs error handlers and template helpers. Models are imported during extension setup so SQLAlchemy/Alembic can discover them.

## Blueprints and URL prefixes

| Blueprint | Prefix | Responsibility |
|---|---|---|
| `main` | `/` | Landing page, about page, signed-in dashboard |
| `auth` | `/auth` | Registration, login, logout, profile |
| `lessons` | `/lessons` | Lesson list/detail, authenticated quizzes, calculator page |
| `institutions` | `/institutions` | Public institution directory and detail pages |
| `admin` | `/admin` | Admin dashboard, lesson publish/reorder/resync, institution management |
| `api` | `/api/v1` | JSON calculator endpoint used by progressive enhancement |

## Typical request flow

A browser request is dispatched to a blueprint route. Routes query or update models through the shared SQLAlchemy `db` extension and render a Jinja template, or return JSON for the calculator endpoint. The app-wide `render_markdown` Jinja filter renders stored lesson Markdown when the lesson page is displayed.

## Content flow

- Lesson source files: `app/content/lessons/*.md` (underscore-prefixed template files are excluded).
- Institution initial seed data: `app/content/institutions.yaml`.
- `flask seed-db` parses and upserts lessons, questions, and choices by lesson slug; institution rows are upserted by name.
- Admin “Resync” calls the lesson sync function. Lesson Markdown remains authoritative for lesson text and quiz questions; the admin UI handles publication/reordering and institution CRUD.
- Tests are grouped by blueprint under `tests/`, with shared fixtures in `tests/conftest.py`.

There is a content-sync note at `docs/architecture/content-sync-flow.md`; the architecture directory does not currently contain a rendered ERD. For the actual fields and relationships, consult `app/models/` and `03-database-schema.md`.

## Change guidance

When changing routes, check the matching blueprint templates and tests. When changing lesson content structure, keep `app/commands.py`'s parser and `app/content/lessons/_TEMPLATE.md` in sync. Keep admin-only routes behind both login and admin authorization.
