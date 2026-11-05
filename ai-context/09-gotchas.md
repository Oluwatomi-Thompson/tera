# Gotchas and Maintenance Notes

- **Markdown parser format is part of the content interface.** Lesson seeding in `app/commands.py` expects YAML frontmatter delimited by `---`, and sections named `## Content` and `## Quiz`. Quiz questions must be numbered (`1. ...`) and choices must use `- [ ]` / `- [x]`; other formats may not parse as intended.
- **The parser does not validate quiz correctness.** It does not enforce four choices or exactly one correct answer. Check each authored quiz before publishing.
- **Resync replaces quiz rows.** For a matching slug, seeding rebuilds questions and choices from Markdown. Do not hand-edit those rows expecting the edits to survive a seed.
- **Publication behavior:** Draft lessons are hidden as 404s from non-admin users, including when a learner guesses the URL. The admin can preview the route.
- **Lesson order is unique.** The admin reorder route and seed routine use temporary negative order values to avoid collisions while swapping/reapplying unique values; do not casually remove that staging behavior.
- **`source_path` belongs to lesson data.** It records the Markdown file used by the seed process; it is not a separate content source.
- **Environment/configuration:** Development has a generated fallback secret, but production must set `SECRET_KEY` and `DATABASE_URL`. Do not commit `.env` or real credentials.
- **Tests use a separate config.** The shared pytest fixture creates/drops an in-memory SQLite schema and disables CSRF in tests. That does not replace checking production configuration or CSRF behavior in a real browser.
- **Financial content is time-sensitive.** Verify figures, product terms, institution links, and licensing details against current authoritative sources before treating them as current.

If a new workaround or confirmed issue is found, record the reproduction or affected file here; avoid listing guesses as known defects.
