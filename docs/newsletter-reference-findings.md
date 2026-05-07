# Newsletter Reference Findings

This file records tested newsletter examples and how they should influence future template work. These examples are references, not shell authority.

## 2026-05-06

Status: known good on all tested platforms; fresh MailerLite copy reported 114 KB.

Use as the baseline for:

- Outlook desktop and Gmail/Pixel conditional safety.
- Compact production shell with short GitHub Pages suit and logo asset URLs.
- Full-width Stay Connected/footer inside the current content column.

Do not infer:

- That 85 KB source HTML is a safe long-term target. MailerLite added roughly 25-30 KB.
- That every current style layer is intentionally minimal. Some CSS exists because it fixed platform defects late in testing.

## 2026-04-28

Status: acceptable, but not visually preferred.

Use as a warning for:

- Auction tables that are too spacious.
- Stay Connected/footer that does not span the content column.

## 2026-04-21

Status: visually preferred MSC reference.

Use as a model for:

- Compact auction tables.
- Action-score tables.
- MSC article structure: facts, South hand, auction, prompt, score table, commentary.

## 2026-04-14

Status: passed testing, but has known presentation issues.

Use as a warning for:

- Nested bottom shells and `548px` footer wrappers that double-inset Stay Connected.
- Percentage-spacer hand layouts that can look slightly off.
- Airy auction rows using large padding.

## 2026-04-07

Status: passed testing, but diagnostic rather than a design model.

Use as a warning for:

- Airy `416px` auctions with `10px 12px` padding.
- Percentage spacer hand diagrams.
- Stray table nesting around generated hand/solution regions.

## 2026-03-31

Status: visually good.

Use as a model for:

- Simple shell structure.
- Compact auction density.
- Declarer-play vertical hand layout when only North/South are visible.

Modernize before reuse:

- Replace raw suit glyphs in utility areas with suit images.
- Add current mobile/Outlook safety where needed.

## 2026-03-24

Status: visually preferred MSC reference.

Use as a model for:

- Compact `320px` auction tables.
- Compact action-score tables with right-aligned numeric columns.
- Footer/Stay Connected placed directly within the main content column.

Modernize before reuse:

- Normalize suit-image spacing.
- Prefer short asset URLs when tested.

## 2026-03-17

Status: useful footnote reference.

Use as a model for:

- Footnote placement immediately below the auction table.

Do not copy:

- Full-width airy auction tables.

## 2026-03-10

Status: first newsletter; useful special-case reference.

Use as a model for:

- Optional bidder-name row below `WEST / NORTH / EAST / SOUTH`.

Do not copy:

- Auction footnotes placed as a spanning row inside the auction table.
- CSS-heavy browser-like layout as a production email shell.

## Design Direction

The current production template is Template Family 1: Classic Editorial. It should remain stable while the new visual assets are pending.

Future visual redesigns should be implemented as additional template families that reuse the same validated bridge components:

- hand diagrams
- auction tables
- auction footnotes
- bidder-name rows
- action-score tables
- MailerLite token handling
- Outlook/Gmail compatibility rules

