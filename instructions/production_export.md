# Production Export Rules

Production export transforms authoring HTML into MailerLite-ready production HTML.

Production export must not change article semantics or intentional rendering.

## Production pipeline

Apply production transformations in this order:

1. Start from validated authoring HTML.
2. Replace any legacy MailerLite suit/logo URLs with the short asset URLs from `manifest.md`.
3. Strip nonessential comments:
   - generation instructions
   - authoring notes
   - editable-region markers
   - section labels
   - preserve MSO conditional comments and non-MSO conditional wrappers
4. Deduplicate CSS while preserving platform scopes:
   - base CSS
   - mobile media CSS
   - MSO conditional CSS
5. Minify:
   - remove indentation and line breaks between tags
   - collapse repeated whitespace outside visible text
   - remove `type="text/css"` from style tags
6. Shorten safe literals:
   - `#ffffff` -> `#fff`
   - `#333333` -> `#333`
   - `#222222` -> `#222`
   - `#444444` -> `#444`
   - `#555555` -> `#555`
   - safe zero units: `0px`/`0pt` -> `0`
7. Remove redundant attributes:
   - nested `role="presentation"` unless required by policy
   - `border="0"` when inline `border:0` remains
   - empty `style` and `class` attributes
8. Apply validated class compression:
   - hand typography/alignment
   - suit image rendering
   - non-Outlook auction typography/alignment
   - paragraph/body text
9. Restore Outlook-critical inline/conditional protection:
   - newsletter identity
   - hand labels
   - MSO auction fonts/bold/row heights
   - Stay Connected fonts
   - footer fonts if needed
10. Run production validation.

## Optimization tiers

### Tier 1: normal safe export

Allowed without special permission:
- strip non-MSO comments
- minify whitespace
- shorten safe hex colors
- replace legacy asset URLs
- remove redundant `role="presentation"`
- remove redundant `border="0"` when `border:0` remains
- class-compress validated non-Outlook and hand typography styles
- remove inherited text colors when parents preserve intended color

### Tier 2: requires Outlook/Gmail regression testing

Allowed only with render testing:
- more aggressive body/paragraph class compression
- selective MSO auction compression while preserving table structure, row heights, fonts, bold headers, spans, and suit alignment
- selective background reduction
- class-compression of non-Outlook auction cells

### Tier 3: high-risk structural changes

Do not use unless explicitly requested and treated as a test build:
- remove whole MSO auction tables
- unwrap non-MSO auction tables for Outlook
- merge Outlook and non-Outlook auction rendering
- remove Outlook hand-stage spacer tables
- remove MSO row-height/span wrappers
- broad background stripping


## Approved production compression classes

The production exporter may use only validated compact classes listed here unless a new class is explicitly added to this section and regression-tested.

### Hand diagram classes

- `.hfont` = `font-family:'Times New Roman',Times,serif`
- `.hlabel` = `font-family:'Times New Roman',Times,serif;font-weight:bold;font-size:17px;line-height:20px;padding:0 0 3px`
- `.hcard` = `font-size:17px`
- `.hnowrap` = `white-space:nowrap`

Rules:
- Keep Outlook-sensitive hand label cells protected with inline `font-family` and `font-weight:bold` or an MSO-equivalent.
- Keep hand layout widths, heights, padding, `mso-line-height-rule`, and spacer cells inline when they affect Outlook.

### Suit image classes

- `.si` = `display:inline-block;width:11px;height:13px;border:0;vertical-align:-1px;mso-line-height-rule:exactly`
- `.sit` = `display:block;width:11px;height:13px;border:0;outline:none;text-decoration:none`

Rules:
- Suit images must retain `src`, `alt`, `width`, and `height` attributes.
- Do not remove suit alignment unless the class is present and tested.

### Auction classes

- `.af` = `font-family:'Times New Roman',Times,serif`
- `.ah` = `font-weight:bold;text-align:left;white-space:nowrap`
- `.ac` = `text-align:left;vertical-align:middle`

Rules:
- Use auction classes primarily in non-Outlook auction markup.
- MSO auction markup must keep inline fonts, bold headers, row heights, line heights, `mso-*` properties, and span wrappers.

### Body text classes

- `.bt` or `.tx` = `font-family:'Times New Roman',Times,serif;font-size:17px;line-height:27px`
- `.pm` or `.p15` = `margin:0 0 15px`
- `.p20` = `margin:0 0 20px`
- `.it` = `font-style:italic`

Rules:
- Do not rely only on body text classes for Outlook-sensitive sections.
- Newsletter identity and Stay Connected require inline or MSO-conditional font protection.

## Outlook-critical inline properties

Do not class-compress these away in Outlook-sensitive regions:

- `font-family`
- `font-weight` where bold is visually required
- `height`
- `line-height`
- `mso-line-height-rule`
- `mso-height-rule`
- `vertical-align`
- `padding`
- `mso-padding-alt`
- MSO spacer heights
- suit image dimensions and vertical alignment

## Size budget

Because MailerLite injects tracking/wrapper HTML, production source HTML should target 75 KB when possible.

Assume MailerLite may append approximately 25 KB of tracking/wrapper HTML after upload. Production reports must estimate delivered size as:

`production_source_size + 25 KB`

Report tradeoffs if:
- production HTML exceeds 75 KB
- safe optimizations cannot reach target
- Tier 2 or Tier 3 optimizations would be required

Hard fail only if the user has set a strict maximum size.

## Authoring vs production invariant

Never upload authoring HTML directly to MailerLite. Production export must remove generation-only comments and authoring markers.

## Production size gates

Production export must report the final source size.

Targets:

- Ideal target: `<= 75 KB`
- Warning: `> 75 KB`
- Human review required: `> 85 KB`
- Hard fail: `> 95 KB` unless the user explicitly approves export
- Informational: estimate MailerLite injection risk because tracking/wrapper HTML may add significant size

Production output must not contain:

- generation-only comments
- editable-region markers
- legacy MailerLite-generated suit/logo URLs
- empty `style=""`
- empty `class=""`
- orphaned or malformed MSO conditional comments

## Protected optimization rule

Production export may optimize only within the safe optimization tiers.

Never optimize protected rendering regions in a way that removes Outlook-critical inline/conditional properties listed in `rendering_rules.md`.

Do not remove whole Outlook/MSO auction tables or Outlook/MSO spacer structures.

Do not unwrap non-MSO auction tables for Outlook unless the user explicitly authorizes a high-risk Tier 3 experiment and Outlook desktop regression testing is performed afterward.

## Concision reporting

Each production export report must include:

- starting authoring size
- production size
- estimated MailerLite injection size
- estimated delivered size
- savings by category when measurable
- asset URL status
- whether size target, warning, or hard-fail threshold was reached
- required regression tests based on optimization tier

## Determinism and idempotence

Production export must be deterministic and idempotent.

Running production export twice on the same authoring HTML must produce byte-identical production HTML.

Production export must not:
- infer semantic meaning
- alter canonical JSON
- alter visible article wording
- reorder email sections
- restructure MSO blocks
- remove protected-region inline styles without an approved replacement

MSO blocks are renderer-owned structures. Production export may compress safe literals inside them, but may not remove, merge, unwrap, or restructure them.

## Safe optimization ownership

Optimization must respect layer ownership:

- extraction and semantic bridge rules decide content and meaning
- rendering rules decide visual structure
- production export only reduces delivery size

If a size optimization changes visible rendering, section order, source semantics, Outlook/MSO behavior, or mobile behavior, it is invalid unless explicitly authorized by the user and regression-tested.

## Template and export versioning

Templates and production export should carry version metadata in authoring comments or reports:
- authoring template version
- production template version
- asset map version
- production export rules version

Production output may strip comments, but the production report must preserve the version information.

## Implementation constraints

Production export and validators should be:
- deterministic
- idempotent
- reproducible
- side-effect-free except for declared output files
- rule-based where rules are sufficient
- conservative around Outlook/MSO and protected regions

Avoid ML-style heuristic rewriting in production export. Any heuristic extraction or OCR step must record confidence and source references.

## Accessibility-preserving minimization

Do not remove:
- meaningful `alt` text from logo images
- meaningful `alt` text from suit images unless an approved accessibility alternative exists
- MailerLite links/tokens
- visible link text
- semantic user-facing text

`role="presentation"` may be removed only from nested tables where accessibility policy and rendering tests allow it. It should not be stripped blindly if doing so would degrade screen-reader behavior.
