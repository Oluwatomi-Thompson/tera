# Content Sync Flow

Textual sketch — turn this into an actual diagram alongside the ERD once
you're in your diagramming tool of choice.

```
app/content/lessons/*.md  (source of truth, git-tracked, cited facts)
        │
        │  flask seed-db   (app/commands.py: seed_db_command)
        │  — parses YAML frontmatter + "## Content" / "## Quiz" sections
        │  — upserts by `slug`
        ▼
   lessons / questions / choices tables  (Postgres/SQLite)
        │
        │  read-only from here on for content_body
        ▼
   Lesson list / detail / quiz routes  (app/lessons/)

Admin panel (app/admin/) only touches:
  - lessons.is_published
  - lessons.order_index
  - triggers a resync (same logic as `flask seed-db`, from the UI)
It never writes lessons.content_body, questions.*, or choices.* directly.
```

## Why this matters for citations
Every RWF figure or institution name in a lesson traces back to a `sources:`
entry in that lesson's `.md` frontmatter. Keeping authoring in files (not a
DB-backed rich text editor) means that trail stays intact in git history —
useful both for your own fact-checking discipline and if a facilitator asks
where a specific number came from.
