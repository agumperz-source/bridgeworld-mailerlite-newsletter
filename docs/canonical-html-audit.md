# Canonical HTML Audit

Date: 2026-05-06

Scope: `templates/production_canonical.html`

## Current Size

- Source size: 85,239 bytes
- Estimated MailerLite injection: 25,000 bytes
- Estimated delivered size: 110,239 bytes
- Policy status: human review required, because source size is above 85 KB

## Byte Buckets

| Bucket | Bytes | Count | Notes |
| --- | ---: | ---: | --- |
| Total | 85,239 | 1 | Current production canonical size |
| Comments | 29,905 | 36 | Mostly Outlook/MSO conditional blocks; not ordinary comments |
| MSO blocks | 29,601 | 20 | High-risk Outlook compatibility markup |
| Style blocks | 11,375 | 19 | Head CSS and MSO-scoped CSS |
| Inline style attributes | 41,315 | 400 | Largest reducible bucket, but many declarations are Outlook-sensitive |
| Class attributes | 6,399 | 324 | Moderate target after class-name safety is proven |
| Table layout attributes | 12,428 | 930 | High-risk for email clients; do not remove generically |
| Image src attributes | 3,064 | 60 | Already shortened with GitHub Pages asset URLs |

## Head Style Layers

The production head contains 19 style blocks. Several are historical override layers, not a clean minimal cascade:

- Multiple MSO blocks redefine `.tbw-section-heading-cell`, `.tbw-auction-head`, `.tbw-auction-cell`, and spacer heights.
- Several mobile blocks are superseded by the final mobile typography block.
- Two section-heading background blocks overlap; the later block adds the left border but does not include the earlier `table` selector.
- The final utility-class blocks (`.hfont`, `.hlabel`, `.hcard`, `.af`, `.ah`, `.ac`, `.si`, `.sit`, `.bt`, `.pm`) are actively used and should be preserved until renderer output is changed.

## Safe Manual Candidates

These should be tested one at a time:

1. Merge the two section-heading background style blocks.
   - Expected saving: small, roughly 100-150 bytes.
   - Risk: low if the merged selector preserves `.tbw-section-heading table`.

2. Remove superseded early mobile offset rules after confirming the final mobile block covers them.
   - Candidate blocks include the early `.tbw-problem-east-mobile-offset` / `.tbw-solution-east-mobile-offset` values and early auction mobile widths.
   - Risk: medium, because Gmail/Pixel regressions have occurred around hand and auction alignment.

3. Collapse repeated MSO heading/auction declarations only after creating specific MSO-region fingerprints.
   - Expected saving: meaningful.
   - Risk: high, because Outlook spacing and Times New Roman rendering are protected production areas.

4. Promote repeated hand-card inline styles into already-used short classes only after renderer fixtures cover hand geometry.
   - Expected saving: meaningful.
   - Risk: medium-high, because Gmail and Outlook can differ on class support versus inline CSS.

## Do Not Optimize Yet

- Do not remove table attributes generically.
- Do not remove `mso-*` declarations generically.
- Do not remove or restructure conditional comments.
- Do not infer that duplicated-looking MSO blocks are redundant without Outlook-specific regression coverage.
- Do not class-compress protected regions until the renderer can reproduce and validate the compressed shape deterministically.

## Recommended Next Step

Make one small canonical simplification first: merge the duplicated section-heading background style blocks while preserving every selector and declaration currently represented by the pair. Then run:

- `pytest`
- `validators.run_all`
- protected-region fingerprinting
- export size analysis

If that passes, move to a dedicated MSO/mobile style-layer audit with fixture screenshots before larger reductions.

## Completed Audit Action

The duplicated section-heading background style blocks were merged after this audit:

- New source size: 85,118 bytes
- Bytes saved: 121
- Head style blocks: 18, down from 19
- Protected-region fingerprints: unchanged
- Validation status: unchanged; still human review required because source size remains above 85 KB
