In lint_text.py for smd files there should be a rule that adds an empty line
between blocks of level 1 (keeping together without empty spaces all the
nested bullets at level > 1)

For instance this

```
- @Motivation@: many independent parties want to share one evolving record (e.g.,
  who owns what, what happened, in what order) with no central party controlling
  it
- @Problem@: _without a trusted intermediary_, how do _mutually distrusting nodes
  agree_ on a single, consistent history?
  - Nodes can be slow, offline, or actively malicious
  - Network messages can be delayed, dropped, or reordered
- @Key idea@: **consensus** is the mechanism that lets independent nodes converge
  on the same ledger despite these failures
- @Example@:
  - A bank's database is the single source of truth for account balances
  - A blockchain replaces the single database with thousands of independently
    operated copies that must all agree
```

becomes

```
- @Motivation@: many independent parties want to share one evolving record (e.g.,
  who owns what, what happened, in what order) with no central party controlling
  it

- @Problem@: _without a trusted intermediary_, how do _mutually distrusting nodes
  agree_ on a single, consistent history?
  - Nodes can be slow, offline, or actively malicious
  - Network messages can be delayed, dropped, or reordered

- @Key idea@: **consensus** is the mechanism that lets independent nodes converge
  on the same ledger despite these failures

- @Example@:
  - A bank's database is the single source of truth for account balances
  - A blockchain replaces the single database with thousands of independently
    operated copies that must all agree
```

Check if some transformation exists in lint_text.py for other types and propose
a plan

## Findings

- No action in `lib_lint_text.py` currently *adds* a blank line between
  level-1 bullets, for any format (`md`, `tex`, `txt`, `smd`).
- The opposite direction already exists and applies to all 4 formats:
  `_postprocess_txt()` (action `postprocess`) has a regex
  (`^\s*\n(\s+-\s+.*)$`) that *removes* a blank line sitting right before an
  indented (level > 1) bullet. That already keeps nested bullets glued
  together with no blank lines, so nothing to change there.
- Prior art for the exact rule requested exists:
  `helpers/hmarkdown_formatting.py::format_first_level_bullets()` strips all
  blank lines then re-inserts one before every level-1 bullet. Docstring says
  "This is the formatting we use in the slides" (there's even a
  `TODO(gp): -> format_first_level_bullets_in_slide`), so it was built for
  exactly this smd use case, just never wired into `lint_text.py`. It's
  currently only used by `format_markdown_slide()` in
  `dev_scripts_helpers/llms/llm_utils.py`, a separate pipeline.

## Revised approach (per discussion)

Rather than a targeted insert-only function, adopt the "strip everything,
then re-derive every blank line the format needs" strategy — same idea
`_format_smd_fence_spacing()` already uses (drop blanks bordering a fence,
then reinsert exactly one). This avoids reconciling separate add/remove
regexes that can drift out of sync.

Wrinkle found: by the time `_smd_format()` runs, `add_blank_lines_between_headers`
has already run once (it's an earlier, separate action in the pipeline) and
put a blank line between consecutive `#`/`##` headers. If `_smd_format()`
strips *all* blank lines and only re-adds around bullets + fences, that
header spacing is lost. So the strip-and-rebuild must also redo the header
rule, not just bullets and fences.

- [x] In `_smd_format()`, after the existing per-line loop (tag-colon
      removal, capitalization), replace the single
      `_format_smd_fence_spacing()` call with:
  - [x] Strip all blank lines: `[l for l in lines_new if l.strip()]`
  - [x] `hmarform.format_first_level_bullets(lines_new)` — adds blank before
        every level-1 bullet except the first in a run (new import:
        `helpers.hmarkdown_formatting as hmarform`, already imported)
  - [x] `_format_smd_fence_spacing(lines_new)` — only touches blanks
        bordering `:::` fence lines, so it can't undo the bullet blanks just
        added, and fixes spacing where a fence sits next to a bullet with no
        blank yet
  - [x] `_add_blank_lines_between_headers(lines_new)` — last. It only inserts
        when the *next* line is directly a header (adjacent, no blank
        between), so it's unaffected by whatever bullets/fences did earlier —
        order relative to them doesn't change the result, this is just the
        more readable order (format the body, then fix up section breaks)
- [x] Known residual risk: any blank line the author placed for a reason
      other than headers/bullets/fences (e.g. between two plain prose lines,
      or around a `$$...$$` math block) is stripped and not restored, since
      no rule re-adds it. Sample real files (`tmp.smd`,
      `Lesson01.1_Blockchain_Consensus_Foundations.txt`) look bullet/header/
      fence-driven, so risk looks low — confirm by diffing before/after on
      those two files as part of verification, not just unit tests
- [x] Second edge case found (theoretical, not present in the two sample
      files — checked, 0 hits): `format_first_level_bullets()` inserts a
      blank before *every* level-1 bullet except the first line of the whole
      file, with no header-awareness. If a header were ever directly followed
      by a `- ` bullet (no `* <slide title>` marker in between), this would
      reintroduce a blank line there, undoing the earlier `handle_empty_lines`
      action's "no blank right after a header" rule. Not fixing pre-emptively
      since it doesn't occur in practice; the before/after diff would catch it
      if it ever does
- [x] Update `_smd_format()` docstring + `VALID_ACTIONS["smd_format"]`
      comment to describe the strip-and-rebuild behavior
- [x] Tests in `dev_scripts_helpers/documentation/test/test_lint_text.py`,
      extending `Test_smd_format`:
  - [x] The exact example from the instructions (level-1 bullets, some with
        nested children, get exactly one blank line between blocks; nested
        bullets stay glued)
  - [x] Headers still get separated (regression check for the wrinkle above)
  - [x] Fence spacing still correct when a fence immediately follows a header
        or a bullet block (no blank in the input)
  - [x] Idempotency: running `_smd_format` twice gives the same output
- [x] Run
      `pytest dev_scripts_helpers/documentation/test/test_lint_text.py -k smd`
      plus a manual diff of `lint_text.py` output on `tmp.smd` /
      `Lesson01.1_Blockchain_Consensus_Foundations.txt` for the residual-risk
      check above
- [ ] Not in scope unless requested: generalizing to `md`/`tex`/`txt`, or
      adding a blank-line rule around `* <slide title>` markers (no existing
      rule does that today either; separate ask if wanted) — **see Result
      below: this turned out to matter more than expected on real content**

## Result

- Done:
  - `_smd_format()` in `dev_scripts_helpers/documentation/lib_lint_text.py`
    now strips all blank lines and re-derives them: one blank line before
    every level-1 bullet (`hmarform.format_first_level_bullets()`), fence
    spacing (`_format_smd_fence_spacing()`), then header spacing
    (`_add_blank_lines_between_headers()`). Docstring and the
    `VALID_ACTIONS["smd_format"]` comment updated to match.
  - Added `Test_smd_format.test14` (the exact instructions example),
    `test15` (header-separation regression), `test16` (fence next to a
    header with no blank in the input), `test17` (idempotency); updated
    `test1` and `test13`, whose expected output changed because they contain
    level-1 bullets that now correctly get a blank line inserted.
  - `pytest dev_scripts_helpers/documentation/test/test_lint_text.py -k
    "Test_smd_format or Test_perform_actions_smd_type or
    Test_add_blank_lines_between_headers"` → 27 passed.
  - Full file: `pytest dev_scripts_helpers/documentation/test/test_lint_text.py`
    → 7 pre-existing failures (verified via `git stash`: same 7 fail on
    unmodified code, unrelated `actions=None` typing issue in
    `_filter_actions_by_format`, not touched by this change), 120 passed.
  - Ran the real strip-and-rebuild logic (via `_perform_actions` with
    `actions=["preprocess", "postprocess", "smd_format"]`, so comments are
    protected and `*` slide titles are restored before `smd_format` sees
    them, matching the real pipeline) on `tmp.smd` and
    `Lesson01.1_Blockchain_Consensus_Foundations.txt` and diffed the output.
- **Finding from the real-file diff — flagging before going further**: the
  bullet spacing itself is correct (one blank line added between every
  level-1 bullet block in both files, nested bullets stay glued, matches the
  instructions example exactly). But the strip-and-rebuild also *removes*
  blank lines that had nothing to do with bullets/headers/fences, and
  nothing re-adds them, because no rule in the pipeline owns that spacing:
  - A blank line right before/after a `* <slide title>` marker (used
    throughout both real files — this is not the rare theoretical case,
    it's the dominant "other" blank-line convention in this format) is
    always dropped.
  - A blank line between the end of a `//` comment block and the following
    `#`/`##` header or `*` slide title is dropped too (only
    header-immediately-after-header gets restored).
  - Net effect on `tmp.smd`: 51 blank lines added (bullets — wanted), but
    also 38 blank lines removed (mostly around `*` slide titles — not
    asked for). Same pattern on the other file (45 added / 55 removed).
- Not done: did not add a blank-line rule for `* <slide title>` markers, or
  for comment-to-header/comment-to-title transitions, since that's new scope
  beyond "blank line between level-1 bullet blocks." The code as implemented
  is correct for what was asked; it's the side effect on unrelated spacing
  that needs a decision.

**Options, need a decision before running this on the real lecture files**:
1. Extend the rebuild to also keep exactly one blank line around `*
   <slide title>` markers (and before a header/title that follows a comment
   block) — closes the gap, still smd-only, small addition to the same
   function.
2. Accept it as full normalization (a strict linter arguably should own all
   blank-line placement in this format, not just bullets) and let it reflow
   those files too.
3. Go back to the original targeted, insert-only design (blank line before
   a level-1 bullet only when the previous line is bullet content) instead
   of strip-and-rebuild — zero effect on slide titles/comments/headers, at
   the cost of the separate add/remove regexes not being unified.

Waiting for direction on the options above before running this on the real
lecture files.

## Result 2: header → slide-title spacing

- Done:
  - Checked for overlap first: none. `_add_blank_lines_between_headers()`
    only matches header/header pairs (`* <title>` doesn't match its header
    regex), and the only other place that even recognizes `* <title>` as a
    slide-title marker (vs. a bullet) is `_convert_asterisk_bullets_to_dashes()`,
    which is about conversion, not spacing.
  - Added `_is_smd_slide_title_line()` and
    `_add_blank_line_before_slide_title()` to
    `dev_scripts_helpers/documentation/lib_lint_text.py`, mirroring
    `_add_blank_lines_between_headers()`: inserts a blank line when a header
    is immediately followed by a `* <title>` marker. Wired into
    `_smd_format()` right after the header-spacing step (order doesn't
    matter — the two conditions don't overlap). Docstring +
    `VALID_ACTIONS["smd_format"]` comment updated.
  - Added `Test_smd_format.test18` (header + blank already above it, no
    blank before the title — your first example) and `test19` (no blanks
    anywhere — your second example); both assert the exact expected output
    you gave.
  - `pytest -k "Test_smd_format or Test_perform_actions_smd_type or
    Test_add_blank_lines_between_headers"` → 29 passed.
- Not done / still open: this only covers header → slide-title. The other
  gap from Result 1 — blank line lost between the *end of a bullet block*
  and the *next* slide title (e.g. `- @Example@\n  - ...\n* New Slide`), and
  between a slide title and a following `//` comment — is still there,
  since neither of those transitions was asked for here. Say the word if you
  want those covered too.

## Result 3: exactly one blank line before/after every header and slide title

- Superseded `_add_blank_line_before_slide_title()` (Result 2) with a
  general, symmetric rule, since this request subsumes it: `_smd_format()`
  no longer special-cases "header → title" and "header → header"
  separately. New helpers `_is_smd_header_or_title_line()` and
  `_format_smd_header_and_title_spacing()` (mirrors
  `_format_smd_fence_spacing()`'s drop-then-reinsert design) ensure exactly
  one blank line before and after *every* header and *every* slide-title
  marker, on both sides, regardless of what's adjacent (plain text, a
  comment, another header, a title, or a fence). This closes the gap flagged
  as "not done" right above: a slide title is now separated from whatever
  came before it (bullet-block end, comment, ...) and whatever comes after
  it, not just from a preceding header.
  - Kept `_add_blank_lines_between_headers()` as-is (still used standalone
    for `md` files via the `add_blank_lines_between_headers` action).
    Removed `_add_blank_line_before_slide_title()` (superseded, no longer
    called from anywhere).
- Updated `_smd_format()` docstring + `VALID_ACTIONS["smd_format"]` comment.
- Updated `test15` (now also expects a blank *after* `## Subtitle`, before
  the following prose) since it previously only checked the narrower
  "between headers" rule. Added `test20` (blank before/after a header and a
  slide title when neither is adjacent to another header/title — preceded
  by plain text, followed by bullet content) and `test21` (idempotency with
  headers, subtitles, and slide titles all mixed together).
- `pytest -k "Test_smd_format or Test_perform_actions_smd_type or
  Test_add_blank_lines_between_headers"` → 31 passed. Full file → same 7
  pre-existing, unrelated failures as before, 124 passed (up from 120).
