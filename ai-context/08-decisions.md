# Architecture Decision Records (ADRs)

These notes capture decisions already reflected in code or existing project notes. Where context is inferred from implementation rather than an approved requirements document, that is stated explicitly.

## ADR-001: SQLite for local development/tests; configurable database for production

- **Context:** Local setup should work without requiring a database server; automated tests need isolated, disposable storage. The production config accepts a `DATABASE_URL`, and PostgreSQL support is present in dependencies and Docker Compose.
- **Decision:** Development defaults to a SQLite file; tests use in-memory SQLite; production configuration requires environment-provided `SECRET_KEY` and `DATABASE_URL`.
- **Consequences:** Local onboarding and tests are lightweight. Production must supply real secrets and a database URL. `docker-compose.yml` provides a PostgreSQL service, but does not by itself configure the Flask app's environment.

## ADR-002: Server-rendered Flask/Jinja with small vanilla JavaScript enhancements

- **Context:** The current app is a Flask/Jinja application with a small amount of interactive behavior; there is no separate frontend application or framework in the package manifests.
- **Decision:** Render pages on the server and use focused vanilla JavaScript where useful. The calculator can still submit/render through the regular page route if JavaScript/API enhancement is unavailable.
- **Consequences:** Fewer frontend build/runtime components and a simpler app structure. Keep JavaScript progressive and preserve server-side validation and behavior for important flows.

## ADR-003: Collapse the `quizzes` table into `questions`

- **Context:** The original ERD had a `quizzes` table containing only an ID and lesson ID. Every question about a lesson's quiz needed an otherwise unnecessary join.
- **Decision:** Removed `quizzes`; `questions.lesson_id` points directly to `lessons.id`. A lesson's questions are its quiz.
- **Consequences:** One fewer table/model/migration. Reintroduce a quiz entity if a future requirement needs multiple quizzes per lesson or quiz-level settings such as time limits or retakes.

## ADR-004: Markdown files are the source of truth for lesson content

- **Context:** Lesson text and quiz content need reviewable history and citations. Keeping separate editable copies in Markdown and database content risks them diverging.
- **Decision:** Author lesson content in `app/content/lessons/*.md`. `flask seed-db` and the admin resync upsert lesson data by slug and replace the associated question/choice rows. The admin area manages publication, ordering, and resync rather than editing lesson body text.
- **Consequences:** Git diffs provide a review trail for content changes. Seeding overwrites the matching lesson's database content and quiz from its Markdown file; edit the source file, then reseed. Institution rows have a separate initial YAML seed and admin CRUD workflow.
