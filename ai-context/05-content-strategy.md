# Content Strategy

## Audience and editorial principles

The lessons are aimed at people learning the basics of investing in Rwanda. Use plain language, define financial terms, prefer realistic RWF examples, and distinguish saving from investing. Explain risks as well as potential returns. Do not frame Tera as a broker, imply a return is guaranteed, or recommend a particular investment product.

Financial figures, product terms, institution names, and licensing claims can change. Cite claims in each lesson's `sources` frontmatter, use authoritative and current sources where possible, and verify those sources before publication. This document summarizes the repository's stated approach; it is not an independent fact-check of lesson claims.

## Current lesson sequence

The checked-in content currently contains five lessons, ordered by frontmatter:

1. `what-is-investing` — Explain investing versus saving using RWF examples.
2. `mobile-money-bank-broker` — Distinguish payment methods from regulated investment providers.
3. `risk-and-return-basics` — Explain risk, return, diversification, and time horizon without recommending a product.
4. `where-rwandans-can-invest` — Introduce relevant Rwandan market institutions and the resource directory.
5. `how-much-to-start` — Discuss entry amounts and use the calculator as an illustrative next step.

The content lives in `app/content/lessons/`; each lesson's frontmatter controls slug, order, title, publication state, objective, and sources. The database is a synchronized runtime copy, not the place to author lesson text.

## Authoring and synchronization

1. Copy `app/content/lessons/_TEMPLATE.md` to a new `.md` file whose name is not underscore-prefixed.
2. Fill in the required frontmatter (`slug`, `order`, `title`); include `is_published`, a learning objective, and sources. Keep new lessons unpublished until review is complete.
3. Put the lesson body beneath `## Content` and quiz questions beneath `## Quiz`.
4. Follow the parser format: numbered questions and choice lines using `- [ ]` or `- [x]`. Ensure exactly one correct choice per question manually; the parser does not enforce that rule.
5. Run `flask seed-db` to synchronize. It upserts by slug and replaces that lesson's questions/choices from Markdown.
6. Review the rendered content, citations, and quiz before publishing. The admin panel can publish/unpublish and reorder, but Markdown remains authoritative on the next seed/resync.

See `app/commands.py`, the lesson template, and ADR-004 in `08-decisions.md` for implementation details.
