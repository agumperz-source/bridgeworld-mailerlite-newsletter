# Validators

This directory defines the validator implementation roadmap for Codex.

Validators must be implemented as deterministic scripts and wired into the production pipeline.

## Required validators

1. `schema_validator`
   - validates newsletter JSON against `schema/newsletter.schema.json`

2. `source_inventory_validator`
   - verifies source inventory exists
   - verifies each uploaded file is classified
   - verifies problem/solution pairings have evidence

3. `bridge_consistency_validator`
   - detects duplicate cards
   - validates full hands and full deals
   - validates problem/solution hand consistency
   - validates dealer/vulnerability consistency
   - validates impossible auctions and impossible play sequences when enough data is known

4. `auction_validator`
   - validates legal call order from dealer
   - validates W-N-E-S table derivation
   - validates incomplete auctions and question seats
   - validates round-trip from rendered auction back to semantic auction

5. `layout_intent_validator`
   - verifies article type and layout intent compatibility
   - verifies visible seats match visible hands
   - verifies full-deal layouts only when all four hands are known

6. `rendering_validator`
   - verifies canonical shell invariants
   - verifies section order
   - verifies Stay Connected and footer placement
   - verifies protected-region markers remain present in authoring output
   - verifies no raw suit glyphs appear in bridge content

7. `production_validator`
   - verifies production output has no generation comments
   - verifies no legacy MailerLite suit/logo URLs
   - verifies size gates
   - verifies no empty style/class attributes
   - verifies protected Outlook/MSO blocks are still present
   - verifies export idempotence

8. `visual_regression_checklist`
   - records Outlook desktop, Gmail Android/Pixel, Gmail web, and Apple Mail/iPhone checks when applicable

## Implementation expectation

Codex should implement these as scripts or tests. The instruction files are the source of truth; validators enforce them and must not redefine them.

## Package test command

Codex should provide a single command, for example:

```bash
python -m validators.run_all --package .
```

The command should run all validators, emit a machine-readable report, and summarize hard fails, warnings, human-review-required items, and informational findings.
