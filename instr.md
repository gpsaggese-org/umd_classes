# Increase test coverage for `class_scripts/`

## Context

`pytest class_scripts --cov=class_scripts` currently reports 39% total coverage.
Several modules sit at 0%: `common_utils.py` (27%, shared by many scripts),
`process_slides.py` (0%, invoked by three wrapper scripts), and a handful of
thin CLI wrappers (`count_lecture_pages.py`, `count_lecture_commentary_pages.py`,
`get_lecture_file.py`, `count_words.py`, `slide_check.py`, `slide_improve.py`,
`slide_reduce.py`). This plan targets exactly that set — it's the highest-ROI
slice: `common_utils.py` is a dependency of most of the wrappers, and
`process_slides.py` is the shared engine behind the three `slide_*.py` scripts,
so covering these two once pays off across every script that calls them.

Other 0%-covered modules (`create_book_toc_from_slides.py`,
`generate_book_chapter.py`, `gen_quizzes.py`, etc.) are out of scope for this
pass — they're larger and independent, better tackled separately.

## Conventions to follow (already established in `class_scripts/test/`)

- Base class `helpers.hunit_test.TestCase` (`hunitest`), one test file per
  source file: `class_scripts/test/test_<module>.py`.
- Import target module with a 7-letter mnemonic alias in the module docstring
  (`import class_scripts.count_words as clcowoor`), matching the alias already
  used in the source file's own docstring where one exists.
- One test class per tested function: `Test_parse`, `Test_main`, `Test__<private_fn>`.
  Test methods `test1`, `test2`, ... with a short docstring (Given/Expect).
- `_parse()` tests: call `_parse()` then `parser.parse_args([...])` (a literal
  list, never `sys.argv` patching), assert `getattr(args, key)`.
- Filesystem fixtures: `self.get_scratch_space()` + `hio.to_file(...)` /
  `os.makedirs(...)` to build fake `lectures_source/`, `lectures/`, `book/`,
  `lectures_video_script/` trees — no shared conftest exists, build inline like
  `test_for_loop_lessons.py` does (see its `_create_test_structure*` helpers).
- Mocking subprocess/shell calls: `helpers.hunit_test_utils.capture_system_calls()`
  (`hunteuti`) — context manager patching `subprocess.run`, `hsystem.system`,
  `hsystem.system_to_string` at once, returns a list of `{function, args, kwargs}`
  dicts; compare with `self.assert_equal(pprint.pformat(invocations), hprint.dedent(expected), purify_text=True)`.
  For a single specific return value (e.g. `mdls` output), use
  `mock.patch("helpers.hsystem.system_to_string")` directly instead.
- Mocking LLM calls: `helpers.hllm_cli.mock_apply_llm()` — context manager that
  patches `helpers.hllm_cli.apply_llm` to return a deterministic MD5 digest,
  no network/API key needed.

## 1. `class_scripts/common_utils.py` (`class_scripts/test/test_common_utils.py`)

| Function | Test approach |
|---|---|
| `validate_dir_lesson_args` | Pure — assert passes for non-empty args, raises (`hdbg` assertion error) for empty `dir_arg`/`lesson_arg` |
| `get_output_name` | Pure string logic — table of (source_name, extension) → expected output, including no-extension and multi-dot cases |
| `find_lecture_file` / `get_source_name` | Scratch dir with `lectures_source/LessonXX-Foo.txt`; assert found path/name; assert `dassert_eq` failure when 0 or 2+ matches |
| `ensure_dir_exists` | Scratch dir; test create-new, idempotent-exists, and `from_scratch=True` wipes prior content |
| `count_pdf_pages` | `mock.patch("helpers.hsystem.system_to_string")` returning `(0, "kMDItemNumberOfPages = 42")`; assert `42`; assert malformed output raises via `dassert_eq` on `parts` length |
| `get_pdf_page_counts` | Scratch dir with a couple of empty `Lesson01.pdf`/`Lesson02.pdf` placeholder files (`hio.to_file(path, "")`), mock `count_pdf_pages` (or `system_to_string`) to return distinct counts per call, assert the returned dict |

## 2. Four thin CLI wrappers

- `class_scripts/test/test_count_lecture_pages.py`
- `class_scripts/test/test_count_lecture_commentary_pages.py`
- `class_scripts/test/test_get_lecture_file.py`
- `class_scripts/test/test_count_words.py`

Each gets:
- `Test_parse`: assert positional args parsed correctly (`dir`, and `lesson` for `get_lecture_file`).
- `Test_main`: scratch dir with the right subdir (`lectures/`, `book/`,
  `lectures_source/`, `lectures_video_script/` respectively) and placeholder
  files; for the two PDF-page-count scripts, mock `common_utils.count_pdf_pages`
  (or `hsystem.system_to_string`) since real PDFs/`mdls` aren't available in CI;
  for `get_lecture_file.py` and `count_words.py`, real placeholder files are
  enough (no mocking needed — `count_words.py` doesn't touch `common_utils` at
  all, it reads real file content directly).
- Call `_main(_parse())`-equivalent by constructing args via
  `parser.parse_args([scratch_dir])` and monkeypatching only what's necessary
  (these scripts read `args.dir` as a plain string, so pass the scratch path
  directly as the positional arg — no `sys.argv` patching required).

## 3. Three `slide_*.py` wrappers

- `class_scripts/test/test_slide_check.py`
- `class_scripts/test/test_slide_improve.py`
- `class_scripts/test/test_slide_reduce.py`

Each gets:
- `Test_parse`: assert `dir`, `lesson`, `extra_opts` (default `[]` and populated) parsed correctly.
- `Test_main`: scratch dir with `lectures_source/LessonXX-Foo.txt`; wrap the
  call in `hunteuti.capture_system_calls()`; assert the single captured
  `hsystem.system` invocation's command string contains the expected
  `process_slides.py --in_file ... --action <text_check_fix|slide_improve|slide_reduce> --out_file ... --use_llm_transform`
  shape (purify the scratch path via `self.assert_equal(..., purify_text=True)`).
  Add a second test passing `extra_opts` and asserting they're appended.

## 4. `class_scripts/process_slides.py` (`class_scripts/test/test_process_slides.py`)

- `Test__extract_slides_from_markdown`: pure text logic — cases: no headers
  (whole text is one "slide" or empty list, per actual behavior), single
  header, multiple headers, last slide running to EOF.
- `Test__get_system_prompt_from_tag`: call with the three real tags used by
  the wrappers (`text_check_fix`, `slide_improve`, `slide_reduce`) from
  `dev_scripts_helpers.llms.llm_prompts`; assert a non-empty dedented string
  is returned; assert `hdbg.dassert_in` failure for an unknown tag.
- `Test__process_single_slide` / `Test__process_slides`: wrap with
  `hllmcli.mock_apply_llm()`; assert the `"* {slide_title}"` prefix logic
  (both already-prefixed and not-prefixed cases) and that `limit_range`
  filtering (via `hseinout.apply_limit_range`) restricts which slides are
  processed.
- `Test__process_slide_with_llm_transform`: mock `hgit.find_file_in_git_tree`
  and `hsystem.system` (via `capture_system_calls()`), pre-seed the expected
  tmp output file with `hio.to_file` before calling, assert the built command
  list and the returned content read back.
- `Test_parse`: assert `--in_file`, `--action`, `--out_file`,
  `--use_llm_transform`, `--no_abort_on_error` parse correctly.
- `Test_main`: end-to-end in a scratch dir — write a small multi-slide
  markdown `in_file`, wrap in `hllmcli.mock_apply_llm()`, call `_main(_parse())`
  equivalent via `parser.parse_args([...])`, read back `out_file` and assert
  its shape (slide count / prefixes), without hitting the network.

## Verification

1. `pytest class_scripts --cov=class_scripts` — confirm `common_utils.py` and
   `process_slides.py` move from 27%/0% to high coverage, and the seven wrapper
   scripts move from 0% to high coverage; confirm total % rises substantially
   from 39%.
2. `pytest class_scripts` (no cov) — confirm no regressions in the existing
   100%-covered test files.
3. Spot-check one or two new test files by hand (e.g. run
   `pytest class_scripts/test/test_process_slides.py -v`) to make sure mocks
   actually prevent real LLM/API calls (no `OPENAI_API_KEY`/network needed).

# Conventions
- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`

- When writing unit tests for follow the instructions in
  `.claude/skills/testing.rules.md`
