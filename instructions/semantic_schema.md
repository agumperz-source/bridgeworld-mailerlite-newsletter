# Semantic Schema Definitions

The semantic JSON model is the contract between extraction, semantic bridge logic, layout intent, rendering, production export, and validation.

This file is the sole authority for JSON object shapes. Other layers may validate or consume these objects, but should not redefine their structure.

## Top-level newsletter object

A newsletter object contains:

- `newsletter_identity`
- `publication_date`
- `preheader_text`
- `editor_note`
- `article`
- `asset_map`
- `layout_intents`
- `validation_status`

```json
{
  "newsletter_identity": "The Bridge World Newsletter • May 6, 2026",
  "publication_date": "2026-05-06",
  "preheader_text": "A Pair by Kantar, XI — two defense problems by Edwin B. Kantar",
  "editor_note": {
    "title": "",
    "html": "<p>This week's Newsletter features two classic rubber-bridge defensive problems from Eddie Kantar.</p>"
  },
  "article": {},
  "asset_map": {
    "S": "https://agumperz-source.github.io/bw/a/S.png",
    "H": "https://agumperz-source.github.io/bw/a/H.png",
    "D": "https://agumperz-source.github.io/bw/a/D.png",
    "C": "https://agumperz-source.github.io/bw/a/C.png",
    "BW": "https://agumperz-source.github.io/bw/a/BW.png",
    "logo": "https://agumperz-source.github.io/bw/a/logo.png"
  },
  "layout_intents": [],
  "validation_status": {
    "extraction": "pending",
    "semantic_bridge": "pending",
    "layout_intent": "pending",
    "rendering": "pending",
    "production": "pending"
  }
}
```

## Article object

An article object contains:

- `article_type`
- `title`
- `deck`
- `series_name`
- `author_and_level`
- `body_blocks`
- `problems`
- `source_references`

Article visible wording must be stored as source-preserved text blocks unless the user explicitly requests editorial rewriting.

```json
{
  "article_type": "defense_problem",
  "title": "A Pair by Kantar, XI",
  "deck": "",
  "series_name": "",
  "author_and_level": "by Edwin B. Kantar",
  "body_blocks": [
    {"type": "paragraph", "text": "Assume a rubber-bridge setting."}
  ],
  "problems": [],
  "source_references": [
    {"source_id": "uploaded_pdf_1", "pages": [1, 2]}
  ]
}
```

## Problem object

A problem object contains:

- `problem_id`
- `facts`
- `visible_hands`
- `auction`
- `prompt_text`
- `solution`
- `layout_intent`

```json
{
  "problem_id": "1",
  "facts": {
    "dealer": "W",
    "vulnerability": "None",
    "scoring": "Rubber bridge",
    "contract": "4S",
    "declarer": "S",
    "opening_lead": "H9",
    "other_source_facts": []
  },
  "visible_hands": [],
  "auction": null,
  "prompt_text": [
    {"type": "paragraph", "text": "Plan your defense."}
  ],
  "solution": {
    "body_blocks": [],
    "visible_hands": [],
    "auction": null
  },
  "layout_intent": {}
}
```

## Facts object

A facts object may contain:

- `dealer`
- `vulnerability`
- `scoring`
- `contract`
- `declarer`
- `opening_lead`
- `other_source_facts`

Use normalized seat abbreviations internally:
- `N`
- `S`
- `E`
- `W`

Display names are produced by rendering rules.

## Hand object

Hands must be stored semantically as:

```json
{
  "seat": "N",
  "label_qualifier": "dummy",
  "suits": {
    "S": ["A", "Q", "10", "3"],
    "H": ["8", "6", "5", "4"],
    "D": ["10", "2"],
    "C": ["8", "7", "4"]
  }
}
```

Use suit keys:
- `S`
- `H`
- `D`
- `C`

Use rank tokens:
- `A`, `K`, `Q`, `J`, `10`, `9`, ... `2`
- empty array for voids where explicitly present

## Auction object

Auctions must be stored semantically, not as copied visual HTML.

```json
{
  "dealer": "W",
  "columns": ["W", "N", "E", "S"],
  "calls": [
    {"seat": "W", "call": "Pass"},
    {"seat": "N", "call": "Pass"},
    {"seat": "E", "call": "Pass"},
    {"seat": "S", "call": "1S"}
  ],
  "incomplete": false,
  "notes": []
}
```

The `columns` field stores normalized W-N-E-S rendering order when applicable. Calls remain seat-owned.

## Layout intent object

Layout intent is content-agnostic. It tells the renderer what layout family to use without specifying HTML or CSS.

```json
{
  "hand_layout": "three_position",
  "visible_seats": ["N", "E"],
  "reader_seat": "E",
  "auction_layout": "w_n_e_s_table"
}
```

## Complete example: defense problem article

```json
{
  "article_type": "defense_problem",
  "title": "A Pair by Kantar, XI",
  "deck": "",
  "series_name": "",
  "author_and_level": "by Edwin B. Kantar",
  "body_blocks": [
    {"type": "paragraph", "text": "Assume a rubber-bridge setting."}
  ],
  "problems": [
    {
      "problem_id": "1",
      "facts": {"dealer": "W", "vulnerability": "None", "scoring": "Rubber bridge"},
      "visible_hands": [
        {
          "seat": "N",
          "label_qualifier": "dummy",
          "suits": {"S": ["5", "4", "3"], "H": ["J", "10", "6"], "D": ["A", "9", "7"], "C": ["Q", "10", "9", "7"]}
        },
        {
          "seat": "E",
          "label_qualifier": "you",
          "suits": {"S": ["A", "J", "7", "2"], "H": ["7", "5", "3"], "D": ["6", "4", "3"], "C": ["K", "6", "2"]}
        }
      ],
      "auction": {
        "dealer": "W",
        "columns": ["W", "N", "E", "S"],
        "calls": [
          {"seat": "W", "call": "Pass"},
          {"seat": "N", "call": "Pass"},
          {"seat": "E", "call": "Pass"},
          {"seat": "S", "call": "1S"}
        ],
        "incomplete": false,
        "notes": []
      },
      "prompt_text": [{"type": "paragraph", "text": "Plan your defense."}],
      "solution": {"body_blocks": [], "visible_hands": [], "auction": null},
      "layout_intent": {
        "hand_layout": "three_position",
        "north_position": "center",
        "reader_seat": "E",
        "visible_seats": ["N", "E"],
        "auction_layout": "w_n_e_s_table"
      }
    }
  ],
  "source_references": []
}
```

## Complete example: play problem article

```json
{
  "article_type": "play_problem",
  "title": "Test Your Play",
  "deck": "Advanced declarer-play problem",
  "series_name": "",
  "author_and_level": "",
  "body_blocks": [],
  "problems": [
    {
      "problem_id": "A",
      "facts": {"dealer": "W", "vulnerability": "NS", "scoring": "Rubber bridge"},
      "visible_hands": [
        {"seat": "N", "label_qualifier": "dummy", "suits": {"S": ["A", "Q", "10", "3"], "H": ["8", "6", "5", "4"], "D": ["10", "2"], "C": ["8", "7", "4"]}},
        {"seat": "S", "label_qualifier": "declarer", "suits": {"S": ["2"], "H": ["A"], "D": ["A", "K", "Q", "J", "9", "8"], "C": ["A", "K", "5", "3", "2"]}}
      ],
      "auction": null,
      "prompt_text": [{"type": "paragraph", "text": "Plan the play."}],
      "solution": {"body_blocks": [], "visible_hands": [], "auction": null},
      "layout_intent": {"hand_layout": "vertical_ns", "visible_seats": ["N", "S"]}
    }
  ],
  "source_references": []
}
```

## Complete example: bidding MSC article

```json
{
  "article_type": "bidding_msc",
  "title": "Master Solvers' Club",
  "deck": "",
  "series_name": "Master Solvers' Club",
  "author_and_level": "",
  "body_blocks": [],
  "problems": [
    {
      "problem_id": "Problem 1",
      "facts": {"dealer": "N", "vulnerability": "Both", "scoring": "Matchpoints"},
      "visible_hands": [
        {"seat": "S", "label_qualifier": "", "suits": {"S": ["A", "Q", "7"], "H": ["K", "10", "4"], "D": ["Q", "8", "3"], "C": ["A", "J", "5"]}}
      ],
      "auction": {
        "dealer": "N",
        "columns": ["W", "N", "E", "S"],
        "calls": [
          {"seat": "N", "call": "1H"},
          {"seat": "E", "call": "Pass"},
          {"seat": "S", "call": "?"}
        ],
        "incomplete": true,
        "notes": []
      },
      "prompt_text": [],
      "solution": null,
      "layout_intent": {"hand_layout": "single_south", "auction_layout": "w_n_e_s_table"}
    }
  ],
  "source_references": []
}
```

## Complete example: historical deal article

```json
{
  "article_type": "historical_deal_article",
  "title": "A Famous Deal",
  "deck": "",
  "series_name": "",
  "author_and_level": "",
  "body_blocks": [
    {"type": "paragraph", "text": "The deal occurred in a major match."}
  ],
  "problems": [
    {
      "problem_id": "deal",
      "facts": {"dealer": "S", "vulnerability": "EW", "scoring": "IMP"},
      "visible_hands": [
        {"seat": "N", "label_qualifier": "", "suits": {"S": ["A"], "H": [], "D": [], "C": []}},
        {"seat": "W", "label_qualifier": "", "suits": {"S": [], "H": [], "D": [], "C": []}},
        {"seat": "E", "label_qualifier": "", "suits": {"S": [], "H": [], "D": [], "C": []}},
        {"seat": "S", "label_qualifier": "", "suits": {"S": [], "H": [], "D": [], "C": []}}
      ],
      "auction": null,
      "prompt_text": [],
      "solution": null,
      "layout_intent": {"hand_layout": "cross_deal", "visible_seats": ["N", "W", "E", "S"], "facts_position": "upper_left"}
    }
  ],
  "source_references": []
}
```

## Schema ownership

Extraction populates this schema. Semantic bridge rules normalize bridge meaning inside this schema. Layout intent rules populate renderer-facing layout fields. Rendering consumes this schema and must not reinterpret PDF/source content.

## Canonicality invariant

Canonical JSON is the only semantic source of truth after extraction.

HTML must never be treated as semantic source truth except in REVISE_HTML mode, where uploaded HTML is first parsed back into canonical JSON and then validated.

Rendering must be deterministic from canonical JSON plus layout intents alone. The renderer must not infer bridge meaning from HTML, CSS, visual spacing, or platform-specific markup.

Semantic correctness and visual correctness are independent validation domains:
- bridge-valid JSON can still render incorrectly
- visually correct HTML can still contain semantic bridge errors
Both domains must pass their own validators.

## Source issue reporting schema

Source inconsistencies and extraction uncertainties are recorded in `validation_status.source_issues`.

Example:

```json
{
  "validation_status": {
    "source_issues": [
      {
        "severity": "hard_fail",
        "type": "problem_solution_hand_mismatch",
        "message": "East spades differ between problem and solution.",
        "source_refs": ["problem_file_page_1", "solution_file_page_2"],
        "conflicting_values": {
          "problem": {"E": {"S": "A J 7 2"}},
          "solution": {"E": {"S": "A J 6 2"}}
        }
      }
    ]
  }
}
```

A hard-fail source issue prevents rendering and production export.

## Auction edge-case schema examples

### Passed-out board

```json
{
  "dealer": "W",
  "auction": {
    "call_order": [
      {"seat": "W", "call": "Pass"},
      {"seat": "N", "call": "Pass"},
      {"seat": "E", "call": "Pass"},
      {"seat": "S", "call": "Pass"}
    ],
    "status": "complete",
    "result": "passed_out"
  }
}
```

### Double and redouble

```json
{
  "dealer": "N",
  "auction": {
    "call_order": [
      {"seat": "N", "call": "1H"},
      {"seat": "E", "call": "Double"},
      {"seat": "S", "call": "Redouble"},
      {"seat": "W", "call": "2C"}
    ],
    "status": "in_progress"
  }
}
```

### Incomplete auction with dealer offset

```json
{
  "dealer": "E",
  "auction": {
    "call_order": [
      {"seat": "E", "call": "1S"},
      {"seat": "S", "call": "Pass"},
      {"seat": "W", "call": "2S"},
      {"seat": "N", "call": "?"}
    ],
    "status": "incomplete",
    "question_seat": "N"
  }
}
```

The renderer derives W-N-E-S columns and blank leading cells from `dealer` and `call_order`; blank cells are semantic blanks, never dashes.

## Issue cardinality policy

A production newsletter issue contains exactly one primary `article` object.

Supporting content may exist only as:
- `editor_note`
- invariant shell sections
- article subsections inside the single primary article
- validation/source reports outside the rendered email

Do not render multiple independent primary articles in one issue unless the schema and renderer are explicitly extended.

## Semantic and rendering version metadata

Reports and generated artifacts should record:
- `semantic_schema_version`
- `semantic_bridge_version`
- `layout_intent_version`
- `rendering_profile_version`
- `production_export_version`
- `asset_map_version`

These versions allow future newsletters to be compared across rule changes.
