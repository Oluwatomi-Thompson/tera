# Tech Stack

Versions are not pinned in `requirements.txt`; do not assume exact versions from these notes. Check the dependency files and the environment before debugging version-specific behavior.

- **Backend:** Python, Flask application factory (`app.create_app`).
- **Database / ORM:** Flask-SQLAlchemy. Development defaults to SQLite; `DATABASE_URL` can select another database. `ProdConfig` expects a configured database URL and supports PostgreSQL URL normalization.
- **Migrations:** Flask-Migrate / Alembic; migration scripts are in `migrations/`.
- **Authentication:** Flask-Login; password hashing uses Werkzeug. Flask-WTF provides forms and CSRF support for form workflows.
- **Views:** Jinja templates and server-rendered HTML.
- **CSS:** Tailwind CSS 3, with input at `app/static/css/input.css`; `npm run build-css` builds the output and `npm run watch-css` watches during development.
- **Browser behavior:** Small vanilla JavaScript files, including calculator enhancement and quiz behavior; core calculator page also has a server-rendered form path.
- **Content:** Markdown lesson files with YAML frontmatter; YAML for initial institution seed data.
- **Tests:** pytest and pytest-flask. `TestConfig` uses in-memory SQLite and disables CSRF for test clients.
- **Deployment-related dependency:** Gunicorn is listed in `requirements.txt`; deployment configuration is not documented here.

Source of truth for dependencies: `requirements.txt`, `package.json`, and `package-lock.json`. There is currently no frontend framework or separate API service; `/api/v1` is a small Flask blueprint.
