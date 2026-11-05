# Backlog

This is a set of **suggested follow-ups inferred from the current repository**, not an approved roadmap. Prioritize against the school-project requirements once the SRS or equivalent is checked in.

## Documentation and verification

- [ ] Add the approved proposal/SRS and link requirements to the implementation and test plan.
- [ ] Verify the README setup steps from a clean environment and document known prerequisites.
- [ ] Run the full pytest suite, fix failures, and record what was tested.
- [ ] Add an ER diagram under `docs/architecture/` if it is useful for the project review.

## Content quality and safety

- [ ] Fact-check every published lesson claim and citation against current authoritative sources.
- [ ] Review institution names, URLs, licensing status, product thresholds, and investment-risk caveats before release.
- [ ] Add a repeatable content review checklist; confirm quiz questions have exactly one correct answer before seeding.

## Product and engineering follow-ups

- [ ] Review calculator wording and presentation so illustrative assumptions cannot be mistaken for guaranteed returns.
- [ ] Review error handling, accessibility, mobile layouts, and form/authorization flows as part of a manual QA pass.
- [ ] Add automated tests for any identified gaps before expanding features.

## Explicit scope boundary

Tera's current educational role does not include executing trades, holding customer funds, or giving personalized investment advice. Do not add these capabilities by implication; they would require a separately approved product, legal, security, and compliance scope.
