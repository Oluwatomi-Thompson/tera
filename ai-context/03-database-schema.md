# Database Schema

Status: finalized for MVP (Sprint 0). Source of truth for field names is
app/models/*.py — if this doc and the code ever disagree, the code wins;
update this doc to match.

Draw the actual ER diagram from this (dbdiagram.io or similar) and drop the
export in docs/architecture/.

## users
| field | type | notes |
|---|---|---|
| id | integer, PK | |
| email | varchar | not null, unique |
| password_hash | varchar | not null |
| role | enum('learner','admin') | not null, default 'learner' — SQLAlchemy `Enum`, not a bare string |
| created_at | timestamp | default now() |

## lessons
| field | type | notes |
|---|---|---|
| id | integer, PK | |
| title | varchar | not null |
| slug | varchar | unique, not null — clean URLs, e.g. `/lessons/what-is-investing` |
| order_index | integer | not null, unique — display order |
| content_body | text | raw markdown, seeded from `app/content/lessons/*.md` — do not hand-edit in the DB |
| is_published | boolean | not null, default false — hide drafts while fact-checking |
| source_path | varchar | which `.md` file this row was last seeded from |
| created_at | timestamp | default now() |
| updated_at | timestamp | on update |

## questions
_Collapsed the old standalone `quizzes` table into this — a lesson's questions
ARE its quiz, so `questions.lesson_id` points straight at `lessons.id`. See
ADR in 08-decisions.md. Reintroduce a `quizzes` table only if/when you need
multiple quizzes per lesson or per-quiz settings._

| field | type | notes |
|---|---|---|
| id | integer, PK | |
| lesson_id | integer, FK -> lessons.id | not null, on delete cascade |
| text | text | not null |
| order_index | integer | |

## choices
| field | type | notes |
|---|---|---|
| id | integer, PK | |
| question_id | integer, FK -> questions.id | not null, on delete cascade |
| text | varchar | not null |
| is_correct | boolean | not null, default false — app-level validation: exactly one `true` per question |

## user_progress
_`quiz_score` split into `correct_count` + `total_questions` instead of a
bare percentage, so a score still means something if a lesson's question
count ever changes later._

| field | type | notes |
|---|---|---|
| id | integer, PK | |
| user_id | integer, FK -> users.id | not null, on delete cascade |
| lesson_id | integer, FK -> lessons.id | not null, on delete cascade |
| completed | boolean | not null, default false |
| correct_count | integer | null until the quiz is taken |
| total_questions | integer | null until the quiz is taken |
| completed_at | timestamp | |

Indexes: unique `(user_id, lesson_id)` — one progress record per user per lesson.

## institutions
| field | type | notes |
|---|---|---|
| id | integer, PK | |
| name | varchar | not null |
| description | text | |
| url | varchar | not null |
| category | varchar | e.g. `regulator`, `exchange`, `unit_trust`, `broker` |
| created_at | timestamp | default now() |

## Relationships at a glance
```
users 1--* user_progress *--1 lessons 1--* questions 1--* choices
institutions (standalone — no FK relationships)
```
