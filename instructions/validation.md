# Validation Rules

Validation enforces the layered architecture. It should not redefine extraction, bridge, rendering, or production rules.

## Validation types

### Extraction validation

Checks source -> raw semantic content:
- article boundaries identified
- article type identified
- visible source wording captured
- hands captured as source-visible
- auctions captured as source-visible
- dealer/vulnerability/facts captured or marked unknown

### Semantic bridge validation

Checks semantic content:
- hands use valid seat/suit/rank schema
- auctions are seat-owned and normalized
- W-N-E-S rendering order is derived correctly
- no invented cards or calls
- incomplete auctions are represented explicitly
- dealer/vulnerability consistency is preserved

### Layout intent validation

Checks renderer-facing layout intent:
- article type has an appropriate layout intent
- visible seats match visible hands
- reader seat is represented when known
- full-deal layouts only used when all four hands are known
- auction layout intent exists when auction exists

### Rendering validation

Checks JSON -> authoring HTML:
- canonical shell preserved
- only intended editable/content regions changed
- Stay Connected and footer remain present
- hand labels uppercase only in hand diagrams
- suit images used instead of raw suit glyphs in bridge content
- MSO conditional structures preserved

### Production validation

Checks authoring HTML -> production HTML:
- no generation-only comments
- no editable-region markers
- no legacy MailerLite suit/logo URLs
- production asset URLs match `manifest.md`
- no empty style/class attributes
- MSO conditional comments preserved
- production size reported

### Render regression validation

Checks visual output:
- Outlook desktop
- Gmail mobile/Pixel
- Gmail web
- Apple Mail/iPhone when available

## Required visual checks

### Outlook desktop

- newsletter identity is Times New Roman and bold
- hand compass labels are Times New Roman and bold
- auction headers are Times New Roman and bold
- auction row spacing is compact and stable
- Stay Connected text is Times New Roman
- no extra vertical gap appears above hand diagrams
- gray gutters and white inner shell are correct
- Problem/Solution heading gray band and left accent render correctly
- no unintended gray/white seam below headings

### Gmail mobile / Pixel

- newsletter identity fits on one line where intended
- hand diagrams do not wrap unexpectedly
- auction headers do not wrap
- suit image size/alignment remains stable
- Stay Connected/footer width aligns with article column

## Size reporting

Always report:
- authoring HTML size when available
- production HTML size
- estimated MailerLite injection size, currently 25 KB
- estimated delivered HTML size
- whether MailerLite injection may create Gmail clipping risk

If production HTML exceeds 75 KB, identify:
- remaining Tier 1 options
- possible Tier 2 options
- Tier 3 options only as explicit risky test builds

## Asset validation

Production HTML must not contain legacy MailerLite suit/logo asset URLs unless explicitly requested.

Required short assets:
- `https://agumperz-source.github.io/bw/a/S.png`
- `https://agumperz-source.github.io/bw/a/H.png`
- `https://agumperz-source.github.io/bw/a/D.png`
- `https://agumperz-source.github.io/bw/a/C.png`
- `https://agumperz-source.github.io/bw/a/logo.png`
- `https://agumperz-source.github.io/bw/a/BW.png`

## Conflict validation

If two active instruction files appear to give different rules, use this authority order:

1. Semantic schema for JSON contract.
2. Semantic bridge rules for bridge meaning.
3. Layout intent rules for renderer-facing layout intent.
4. Rendering rules for authoring HTML.
5. Production export rules for MailerLite output.
6. Validation rules only enforce; they do not override upstream rule definitions.


## Validation gates

Validation results must be classified as `hard_fail`, `warning`, or `pass`.

### Hard failures

A build must not be exported when any of these occur:

- Semantic bridge mismatch: card holding, auction call, dealer, vulnerability, contract, or opening lead differs from source truth.
- Invalid hand schema, invalid suit key, invalid rank token, or impossible seat key.
- Auction cannot be mapped to seat-owned calls.
- Required article shell sections are missing: header, article mount, Stay Connected, footer.
- Article content appears after Stay Connected or footer.
- Raw Unicode suit glyphs appear in visible bridge content where suit images are required.
- Whole MSO auction tables are removed, merged, or unwrapped unless the user explicitly requested a Tier 3 test build.
- Production HTML contains legacy MailerLite suit/logo URLs.
- Production HTML contains generation-only comments or editable-region markers.
- `canonical.html` differs from `authoring_canonical.html` when maintained as compatibility alias.

### Warnings

A build may be exported only after reporting the risk when any of these occur:

- Production HTML is greater than 85 KB.
- Production HTML is greater than 95 KB and the user has not set a hard maximum.
- Render regression screenshots are unavailable.
- Tier 2 optimizations were applied but Outlook/Gmail regression testing has not been confirmed.
- CSS selector duplication remains outside platform-scoped blocks.
- The production exporter had to restore Outlook-critical inline styles after class compression.
- Asset URLs are short but not from the manifest-declared asset map.

### Informational checks

Report but do not block:

- Authoring HTML size.
- Production HTML size.
- Estimated MailerLite/Gmail clipping risk.
- Number of comments removed.
- Number of legacy URLs replaced.
- Number of production compression classes used.

## Validation-to-layer mapping

- Extraction validation enforces `extraction_rules.md`.
- Schema validation enforces `semantic_schema.md`.
- Semantic bridge validation enforces `semantic_bridge_rules.md`.
- Layout intent validation enforces `layout_intent_rules.md`.
- Rendering validation enforces `rendering_rules.md`.
- Production validation enforces `production_export.md`.

Validators must reference authoritative rules rather than restating them in implementation comments.

## Template architecture checks

- `templates/authoring_canonical.html` may contain maintainability comments but must not contain extraction heuristics, article-type detection logic, bridge normalization logic, or production-minification logic.
- `templates/production_canonical.html` must contain no generation-only comments and no editable markers.
- `templates/canonical.html` is a compatibility alias generated from `templates/authoring_canonical.html`; do not edit it directly.
- Both templates must use manifest-declared short asset URLs and no legacy MailerLite suit/logo URLs.

## Hard gates for known failure modes

### Extraction hard gates

Fail validation when:

- a paginated PDF was read without first generating page images
- the source inventory was not built for a multi-file source set
- a solution file cannot be confidently paired with its problem file
- an MSC solution article is available but commentary/action scores were extracted from the prompt-only problem article
- article type is uncertain
- hand, auction, dealer, vulnerability, contract, or opening lead data is ambiguous

### Auction hard gates

Fail validation when:

- auction calls are not stored semantically by seat
- W-N-E-S display is not derived from the semantic auction
- dealer offset does not match the first rendered call
- incomplete auction blanks are rendered as dashes
- a rendered auction cannot round-trip back to the semantic auction object
- any call, seat, order, pass, double, redouble, suit, notrump, question mark, or blank differs from source truth

### Rendering assembly hard gates

Fail validation when final HTML order is not:

`preheader -> shell/header -> newsletter identity -> editor note -> share/signup -> article heading -> article body -> Stay Connected -> footer`

Fail validation when:

- Stay Connected or footer appears above the article
- article content appears below Stay Connected or footer
- more than one article block is populated
- an unused article block contains visible content
- invariant Stay Connected or footer is missing

### Platform hard gates

Fail validation when protected regions lose required Outlook/Gmail-safe properties:

- newsletter identity loses Times New Roman in Outlook
- hand labels lose Times New Roman or bold in Outlook
- auction headers lose bold in Outlook
- auction row height/line-height changes in Outlook
- heading bands lose gray fill or left rule
- Stay Connected loses Times New Roman in Outlook
- outer gray gutters or inner white shell are lost
- suit icons are replaced by raw suit glyphs in visible bridge content

### Production hard gates

Fail validation when:

- production HTML exceeds 95 KB without explicit user approval
- production HTML contains legacy MailerLite-generated suit/logo URLs
- production HTML contains authoring/generation comments
- production HTML contains empty style/class attributes
- production HTML contains malformed conditional comments

## Source bridge inconsistency gates

Hard-fail before rendering if any source bridge inconsistency is detected, including:
- duplicate card in one deal
- full hand not equal to 13 cards
- full deal not equal to 52 unique cards
- problem hand conflicts with paired solution hand
- dealer/vulnerability conflict across paired files
- impossible auction
- impossible double/redouble
- play sequence using unavailable cards
- play sequence violating known follow-suit constraints
- source facts contradicting contract/opening lead/play description

The validation report must identify the conflicting source facts and where they came from. Do not produce corrected HTML until the inconsistency is resolved or the user explicitly authorizes a correction.

## Template and JSON canonicality gates

Hard-fail if:
- rendering uses HTML as semantic source truth outside REVISE_HTML parse-back mode
- production template contains extraction, OCR, bridge-logic, or article-detection instructions
- authoring template is sent directly as production output
- `canonical.html` diverges from `authoring_canonical.html` except by approved compatibility alias policy
- asset URLs in rendered production HTML do not come from the manifest asset map

## Mobile and platform gates

Required platform checks after Tier 2 or Tier 3 optimization:
- Outlook desktop
- Gmail Android/Pixel
- Gmail web
- Apple Mail/iPhone when available

Required visual checks:
- gray desktop gutters
- white central shell
- visible gray Problem/Solution headings
- no gray/white Outlook spacer seams
- newsletter identity Times New Roman in Outlook
- hand compass labels Times New Roman and bold in Outlook
- Stay Connected Times New Roman in Outlook
- auction headers bold in Outlook
- auction rows maintain compact spacing
- mobile has no horizontal scroll
- mobile auction headers do not wrap
- suit icons align in hand diagrams and auctions

## Deterministic export gate

Production export must be idempotent.

Validator should run export twice and compare output. Any byte difference is a warning at minimum and a hard fail for production automation.

## Production export diff report

Every production export should produce a concise diff report containing:
- authoring HTML size
- production HTML size
- bytes saved by comment stripping
- bytes saved by URL replacement
- bytes saved by class compression
- bytes saved by minification
- whether protected regions were touched
- whether MSO blocks were touched
- final size risk estimate after MailerLite injection

## Source inconsistency correction workflow

When source bridge inconsistency validation fails, the system must stop before rendering and present a structured report.

The user may choose one of:
- stop and correct the source
- use the problem version of the conflicting fact
- use the solution version of the conflicting fact
- apply a user-provided correction
- mark the item as a source erratum and proceed with explicit annotation if appropriate

No correction is allowed without explicit user authorization.

## Rendering fingerprint snapshots

Golden fixtures should include normalized fingerprints for protected rendered regions.

Recommended fingerprints:
- newsletter identity block
- Problem/Solution heading block
- hand geometry block
- Outlook/MSO auction block
- Stay Connected block
- footer block

A fingerprint may be a normalized HTML hash or structural assertion list. Fingerprints are not a replacement for visual testing, but they catch accidental structural drift.

## Human-review-required state

Validation may return `human_review_required` for cases that are not safe to auto-resolve but may not be definite source errors.

Examples:
- OCR ambiguity in card/auction region
- weak or moderate-only problem/solution pairing evidence
- conflicting non-bridge metadata
- production HTML over target size but under hard fail
- Tier 2 optimization without fresh Outlook/Gmail screenshots
- unexpected protected-region fingerprint change

`human_review_required` blocks automated production export unless the user explicitly approves proceeding.

## Package test orchestration

Codex should implement a single package test command equivalent to:

```text
validate_package():
    validate_manifest()
    validate_templates()
    validate_schema()
    validate_fixtures()
    validate_extraction_contract()
    validate_bridge_consistency()
    validate_auction_roundtrip()
    validate_layout_intents()
    validate_rendering_invariants()
    validate_production_export()
    validate_export_idempotence()
    produce_validation_report()
```

The command should return a nonzero failure status on any hard fail.
