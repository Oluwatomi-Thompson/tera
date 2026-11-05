# Content Strategy

TODO:
- Full lesson list in order, each with a one-line learning objective
- Rwanda-specific facts bank (source each one — see docs/research/)
- Tone/voice notes (simple, jargon-light, RWF-denominated, cite every figure)

## Authoring workflow (finalized — see ai-context/08-decisions.md, ADR-004)
1. Copy `app/content/lessons/_TEMPLATE.md` to `<slug>.md`.
2. Fill in frontmatter: `slug`, `order`, `title`, `is_published` (leave
   `false` until fact-checked), `objective`, `sources` (every factual claim
   in the lesson needs at least one entry here).
3. Write the lesson under `## Content` in plain markdown.
4. Write quiz questions under `## Quiz`:
   - Numbered list = questions, in order.
   - Sub-bullets `- [ ]` / `- [x]` = choices; exactly one `[x]` per question
     (not enforced by the parser — check it yourself).
5. Run `flask seed-db`. Re-run any time you edit the file — it upserts by
   `slug`, so it's safe to run repeatedly.
6. Flip `is_published: true` once the content is fact-checked and re-seed,
   or toggle it from the admin panel (same effect, no re-seed needed for
   just a publish-state change).

## Lesson list
TODO — draft the actual sequence, something like:
1. What is investing, in RWF terms
2. Mobile money vs. bank vs. broker
3. Risk and return basics
4. Where Rwandans can actually invest (RSE, RNIT, etc.)
5. How much do you actually need to start
