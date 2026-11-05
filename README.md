# Tera

A localized investment-literacy platform for Rwandan youth. See `docs/srs/`
for the full Proposal & SRS.

## Status
Sprint 0 — scaffolding. See `ai-context/06-current-sprint.md` for live state.

## Setup (TODO — fill in as the real steps stabilize)
1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. `npm install`
4. Copy `.env.example` -> `.env` and fill in values
5. `flask db upgrade`
6. `npm run watch-css` (separate terminal)
7. `flask run`

## Docs
- `docs/srs/` — Proposal & SRS
- `docs/architecture/` — architecture + ERD diagrams
- `docs/research/` — sourced facts, institution notes
- `docs/figma/` — design tokens, prototype screenshots
- `ai-context/` — read this first if you're an AI assistant picking up this project
