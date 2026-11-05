# Project Overview

**Tera** is a localized investment-literacy web application for young people in Rwanda. Its goal is to explain basic investing concepts with Rwanda-specific institutions, examples denominated in Rwandan francs (RWF), and an approachable path from learning to finding regulated providers.

The repository currently implements a Flask web app with public lessons and an institution directory, learner accounts and quiz progress, an illustrative compound-growth calculator, and an admin area. Lesson content is authored in Markdown under `app/content/lessons/` and synchronized into the database. See `02-architecture.md` for the code map and `05-content-strategy.md` for the current lesson sequence.

Tera is an educational resource, **not** a broker, investment product, transaction service, or source of personalized financial advice. It should direct users to verify current information with licensed institutions rather than imply guaranteed returns or recommend a product.

**Project status:** The branch contains a substantial MVP implementation and tests. The SRS directory currently has no requirements document, so treat detailed product requirements and roadmap as unconfirmed until that source is added. This status is based on the checked-in code, not a claim that the app has been deployed or independently tested.

## AI assistant guidance

- Read this folder before making changes; treat implementation as the source of truth when it disagrees with these notes.
- Keep Rwanda-specific financial claims sourced and confirm that figures and institution licensing details are current before publishing.
- Preserve the distinction between educational examples and investment advice. Calculator projections are illustrative, not promises.
- Add or update tests alongside behavior changes, and do not claim tests passed unless they were actually run.
