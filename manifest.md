# Manifest

Package version: v3-layered-instruction-architecture
Updated: 2026-05-06

## Required files

- `bootstrap.md`
- `manifest.md`
- `templates/authoring_canonical.html`
- `templates/production_canonical.html`
- `templates/canonical.html`
- `instructions/extraction_rules.md`
- `instructions/semantic_schema.md`
- `instructions/semantic_bridge_rules.md`
- `instructions/layout_intent_rules.md`
- `instructions/rendering_rules.md`
- `instructions/production_export.md`
- `instructions/validation.md`
- `validators/README.md`
- `schema/newsletter.schema.json`
- `fixtures/README.md`
- `fixtures/rendering_fingerprints.spec.json`
- `validators/validation_gates.md`
- `CODEX_HANDOFF.md`
- `reports/change_report.md`

## Loading order

1. `bootstrap.md`
2. `manifest.md`
3. `instructions/extraction_rules.md`
4. `instructions/semantic_schema.md`
5. `instructions/semantic_bridge_rules.md`
6. `instructions/layout_intent_rules.md`
7. `instructions/rendering_rules.md`
8. `instructions/production_export.md`
9. `instructions/validation.md`
10. `templates/authoring_canonical.html`

## Rule-layer authority

Each rule belongs to exactly one primary layer:

- Extraction rules govern how source PDFs/images are processed and what content is selected.
- Semantic schema defines the JSON contract.
- Semantic bridge rules govern bridge meaning, hand structure, auction structure, and normalization inside JSON.
- Layout intent rules govern content-agnostic layout decisions represented inside JSON.
- Rendering rules govern how JSON becomes authoring HTML.
- Production export rules govern optimization of authoring HTML into MailerLite-ready production HTML.
- Validation rules enforce the above without redefining them.

When a rule appears to belong to multiple layers, define it in the lowest semantic layer that owns the decision and reference it elsewhere.

## Template roles

### Authoring template

Use `templates/authoring_canonical.html` for:
- GENERATE mode
- REVISE_HTML mode object reconstruction
- human-readable maintenance
- editable regions and comments
- authoring-time shell truth

### Production template

Use `templates/production_canonical.html` as:
- optimized production shape/reference
- target style for export
- regression comparison for size-safe markup

Do not author new issues directly in the production template unless explicitly requested.

### Compatibility alias

`templates/canonical.html` is retained for older tooling. It is an authoring alias and should mirror `templates/authoring_canonical.html`. Do not edit it independently.

## Asset map

All future generated and production HTML must use these short asset URLs:

- Spade: `https://agumperz-source.github.io/bw/a/S.png`
- Heart: `https://agumperz-source.github.io/bw/a/H.png`
- Diamond: `https://agumperz-source.github.io/bw/a/D.png`
- Club: `https://agumperz-source.github.io/bw/a/C.png`
- Header wordmark/logo: `https://agumperz-source.github.io/bw/a/logo.png`
- Bridge World emblem: `https://agumperz-source.github.io/bw/a/BW.png`

Legacy MailerLite `storage.mlcdn.com/account_image` suit/logo URLs are prohibited in production output unless the user explicitly requests them.


## Archive policy

Directories beginning with `archive_` are non-loading historical notes. They must not be used as active instructions and cannot override the loading order above.

## Compatibility alias policy

`templates/canonical.html` is a compatibility alias generated from `templates/authoring_canonical.html`. Edit `templates/authoring_canonical.html` first, then regenerate/synchronize `templates/canonical.html`. Do not edit the alias directly.

## Asset URL policy

All generated newsletters must use the short GitHub Pages asset URLs listed in the asset map.

Legacy MailerLite-generated `storage.mlcdn.com/account_image/...` suit/logo URLs are forbidden in canonical templates and production exports.

## Production size policy

Production output target is `<= 85 KB`.

Production output above `95 KB` requires explicit user approval before export.


## Canonical JSON contract

Canonical JSON is the semantic contract between extraction, bridge logic, layout intent, rendering, export, and validation.

HTML is never semantic source truth except when uploaded HTML is parsed back into JSON during REVISE_HTML mode.
