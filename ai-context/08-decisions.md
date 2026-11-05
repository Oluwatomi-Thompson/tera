# Architecture Decision Records (ADRs)

## ADR-001: SQLite for dev/test, PostgreSQL for prod
- Context: TODO
- Decision: TODO
- Consequences: TODO

## ADR-002: Vanilla JS over a frontend framework
- Context: TODO
- Decision: TODO
- Consequences: TODO

## ADR-003: Collapse the `quizzes` table into `questions`
- Context: The original ERD had `quizzes {id, lesson_id}` purely as a join
  table with no attributes of its own — every query about a lesson's quiz
  had to join through it for nothing.
- Decision: Removed `quizzes`. `questions.lesson_id` now points directly at
  `lessons.id`. A lesson's questions are implicitly "its quiz."
- Consequences: One fewer table, model, and migration to maintain. If a
  future requirement needs multiple quizzes per lesson or per-quiz settings
  (time limits, retakes), reintroduce `quizzes` then — it's a cheap
  Alembic migration, not worth paying for now.

## ADR-004: Markdown files are the single source of truth for lesson content
- Context: Content accuracy (RWF figures, institution names, thresholds) is
  the core risk for this product. Editing `lessons.content_body` directly
  through an admin panel would create two writable copies of the same
  content (the `.md` file and the DB row) that can silently drift —
  especially risky here because every factual claim needs to stay traceable
  to a citation.
- Decision: `app/content/lessons/*.md` is authoritative. `flask seed-db`
  (see app/commands.py) parses each file's YAML frontmatter + body and
  upserts the matching `Lesson`/`Question`/`Choice` rows by `slug`. The
  admin panel (FR10) does NOT provide a content_body edit form; it only
  manages what has no natural home in a `.md` file: publish/unpublish
  (`is_published`), reordering, and triggering a resync. Content authoring
  happens in a text editor, with real git history and diffs for every
  factual change.
- Consequences: FR10 in the SRS reads as "admin content management," which
  now means something narrower than full CRUD — worth a one-line note if a
  facilitator asks why there's no lesson-edit form in the admin UI. Tradeoff
  accepted deliberately: one source of truth was a stated priority over
  admin-panel completeness.
