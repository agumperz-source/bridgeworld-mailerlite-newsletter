# Component Style Rules

These component rules capture the current preferred look and the known platform traps.

## Auction Tables

All auctions must share one visual family:

- Times New Roman.
- Four equal columns in `WEST / NORTH / EAST / SOUTH` order.
- Thin neutral border.
- Gray header row.
- Left-aligned calls.
- Compact row rhythm.
- Suit images aligned with adjacent calls.

Preferred compact MSC auction:

- `width:320px` to `360px`
- `max-width:100%`
- `table-layout:fixed`
- `border-collapse:separate`
- `border:1px solid #999999`
- cell padding around `6px 8px`

Preferred longer play/defense auction:

- wider only when needed, usually max `500px`
- same compact visual language
- avoid `10px 12px` padding unless a tested client fix requires it

## Bidder-Name Rows

Some auctions need a row identifying the table players.

Render as an optional row directly under the seat header row:

- italic
- smaller or lighter than calls
- pale gray background
- one name per compass seat

Do not put bidder names into the first call row or into footnotes.

## Auction Footnotes

Footnotes must be outside the auction table.

Preferred shape:

- immediately below the auction
- aligned to the auction table width and left edge
- `font-size:13px`
- `line-height:18px`
- gray text
- modest top padding, around `6px`

Do not render footnotes as a `colspan="4"` row inside the auction table. That makes the auction feel like a notes box and is not the preferred presentation.

Use superscript markers in calls when possible:

- `1 NT<sup>*</sup>`
- `2 <img ...><sup>**</sup>`

## Action-Score Tables

Preferred MSC scoring table:

- `width:auto`
- `border-collapse:collapse`
- `border:1px solid #9a9a9a`
- gray header row
- compact `6px` padding
- action column left-aligned
- score and votes columns right-aligned

## Hand Diagrams

Prefer stable table geometry over percentage spacer improvisation.

Declarer-play problem:

- use vertical North/South layout.

Defense problem:

- use the tested three-position stage geometry.
- North remains stable above the side hand.
- West reader hand goes left.
- East reader hand goes right.

Full-deal solution:

- use tested cross layout.
- avoid arbitrary percentage spacer columns unless a platform-tested template owns them.

## Stay Connected And Footer

Stay Connected and footer must live inside the active content column.

Do not create a second `600px` shell or a `548px` inner wrapper beneath the article body. That causes double insets and prevents the bottom section from spanning the column.

## Template Families

The current production shell is Template Family 1: Classic Editorial.

Future redesigns may introduce additional template families, but they must reuse or deliberately replace validated bridge components rather than forking ad hoc HTML.

