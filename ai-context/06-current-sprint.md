# Current Sprint

**Sprint:** 0 — Planning & Setup
**Goal:** finalize requirements, ERD, architecture, scaffold the repo

## Todo
- [ ] Draw the actual ERD diagram from ai-context/03-database-schema.md (dbdiagram.io or similar) -> docs/architecture/
- [ ] Write content strategy: full lesson list + objectives (ai-context/05)
- [ ] Write 2-3 real lesson .md files from _TEMPLATE.md, fact-checked and cited
- [ ] `flask db init` + first migration once models are reviewed
- [ ] Try `flask seed-db` against the real lesson files, confirm upsert-by-slug works
- [ ] Figma wireframes for key screens

## In Progress
- [ ]

## Done
- [x] Repo scaffolded
- [x] ERD finalized (dropped standalone `quizzes` table — see ADR-003)
- [x] Decision made: markdown files are source of truth for lesson content — see ADR-004
- [x] app/models/* written to match finalized ERD
- [x] app/extensions.py + app/__init__.py wired up (db, migrate, login_manager, blueprints)
- [x] `flask seed-db` command written (app/commands.py) — parses frontmatter + quiz markdown, upserts by slug
