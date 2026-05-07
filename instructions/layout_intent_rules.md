# Layout Intent Rules

Layout intent rules define content-agnostic display intentions inside JSON.

Layout intent is not HTML. It is a semantic instruction to the renderer.

## Purpose

Layout intent separates bridge/source meaning from HTML implementation.

The extraction and semantic bridge layers may identify facts such as:
- article type
- visible hands
- reader seat
- all four hands known
- auction present
- solution section present

The layout intent layer converts those facts into renderer-facing intents.

## Common layout intents and regression examples

### Declarer play vertical layout

Use when a `play_problem` source presents North and South for declarer play.

```json
{
  "article_type": "play_problem",
  "layout_intent": {
    "hand_layout": "vertical_ns",
    "visible_seats": ["N", "S"],
    "primary_hand_order": ["N", "S"]
  }
}
```

Expected rendering behavior:
- North appears above South.
- No West/East side columns are rendered.
- Facts appear above the hand layout unless the article object specifies another semantic placement.
- Outlook and Gmail must show the same vertical relationship.

### Defense/problem three-position layout

Use for defense/problem statements with North centered and one side defender hand.

```json
{
  "article_type": "defense_problem",
  "layout_intent": {
    "hand_layout": "three_position",
    "north_position": "center",
    "reader_seat": "E",
    "visible_seats": ["N", "E"],
    "empty_side": "W"
  }
}
```

Expected rendering behavior:
- North remains centered over the hand stage.
- If reader seat is `E`, East is placed in the right column and West is empty.
- If reader seat is `W`, West is placed in the left column and East is empty.
- Outlook-specific vertical offset/spacer behavior is preserved.

### Full deal cross layout

Use when all four hands are known and should be displayed.

```json
{
  "article_type": "historical_deal_article",
  "layout_intent": {
    "hand_layout": "cross_deal",
    "visible_seats": ["N", "W", "E", "S"],
    "facts_position": "upper_left"
  }
}
```

Expected rendering behavior:
- North appears at top.
- West and East appear side by side.
- South appears below.
- Deal facts appear once only in the upper-left facts position.
- Do not duplicate facts below the diagram.

### Bidding MSC single-hand layout

Use for Master Solvers' Club-style bidding problems.

```json
{
  "article_type": "bidding_msc",
  "layout_intent": {
    "hand_layout": "single_south",
    "visible_seats": ["S"],
    "auction_layout": "w_n_e_s_table",
    "action_score_table": true,
    "expert_commentary_blocks": true
  }
}
```

Expected rendering behavior:
- South hand appears as the only visible hand.
- Auction appears in W-N-E-S table form.
- Incomplete call appears in South with `?`.
- Action score table and expert commentary render after the hand/auction.

### Auction table layout

Use W-N-E-S rendering order for bridge auctions unless the source or article type requires otherwise.

```json
{
  "auction_layout": "w_n_e_s_table",
  "columns": ["W", "N", "E", "S"]
}
```

Expected rendering behavior:
- Renderer derives table columns from the semantic auction object.
- Empty visible auction cells render blank, not as dashes.
- When a level number is followed by a suit image, render one non-breaking space between them.

## What layout intent does not define

Layout intent does not define:
- CSS
- table widths
- fonts
- colors
- MSO conditionals
- minification
- production classes

Those belong to rendering and production export.

## Validation hooks

Layout intent validation must confirm:
- `visible_seats` equals the seats represented by visible hand objects.
- `reader_seat` is present for one-side defense layouts when source identifies the reader.
- `cross_deal` is used only when all four hands are represented.
- `single_south` is used for bidding MSC unless an explicit source exception exists.
- `auction_layout` is present when an auction object exists.

## Formal allowed layout intents

Allowed `hand_layout` values:

- `vertical_ns`
- `defense_three_position`
- `full_deal_cross`
- `bidding_single_south`
- `none`

Allowed `auction_layout` values:

- `wnes_table`
- `incomplete_wnes_table`
- `none`

Required mappings:
- `play_problem` -> `vertical_ns` unless source explicitly provides another layout intent
- `defense_problem` -> `defense_three_position` for problem statement when two visible hands are shown
- `historical_deal_article` with four known hands -> `full_deal_cross`
- `bidding_msc` -> `bidding_single_south` plus `incomplete_wnes_table`

The renderer must consume these layout intents directly. It must not infer layout from article text, hand count, title, or PDF appearance.

## Renderer-purity contract

Layout intent is the only layer allowed to translate semantic article type into renderer-facing display intent.

Rendering receives:
- canonical JSON
- layout intent
- asset map

Rendering does not decide article type, does not pair problems and solutions, and does not interpret bridge meaning.
