# Extraction Rules

Extraction rules govern source processing only.

## Scope

Extraction transforms uploaded PDFs, scans, pasted source text, or source images into raw semantic content that can populate the canonical JSON model.

Extraction rules may decide:
- which pages or regions belong to an article
- article type
- title, author, deck, issue metadata
- visible article wording
- hand diagrams as observed in the source
- auctions as observed in the source
- dealer and vulnerability as observed in the source
- captions, prompts, solution boundaries, and commentary boundaries

Extraction rules must not decide:
- HTML structure
- CSS, fonts, colors, spacing, or email-client fallbacks
- production minification
- Outlook or Gmail behavior
- final hand layout geometry in HTML
- bridge-theoretic corrections not present in the source

## Source fidelity

Treat uploaded article sources as content truth.

If source content is uncertain:
- do not guess card holdings
- do not guess auctions
- do not guess dealer or vulnerability
- do not invent missing article wording
- fail or request clarification when needed

## PDF/source processing

For paginated visual sources, build a display-independent semantic source object before rendering.

Extraction should identify:
- source page(s)
- article boundaries
- article type
- visible hands
- visible auctions
- facts: dealer, vulnerability, scoring, contract, lead where present
- problem statement text
- solution text
- expert commentary where present

## Article type detection

Detect article type from source content, not from rendering needs:

- `bidding_msc`: one visible South hand plus incomplete auction ending with `?` in South.
- `play_problem`: declarer-play problem, usually two visible hands in the problem statement.
- `defense_problem`: defensive problem, usually North/dummy plus a reader defender hand.
- `historical_deal_article`: four visible hands in primary article body with report/reprint framing and no explicit reader prompt.

Article type is stored in JSON and later used by semantic bridge and layout-intent layers.

## Extraction output

Extraction output must populate JSON fields defined in `semantic_schema.md`. Extraction does not render HTML.

## Required source processing sequence

Before extracting content from any paginated PDF or scan, perform this sequence:

1. Build a source inventory for every uploaded file.
2. Classify each source as one of:
   - problem prompt
   - solution article
   - combined problem-and-solution article
   - article reprint
   - template/reference fixture
   - unrelated/supporting file
3. For each paginated source, generate page images first.
4. Extract from the page images and parsed text together.
5. Build a display-independent source object before populating semantic JSON.
6. Do not rely on PDF text extraction alone for hands, auctions, diagrams, tables, or layout-sensitive bridge content.

Hard fail if page images cannot be generated for a PDF and the requested output depends on diagrammatic content.

## Multi-file problem/solution pairing

When problems and solutions are supplied in different files:

- Pair each solution with its corresponding problem before extraction is considered complete.
- Match by article title, problem number/letter, visible hands, dealer, vulnerability, auction, contract, opening lead, and nearby headings.
- Do not pair by upload order alone.
- If multiple plausible pairings remain, fail and report the ambiguity.
- The final article object must combine the problem statement and matching solution into one semantic article object unless the user explicitly requests separate outputs.

## MSC source selection

For Master Solvers' Club or bidding MSC articles:

- If a current prompt/problem article and a later solution/discussion article are both available, extract expert commentary, action scores, recommendations, and final conclusions from the solution/discussion article.
- Use the prompt/problem article only for the problem statement, hand, vulnerability/dealer, and incomplete auction when those elements are not fully repeated in the solution article.
- Never substitute prompt-only content for solution commentary.
- If the source set contains only the prompt/problem article, mark solution/commentary fields as unavailable rather than inventing them.

## Source ambiguity failures

Extraction must fail rather than guess when:

- article type is uncertain
- a solution cannot be confidently paired to a problem
- an MSC prompt is mistaken for a solution source
- hand, auction, dealer, vulnerability, contract, or opening lead content is visually unclear
- source files conflict and no authoritative source is designated

## Ordered article classification and source inventory

Before extracting content, build a source inventory for every uploaded file.

For each source file, classify it as one of:
- problem prompt
- solution article
- combined problem-and-solution article
- reference/template fixture
- unknown

Article-type classification must be ordered and explicit:
1. bidding_msc
2. play_problem
3. defense_problem
4. historical_deal_article
5. other_feature_article

If a source satisfies more than one article type with similar confidence, extraction must fail and report the ambiguity.

For Master Solvers' Club or similar bidding/problem material:
- if both a prompt-only problem and a solution article are supplied, extract action scores, expert commentary, and recommendation/conclusion from the solution article, not from the prompt-only problem
- extract the problem hand and incomplete auction only from the prompt or from the matching problem statement embedded in the solution article
- never use a current prompt article as if it contains the final solution commentary

When problems and solutions are in different files:
- pair each solution to its corresponding problem using article title, problem number, deal facts, visible hands, auction, contract, opening lead, and article heading
- never pair by file order alone
- if more than one plausible pairing exists, fail and report the ambiguity

## Source bridge inconsistency detection

Extraction must record source-level bridge inconsistencies rather than silently resolving them.

Hard-fail and alert the user when the source contains or appears to contain:
- the same card appearing in more than one hand in the same deal
- a hand with more than 13 cards when a full hand is asserted
- a full deal with fewer or more than 52 unique cards
- impossible suit/rank tokens
- inconsistent dealer or vulnerability between matched problem and solution
- a hand in a solution that conflicts with the corresponding hand in the problem
- an auction that cannot legally follow from the dealer/seat sequence
- a play sequence that uses a card not held by that player, follows suit incorrectly when the source shows the player could follow, or otherwise violates known bridge constraints
- a contract/opening lead/play description that contradicts the semantic deal facts

If the inconsistency may be due to OCR/source unreadability, report it as uncertain extraction and fail rather than guessing.

Do not correct source bridge errors unless the user explicitly requests an editorial correction. The default output is an alert identifying the inconsistency and the conflicting source facts.

## Do-not-infer source facts

Never infer these facts unless they are explicitly present in the source or derivable by a stated bridge-rule validation step:
- hidden cards
- unstated dealer
- unstated vulnerability
- unstated calls
- unstated opening lead
- unstated play sequence
- unstated problem/solution pairing
- unstated article type
- unstated layout intent

If a necessary fact is absent or ambiguous, extraction must fail or mark the field unknown according to the semantic schema.

## Problem/solution pairing confidence rubric

Problem/solution pairing must use evidence.

Strong evidence:
- exact article title and problem number match
- identical visible hand plus identical auction/deal facts
- explicit source cross-reference

Moderate evidence:
- matching title/series plus matching deal facts
- matching visible hand plus matching contract/lead

Weak evidence:
- same author only
- same issue only
- same file order only
- similar topic only

Pairing requires strong evidence or multiple moderate evidence points. File order alone is invalid.

## OCR and visual-confidence handling

OCR or visual extraction confidence must be tracked for bridge-critical regions.

Bridge-critical low-confidence regions require human review or hard fail:
- card ranks
- suit symbols
- dealer
- vulnerability
- auction calls
- contract
- opening lead
- problem number/title used for pairing

Common ambiguity examples:
- `8` vs `B`
- `10` vs `T` vs `1O`
- `1` vs `I` vs `l`
- suit symbols confused with decorative icons
- diamond/heart symbol confusion in poor scans
- spade/club symbol confusion in low contrast

If a low-confidence region affects bridge semantics, do not infer a correction. Report the uncertainty.

## Image preprocessing guidance

For paginated PDFs and scanned sources, rasterization should use settings that preserve bridge symbols and small ranks.

Recommended preprocessing before semantic extraction:
- render each page to image before reading
- use sufficiently high resolution for small suit/rank glyphs
- preserve original page ordering and page identifiers
- crop only after saving the full-page raster reference
- avoid destructive thresholding that can erase suit pips
- use contrast normalization only when it improves symbol readability
- retain links from extracted objects back to page/region references

Extraction should be reproducible from saved page images and extraction parameters.

## Known impossible-to-infer examples

Examples of facts that must not be inferred without explicit source support:

- reconstructing unseen hands from a partial play sequence
- inferring vulnerability from score language alone when not stated
- inferring dealer from auction alignment when the visual table is ambiguous
- inferring a missing call because a later contract seems likely
- inferring a hidden card from standard bridge logic
- inferring that two files are paired because they are adjacent in upload order
- inferring article type from author or series name alone

When these are needed but not explicit, fail or request clarification.
