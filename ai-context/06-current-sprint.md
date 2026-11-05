# Current Project Status

**Snapshot:** `docs/complete-ai-context` branch, based on the files currently checked in. The repository does not include an SRS under `docs/srs/`, so there is no verified sprint plan to reproduce here. Do not treat this snapshot as a formal project-management status.

## Implemented in the repository

- [x] Flask app factory, configuration, extensions, six registered blueprints, and CLI commands.
- [x] User registration/login/profile and learner/admin roles.
- [x] Lesson listing/detail, quizzes, quiz scoring, and per-learner progress.
- [x] Markdown lesson seeding and initial institution YAML seeding.
- [x] Public institution directory and admin management flows.
- [x] Server-rendered calculator plus JSON endpoint and browser-side enhancement.
- [x] Initial migration and tests organized by app area.
- [x] Five lesson Markdown files are present and marked published in their frontmatter.

## Useful next checks (not a committed sprint plan)

- [ ] Add the approved SRS or requirements document to `docs/srs/` and align the roadmap/status notes with it.
- [ ] Run the test suite and record the result in the PR or project notes; this review did not execute tests.
- [ ] Confirm lesson facts, citations, institution links, and licensing information against current primary sources before presenting the material as current.
- [ ] Check that local setup instructions work from a clean clone and document verified steps in `README.md`.
- [ ] Decide whether to add a rendered ERD to `docs/architecture/`; the schema currently has no diagram checked in.

Update this file when a verified project plan exists. Keep completed work, active work, and proposed follow-ups distinct.
