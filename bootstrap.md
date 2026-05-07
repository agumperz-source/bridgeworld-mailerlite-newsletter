# Bootstrap

This package governs The Bridge World MailerLite newsletter system.

## First action

1. Read `manifest.md`.
2. Load the active instruction files in manifest order.
3. Treat the semantic JSON model as the contract between extraction, bridge normalization, rendering, and production export.
4. Use `templates/authoring_canonical.html` for authoring/rendering.
5. Use `templates/production_canonical.html` only as the optimized production shape/reference.
6. Never upload authoring HTML directly to MailerLite; always run production export.

## Layered architecture

The package is organized by rule type:

1. Extraction rules: source PDFs/images -> raw semantic content.
2. Semantic schema definitions: JSON contract.
3. Semantic bridge rules: bridge correctness and normalization inside JSON.
4. Layout intent rules: content-agnostic rendering intents stored in JSON.
5. Rendering rules: canonical JSON -> authoring HTML.
6. Production export rules: authoring HTML -> MailerLite-ready HTML.
7. Validation rules: checks at every layer.

Rules must remain in their proper layer. Do not put rendering or CSS rules into extraction or bridge rules. Do not put PDF-extraction heuristics into rendering rules.
