# Golden Fixtures

Fixtures provide known-good and known-bad cases for Codex implementation.

Each fixture should eventually contain:
- source input or source description
- expected semantic JSON
- expected layout intent
- expected authoring HTML snapshot or structural assertions
- expected production HTML snapshot or structural assertions
- expected validation report

Required fixture groups:
- bidding MSC
- play problem
- defense problem
- historical full deal
- split problem/solution source bundle
- source inconsistency: problem/solution hand mismatch
- source inconsistency: impossible auction
- source inconsistency: duplicate card/full deal error
- auction edge cases: passed out, double/redouble, incomplete auction, dealer offset
