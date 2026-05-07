# Change Report — v2 Production Template Split

Date: 2026-05-06

## Summary

This package revision separates the newsletter system into an authoring template and a production template, updates the creation instructions to use them appropriately, and incorporates the size-reduction and cross-client rendering lessons from recent testing.

## Template changes

### Added

- `templates/authoring_canonical.html`
- `templates/production_canonical.html`

### Retained

- `templates/canonical.html` remains as a compatibility alias for the authoring template.

## Asset changes

Replaced legacy MailerLite-generated asset URLs with short GitHub Pages asset URLs:

- Spade: `/bw/a/S.png`
- Heart: `/bw/a/H.png`
- Diamond: `/bw/a/D.png`
- Club: `/bw/a/C.png`
- Header wordmark/logo: `/bw/a/logo.png`
- Bridge World emblem: `/bw/a/BW.png`

## Production pipeline changes

Added an explicit two-phase workflow:

1. Render and validate using the authoring template.
2. Export to production using stripping, minification, short URLs, safe literal shortening, validated class compression, and Outlook restoration.

## Rationalization results

The instructions now distinguish:

- authoring source vs production output
- safe vs risky size reductions
- Outlook-critical inline/conditional styling vs class-compressed styling
- outer gutter background vs inner shell background vs heading background
- MSO auction blocks as required Outlook stabilizers

## Lessons incorporated

- Strip generation comments before MailerLite upload.
- Preserve MSO conditional blocks, especially auction tables.
- Use short asset URLs from the start.
- Use class compression only for validated repeated typography/alignment.
- Restore inline/conditional Times New Roman for Outlook-sensitive regions.
- Avoid broad background stripping.
- Target 75–85 KB production source when MailerLite tracking injection is expected.

## Size observations

- Authoring template size: 118.9 KB
- Production template/reference size: 83.8 KB

The authoring template is intentionally more readable and instructional. The production template/reference is the size-optimized shape for MailerLite output.


## v3 layered instruction architecture

Rearchitected the active instruction files into seven rule layers:

1. Extraction rules
2. Semantic schema definitions
3. Semantic bridge rules
4. Layout intent rules
5. Rendering rules
6. Production export rules
7. Validation rules

Key changes:
- Separated PDF/source extraction from bridge normalization and rendering.
- Defined semantic JSON as the contract between layers.
- Moved hand/auction/fidelity semantics out of rendering and into semantic bridge rules.
- Moved hand layout choices into content-agnostic layout intent rules.
- Restricted rendering rules to JSON -> authoring HTML.
- Restricted production export to authoring HTML -> MailerLite-ready HTML optimization.
- Added validation categories for each layer.
- Archived previous overlapping instruction files under `archive_instructions_layered_refactor/`.


## Layered architecture completion pass

Completed items 1-7 requested after the layered refactor:

1. Added complete semantic JSON examples for defense, play, bidding MSC, and historical deal articles.
2. Clarified validator categories and mapped each validator to its authoritative instruction layer.
3. Checked templates against the new architecture and removed extraction/bridge-semantic heuristic comments from authoring/canonical templates.
4. Added layout-intent regression examples for vertical N/S, three-position defense, cross-deal, and bidding MSC single-South layouts.
5. Added approved production compression classes for hands, suits, auction text, and body text.
6. Added hard-fail, warning, and informational validation gates.
7. Marked archive directories/files as non-loading historical notes and added manifest archive policy.

No ZIP was generated in this pass.

## 2026-05-06 Failure-mode hardening pass

Added rules and validators for:

- PDF rasterization before diagram extraction
- source inventory for multi-file bundles
- cross-file problem/solution pairing
- MSC prompt-vs-solution source selection
- semantic auction storage and W-N-E-S derivation
- auction round-trip validation
- protected rendering regions
- section assembly order invariant
- platform hard gates for Outlook desktop and Gmail/Pixel
- production size gates and concision reporting

## Additional architecture hardening - source consistency and layer purity

Updated on 2026-05-06.

Added rules for:
- JSON canonicality and renderer purity
- formal layout intent ownership
- deterministic/idempotent production export
- protected output regions and Outlook-critical inline properties
- mobile constraints and platform gates
- template edit-region ownership
- source bridge inconsistency detection
- impossible deal/auction/play hard-fail validation
- do-not-infer source facts
- auction edge-case schema examples

## Codex-readiness additions

Updated on 2026-05-06.

Added:
- machine-readable JSON schema
- validator implementation roadmap
- validation gate definitions
- golden fixture directory and initial fixtures
- production export diff-report requirements
- source inconsistency correction workflow
- problem/solution pairing confidence rubric
- template/export versioning guidance
- protected authoring sentinels
- accessibility policy
- Codex handoff guide

## Final knowledge polish before Codex handoff

Updated on 2026-05-07.

Added:
- single-article issue policy
- immutable rendering identity invariants
- renderer component ownership
- semantic/render/export version metadata
- OCR confidence handling
- image preprocessing guidance
- impossible-to-infer examples
- canonical card-rank formatting
- human-review-required validation state
- package-level test orchestration
- implementation constraints for deterministic validators/export
- accessibility-preserving minimization guidance
- protected-region fingerprint specification
