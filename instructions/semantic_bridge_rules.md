# Semantic Bridge Rules

Semantic bridge rules govern bridge meaning inside JSON.

They do not govern PDF extraction and do not govern HTML rendering.

## Content fidelity

Never invent or modify:
- card holdings
- auctions
- dealer
- vulnerability
- contracts
- opening leads
- article wording

unless the user explicitly requests editorial rewriting or correction.

## Seats

Internally normalize seats as:

- `N` = North
- `S` = South
- `E` = East
- `W` = West

Bridge semantics use these abbreviations. Rendering decides whether display text is `NORTH`, `North`, or another form.

## Hand validation

For any full hand known from source:
- preserve suit membership exactly
- preserve ranks exactly
- do not reorder between suits
- do not infer missing cards unless the source explicitly gives the full deal and the inference is requested and validated

For visible hands:
- keep only visible source holdings
- do not complete unseen hands

## Suit order

Store and render bridge hands in standard suit order unless source explicitly requires another order:

1. Spades
2. Hearts
3. Diamonds
4. Clubs

## Auction normalization

Auctions are stored as seat-owned calls.

When a visual auction is extracted, normalize it into the canonical W-N-E-S structure while preserving:
- dealer
- seat ownership of each call
- pass/double/redouble notation
- incomplete auction marker
- alerts/footnotes where present

Do not render auctions by copying visual source layout. The renderer receives semantic auction data and produces the proper table.

## Bidding MSC semantics

For `bidding_msc`:
- South owns the visible hand.
- The auction is incomplete.
- The incomplete call ends with `?` in South.
- Action-score tables and expert commentary remain separate semantic blocks.

## Play/defense semantics

For play and defense problems:
- store the reader seat if identifiable.
- store dummy/declarer/defender labels when source provides them.
- store problem facts separately from prose.
- solution hands may differ from problem-statement visible hands and must be separately represented when needed.

## No rendering decisions

Semantic bridge rules may create a normalized auction or hand object. They must not decide HTML table widths, colors, font sizes, spacer rows, or email-client fallbacks.

## Auction canonicalization and validation

Auction data is semantic bridge content.

Store auctions as seat-owned calls, not copied visual tables.

Required auction object properties:

- `dealer`
- `seat_order`
- `rounds`
- `calls`
- `incomplete`
- `final_contract` when source provides it
- `source_trace` for each call when available

## W-N-E-S rendering derivation

All rendered auction tables must display columns in this order:

`W | N | E | S`

The semantic auction may begin with any dealer. The renderer must derive blank leading cells from the dealer offset.

Rules:

- West dealer: first call appears in W column.
- North dealer: first call appears in N column; W is blank.
- East dealer: first call appears in E column; W and N are blank.
- South dealer: first call appears in S column; W, N, and E are blank.
- Empty cells are blank, not dashes.
- An incomplete MSC auction ending with a question must preserve the question in the correct seat cell.

## Auction round-trip validation

Before rendering export:

1. Convert source auction into semantic calls.
2. Derive the W-N-E-S display table from the semantic calls.
3. Parse the rendered auction table back into calls.
4. Compare the parsed calls with the semantic object.

Hard fail if any call, seat, order, blank, double/redouble, pass, question mark, or suit denomination differs.

Never copy a visual source auction table directly into final HTML.

## Source consistency validation

Semantic bridge validation must detect impossible or inconsistent bridge content in the source.

Validate:
- each card appears at most once within any single deal object
- known full hands contain exactly 13 cards
- known full deals contain exactly 52 unique cards
- visible partial hands do not contradict full-deal information when both are present
- problem and solution versions of the same hand agree unless the source explicitly states a correction
- dealer and vulnerability agree across paired problem/solution files
- auction calls are legal in sequence with dealer and seat order
- doubles/redoubles occur only when legally available
- an auction ends legally when marked complete
- play sequences use cards held by the player when holdings are known
- play sequences respect following-suit requirements when source-known holdings prove the obligation

If validation detects a source inconsistency, do not repair it silently. Add a hard-fail source issue and alert the user.

## Auction legality

Auction validation must treat the semantic auction as a bridge object, not as a copied visual table.

Validate:
- calls are assigned to the correct seats in rotation from dealer
- bid levels increase legally
- strains are ordered clubs, diamonds, hearts, spades, notrump
- pass, double, and redouble are legal in context
- incomplete auctions may end with `?` only for the question seat
- rendered W-N-E-S tables must round-trip exactly to the semantic auction object

Impossible source auctions must be reported as source inconsistencies rather than normalized into plausible legal auctions.

## Canonical card-rank formatting

Canonical internal rank order is:

`A K Q J 10 9 8 7 6 5 4 3 2`

Use `10` rather than `T` in canonical JSON unless the source explicitly uses `T` and fidelity requires preserving it in source text.

Hand holdings should be stored as space-separated rank strings by suit, for example:
- `"A Q 10 3"`
- `"8 6 5 4"`
- `""` for a known void
- `null` or omitted suit only when the suit is unknown/not extracted

Do not mix `T` and `10` inside canonical holdings.

Rendering may preserve source prose wording, but generated hand diagrams should use canonical holdings exactly.
