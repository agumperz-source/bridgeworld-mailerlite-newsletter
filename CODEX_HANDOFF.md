# Codex Handoff

This package is ready for Codex implementation work.

## Recommended Codex tasks

1. Implement JSON schema validation using `schema/newsletter.schema.json`.
2. Implement validators described in `validators/README.md`.
3. Add tests based on `fixtures/`.
4. Implement deterministic production export.
5. Add production export diff report.
6. Add protected-region checks for Outlook/MSO structures.
7. Add auction legality and W-N-E-S round-trip tests.
8. Add source bridge inconsistency detection tests.
9. Ensure production export is idempotent.
10. Package CI or a local test command that runs all validators.

## Do not ask Codex to redesign rendering first

The current rendering rules are the result of Outlook/Gmail regression testing. Codex should first implement validation and export determinism before attempting further HTML-size reductions.

## High-risk areas

- Outlook/MSO auction tables
- Outlook spacers
- newsletter identity font
- Stay Connected font
- gray gutters and white shell
- Problem/Solution heading bands
- mobile hand/auction wrapping

## Final polish requirements

Before implementing new rendering features, Codex should add:
- package-level test command
- schema validation
- protected-region fingerprints
- fixture validation
- deterministic production export
- export diff report
- source inconsistency correction workflow support
