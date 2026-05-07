# Rendering Rules

Rendering rules govern how validated semantic JSON and layout intents become authoring HTML.

Rendering rules are content-agnostic. They must not contain PDF extraction heuristics or bridge semantic normalization rules.

## Template

Render from `templates/authoring_canonical.html`.

Preserve:
- canonical shell
- MailerLite tokens
- VML button markup
- Stay Connected section
- footer
- Outlook/MSO conditional structures
- designated editable regions

## Article content

Render article text exactly as stored in JSON.

Do not edit article wording, cards, auctions, dealer, vulnerability, contracts, or source facts during rendering. Those are governed by `semantic_bridge_rules.md`.

## Suit images

Never render raw suit glyphs in visible bridge content. Use image tags.

Use logical assets from the JSON asset map and concrete URLs from `manifest.md`.

Production-safe suit image classes:
- `si` for inline auction/commentary suits
- `sit` for stacked hand-table suit icons

Keep on suit images:
- `src`
- `alt`
- `width`
- `height`

## Compass labels

Rendering controls display capitalization.

In hand diagrams, compass-direction labels render uppercase:
- `NORTH`
- `SOUTH`
- `EAST`
- `WEST`

In prose under/around diagrams, render normal initial capitalization unless source text says otherwise:
- `North`
- `South`
- `East`
- `West`

## Hand diagrams

Use layout intents from `layout_intent_rules.md`.

Preserve:
- table geometry
- seat placement
- row heights where Outlook-sensitive
- suit image dimensions
- Outlook-specific hand spacers

Hand label cells are Outlook-sensitive. They must retain inline Times New Roman and bold protection or an Outlook-specific equivalent.

## Auctions

Render auctions from semantic auction objects.

Non-Outlook auction tables may be class-compressed if visual behavior is preserved.

Outlook/MSO auction tables are rendering stabilizers. Do not remove or merge them in normal rendering.

Preserve in MSO auction markup:
- separate Outlook table structure
- row heights
- line heights
- `mso-line-height-rule`
- `mso-height-rule`
- span wrappers
- inline Times New Roman
- bold column headers
- suit image alignment

## Background roles

Rendering must preserve these visual roles:
- outer page/gutters: light gray
- inner 600px shell: white
- main content cells: white
- Problem/Solution heading band: visible light gray
- heading left accent bar: dark gray
- auction headers: gray
- Outlook spacer below heading: white unless a tested design says otherwise

## Outlook-sensitive text

Outlook desktop may ignore inherited/class font declarations.

Keep or restore inline/conditional Times New Roman protection for:
- newsletter identity
- hand compass labels
- MSO auction tables
- Stay Connected section
- footer where visually important

If a sensitive row still fails in Outlook, use an Outlook-only conditional row or MSO conditional CSS.

## Protected rendering regions

The following regions are protected because prior testing showed they are fragile across Outlook desktop, Gmail/Pixel, and webmail:

- newsletter identity
- hand labels / compass direction labels
- auction tables
- Problem/Solution heading bands
- Stay Connected section
- footer
- Outlook/MSO auction blocks
- Outlook/MSO spacers
- VML buttons
- outer gutter and inner shell backgrounds

In protected regions, rendering and optimization must preserve critical inline or conditional styles unless a user explicitly authorizes a visual change.

Critical protected properties include:

- `font-family`
- `font-weight`
- `font-size`
- `height`
- `line-height`
- `mso-line-height-rule`
- `mso-height-rule`
- `mso-padding-alt`
- `padding`
- `vertical-align`
- `background-color`
- `bgcolor`
- `width` / `height` table attributes where Outlook uses them
- MSO conditional comments and non-MSO conditional wrappers

## Email assembly order

The final rendered newsletter must assemble sections in this order:

1. preheader
2. outer shell and header
3. newsletter identity
4. editor note
5. forward/share and signup block
6. article heading
7. article body
8. Stay Connected
9. footer

Hard fail if:

- Stay Connected appears before article body completion
- footer appears before article body completion
- article content appears after Stay Connected
- article content appears after the footer
- more than one article body block is visibly populated
- an unused article block contains visible content

## Platform accommodation requirements

Generated HTML must retain tested accommodations for:

- Outlook desktop / Word rendering
- Gmail mobile on Pixel-class screens
- Gmail webmail
- Apple Mail / iOS mail clients

The renderer must keep table-based layout for bridge diagrams, auctions, heading bands, invariant sections, and VML buttons.

Do not introduce div-only layout for email-critical regions.

## Renderer purity

Rendering must be deterministic and content-agnostic.

Rendering must not:
- inspect PDF/source files
- classify article type
- pair problem/solution files
- infer bridge meaning
- infer layout from title text, hand count, or visual source shape
- correct source bridge inconsistencies

Rendering consumes only validated canonical JSON, layout intents, and the asset map.

## Protected output regions

The following regions are protected:

- newsletter identity
- share/signup block
- article heading
- Problem/Solution section headings
- hand geometry
- hand compass labels
- auction tables
- Outlook/MSO auction blocks
- Outlook/MSO spacers
- Stay Connected
- footer

Protected inline properties must not be removed or class-compressed in these regions unless an equivalent Outlook-tested replacement exists:
- `font-family`
- `font-weight`
- `height`
- `line-height`
- `mso-line-height-rule`
- `mso-height-rule`
- `padding`
- `mso-padding-alt`
- `vertical-align`
- `background-color`
- `bgcolor`
- table `width`, `height`, `valign`, and `align` attributes where Outlook depends on them

Known Outlook-sensitive text requiring inline or conditional font protection:
- newsletter identity
- hand compass labels
- auction headers and cells
- Stay Connected
- footer

## Mobile rendering constraints

Mobile rendering must preserve:
- no horizontal scroll in Gmail/Pixel
- readable body text at mobile override size
- hand diagrams must not wrap seat labels or card ranks unexpectedly
- auction headers must not wrap
- suit images must remain aligned with adjacent ranks/calls
- central shell may become full width on small screens
- outer gutters may collapse on mobile, but desktop gutters must remain gray
- Problem/Solution heading bands must remain visible

Any change to production classes, hand layout, auction layout, or responsive CSS requires Gmail/Pixel regression testing.

## Template edit-region ownership

Templates contain three region types:

- semantic content regions: populated from canonical JSON
- renderer-owned regions: generated by renderer components and layout intents
- invariant shell regions: header, buttons, Stay Connected, footer, MailerLite tokens, and platform fallbacks

Generation may modify only semantic content regions and renderer-owned generated output. It must not alter invariant shell regions except through approved template architecture changes.

## Protected authoring sentinels

Authoring templates may contain protected-region sentinels such as:
- `PROTECTED:NEWSLETTER_IDENTITY`
- `PROTECTED:MSO_AUCTION`
- `PROTECTED:HAND_GEOMETRY`
- `PROTECTED:STAY_CONNECTED`
- `PROTECTED:FOOTER`

Renderers and production exporters must respect these sentinels before stripping comments in final production output.

## Accessibility policy

Suit images in bridge content must include meaningful alt text:
- spade: `♠` or `spade`
- heart: `♥` or `heart`
- diamond: `♦` or `diamond`
- club: `♣` or `club`

Logo images must retain meaningful alt text.

Production export may remove redundant presentational attributes only if doing so does not remove required accessible names or break email rendering.

## Immutable visual rendering invariants

The following visual invariants are part of the canonical Bridge World email identity:

- gray desktop gutters around the central shell
- white central content shell
- visible gray Problem/Solution heading bands
- dark left accent on Problem/Solution heading bands
- Times New Roman in Outlook-sensitive regions
- compact Outlook auction row spacing
- stable hand geometry and compass-label placement
- suit image alignment with adjacent ranks/calls
- invariant Stay Connected section
- invariant footer structure
- MailerLite forward/signup tokens preserved

A rendering that is semantically correct but violates these visual invariants is not production-valid.

## Renderer component ownership

Renderer-owned components:

- newsletter identity renderer
- editor note renderer
- article heading renderer
- section heading renderer
- hand renderer
- auction renderer
- bridge facts renderer
- CTA/share/signup renderer
- Stay Connected renderer
- footer renderer
- Outlook/MSO fallback renderer
- production asset renderer

Each component receives canonical JSON and layout intent. Components must not reach back into source PDFs or infer bridge meaning.
