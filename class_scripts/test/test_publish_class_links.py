"""
Unit tests for publish_class_links.py.

Import as:

import class_scripts.test.test_publish_class_links as csttpucli
"""

import os
from typing import Dict, List
from unittest import mock

import helpers.hio as hio
import helpers.hunit_test as hunitest

import class_scripts.publish_class_links as cspucli

_ALL_LABELS = [
    "Slides (PDF)",
    "Commentary (HTML)",
    "Commentary (PDF)",
    "Recap",
]


def _create_lesson_source_files(class_dir: str, lesson_names: List[str]) -> None:
    """
    Create empty lecture source files for the given lesson names.

    :param class_dir: course/book directory (e.g., `.../data605`)
    :param lesson_names: lesson names to create source files for
    """
    for lesson_name in lesson_names:
        file_path = os.path.join(
            class_dir, "lectures_source", f"{lesson_name}.txt"
        )
        hio.to_file(file_path, f"Content of {lesson_name}")


def _create_lesson_artifacts(
    class_dir: str, lesson_name: str, labels: List[str]
) -> None:
    """
    Create the artifact files for a lesson for the given artifact labels.

    :param class_dir: course/book directory
    :param lesson_name: lesson name (e.g., `Lesson01.1-Intro`)
    :param labels: subset of `_ALL_LABELS` to create files for
    """
    artifact_paths = {
        "Slides (PDF)": os.path.join(
            class_dir, "lectures_pdf", f"{lesson_name}.pdf"
        ),
        "Commentary (HTML)": os.path.join(
            class_dir,
            "lectures_commentary",
            f"{lesson_name}.book_chapter.html",
        ),
        "Commentary (PDF)": os.path.join(
            class_dir,
            "lectures_commentary",
            f"{lesson_name}.book_chapter.pdf",
        ),
        "Recap": os.path.join(
            class_dir, "lectures_recap", f"{lesson_name}.recap.md"
        ),
    }
    for label in labels:
        hio.to_file(artifact_paths[label], f"Content for {label}")


def _mock_github_url(*, file_path: str, use_master: bool) -> str:
    """
    Stand in for `to_github._get_github_url()` with a deterministic URL.

    :param file_path: path to the file, echoed back in the URL
    :param use_master: unused, kept to match the mocked signature
    :return: fake GitHub URL derived from `file_path`
    """
    return f"https://github.com/example/repo/blob/main/{file_path}"


# #############################################################################
# Test_parse
# #############################################################################


class Test_parse(hunitest.TestCase):
    """
    Test `_parse()` function.
    """

    def test1(self) -> None:
        """
        Test parser accepts the required arguments with `do_not_fail_on_warnings`
        defaulting to `False`.
        """
        # Prepare inputs.
        arg_list = ["--dir", "data605", "--out_file", "data605/links.html"]
        # Run test.
        parser = cspucli._parse()
        args = parser.parse_args(arg_list)
        # Check outputs.
        self.assertEqual(args.dir, "data605")
        self.assertEqual(args.out_file, "data605/links.html")
        self.assertFalse(args.do_not_fail_on_warnings)
        self.assertFalse(args.use_master)

    def test2(self) -> None:
        """
        Test parser sets `do_not_fail_on_warnings` to `True` when the flag is
        passed.
        """
        # Prepare inputs.
        arg_list = [
            "--dir",
            "data605",
            "--out_file",
            "data605/links.html",
            "--do_not_fail_on_warnings",
        ]
        # Run test.
        parser = cspucli._parse()
        args = parser.parse_args(arg_list)
        # Check outputs.
        self.assertTrue(args.do_not_fail_on_warnings)

    def test3(self) -> None:
        """
        Test parser sets `use_master` to `True` when the flag is passed.
        """
        # Prepare inputs.
        arg_list = [
            "--dir",
            "data605",
            "--out_file",
            "data605/links.html",
            "--use_master",
        ]
        # Run test.
        parser = cspucli._parse()
        args = parser.parse_args(arg_list)
        # Check outputs.
        self.assertTrue(args.use_master)


# #############################################################################
# Test_find_lesson_names
# #############################################################################


class Test_find_lesson_names(hunitest.TestCase):
    """
    Test `publish_class_links._find_lesson_names()` function.
    """

    def test1(self) -> None:
        """
        Test finding lesson names from multiple lecture source files, sorted
        by lesson number.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        lesson_names = [
            "Lesson02.1-Git",
            "Lesson01.2-Big_Data",
            "Lesson01.1-Intro",
        ]
        _create_lesson_source_files(class_dir, lesson_names)
        # Prepare outputs.
        expected = [
            "Lesson01.1-Intro",
            "Lesson01.2-Big_Data",
            "Lesson02.1-Git",
        ]
        # Run test.
        actual = cspucli._find_lesson_names(class_dir)
        # Check outputs.
        self.assertEqual(actual, expected)

    def test2(self) -> None:
        """
        Test that a missing `lectures_source` directory raises
        `AssertionError`.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        # Run test and check output.
        with self.assertRaises(AssertionError):
            cspucli._find_lesson_names(class_dir)

    def test3(self) -> None:
        """
        Test that an empty `lectures_source` directory raises
        `AssertionError`.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        os.makedirs(os.path.join(class_dir, "lectures_source"), exist_ok=True)
        # Run test and check output.
        with self.assertRaises(AssertionError):
            cspucli._find_lesson_names(class_dir)


# #############################################################################
# Test_get_lesson_artifacts
# #############################################################################


class Test_get_lesson_artifacts(hunitest.TestCase):
    """
    Test `publish_class_links._get_lesson_artifacts()` function.
    """

    def helper(
        self,
        class_dir: str,
        lesson_name: str,
        do_not_fail_on_warnings: bool,
        expected_exists: Dict[str, bool],
    ) -> None:
        """
        Helper for `_get_lesson_artifacts()`.

        :param class_dir: course/book directory
        :param lesson_name: lesson name
        :param do_not_fail_on_warnings: passed through to the function under
            test
        :param expected_exists: expected map from artifact label to whether
            it exists
        """
        # Run test.
        actual = cspucli._get_lesson_artifacts(
            class_dir,
            lesson_name,
            do_not_fail_on_warnings=do_not_fail_on_warnings,
        )
        # Check outputs.
        actual_exists = {artifact.label: artifact.exists for artifact in actual}
        self.assertEqual(actual_exists, expected_exists)

    def test1(self) -> None:
        """
        Test that a lesson with all artifacts present returns `exists=True`
        for each.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        lesson_name = "Lesson01.1-Intro"
        _create_lesson_artifacts(class_dir, lesson_name, _ALL_LABELS)
        do_not_fail_on_warnings = False
        # Prepare outputs.
        expected_exists = {label: True for label in _ALL_LABELS}
        # Run test.
        self.helper(
            class_dir, lesson_name, do_not_fail_on_warnings, expected_exists
        )

    def test2(self) -> None:
        """
        Test that missing artifacts with `do_not_fail_on_warnings=True`
        return `exists=False` for the missing ones instead of raising.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        lesson_name = "Lesson01.1-Intro"
        _create_lesson_artifacts(
            class_dir, lesson_name, ["Slides (PDF)", "Recap"]
        )
        do_not_fail_on_warnings = True
        # Prepare outputs.
        expected_exists = {
            "Slides (PDF)": True,
            "Commentary (HTML)": False,
            "Commentary (PDF)": False,
            "Recap": True,
        }
        # Run test.
        self.helper(
            class_dir, lesson_name, do_not_fail_on_warnings, expected_exists
        )

    def test3(self) -> None:
        """
        Test that a missing artifact with `do_not_fail_on_warnings=False`
        raises `AssertionError`.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        lesson_name = "Lesson01.1-Intro"
        # Prepare outputs.
        expected = "Missing 'Slides (PDF)' for lesson 'Lesson01.1-Intro'"
        # Run test.
        with self.assertRaises(AssertionError) as cm:
            cspucli._get_lesson_artifacts(
                class_dir, lesson_name, do_not_fail_on_warnings=False
            )
        # Check outputs.
        self.assertIn(expected, str(cm.exception))


# #############################################################################
# Test_generate_html_page
# #############################################################################


class Test_generate_html_page(hunitest.TestCase):
    """
    Test `publish_class_links._generate_html_page()` function.
    """

    def test1(self) -> None:
        """
        Test that an existing artifact is rendered as a link to its GitHub
        URL, using the current branch by default.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        pdf_path = os.path.join(
            class_dir, "lectures_pdf", "Lesson01.1-Intro.pdf"
        )
        artifact = cspucli.LessonArtifact("Slides (PDF)", pdf_path, True)
        lessons = [cspucli.LessonPage("Lesson01.1-Intro", [artifact])]
        # Prepare outputs.
        github_url = _mock_github_url(file_path=pdf_path, use_master=False)
        expected = f'<a href="{github_url}">Slides (PDF)</a>'
        # Run test.
        with mock.patch(
            "class_scripts.publish_class_links.dshgtogi._get_github_url",
            side_effect=_mock_github_url,
        ) as mock_get_url:
            actual = cspucli._generate_html_page(
                class_dir, lessons, use_master=False
            )
        # Check outputs.
        self.assertIn(expected, actual)
        mock_get_url.assert_called_once_with(
            file_path=pdf_path, use_master=False
        )

    def test2(self) -> None:
        """
        Test that `use_master=True` is passed through to
        `to_github._get_github_url()`.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        pdf_path = os.path.join(
            class_dir, "lectures_pdf", "Lesson01.1-Intro.pdf"
        )
        artifact = cspucli.LessonArtifact("Slides (PDF)", pdf_path, True)
        lessons = [cspucli.LessonPage("Lesson01.1-Intro", [artifact])]
        # Run test.
        with mock.patch(
            "class_scripts.publish_class_links.dshgtogi._get_github_url",
            side_effect=_mock_github_url,
        ) as mock_get_url:
            cspucli._generate_html_page(class_dir, lessons, use_master=True)
        # Check outputs.
        mock_get_url.assert_called_once_with(
            file_path=pdf_path, use_master=True
        )

    def test3(self) -> None:
        """
        Test that a missing artifact is rendered without a link.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        pdf_path = os.path.join(
            class_dir, "lectures_pdf", "Lesson01.1-Intro.pdf"
        )
        artifact = cspucli.LessonArtifact("Slides (PDF)", pdf_path, False)
        lessons = [cspucli.LessonPage("Lesson01.1-Intro", [artifact])]
        # Prepare outputs.
        expected = '<td class="missing">Slides (PDF)</td>'
        # Run test.
        actual = cspucli._generate_html_page(
            class_dir, lessons, use_master=False
        )
        # Check outputs.
        self.assertIn(expected, actual)
        self.assertNotIn("<a href=", actual)

    def test4(self) -> None:
        """
        Test that the page title uses the course/book directory name.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        lessons: List[cspucli.LessonPage] = []
        # Prepare outputs.
        expected = "<title>data605 - Class Links</title>"
        # Run test.
        actual = cspucli._generate_html_page(
            class_dir, lessons, use_master=False
        )
        # Check outputs.
        self.assertIn(expected, actual)


# #############################################################################
# Test_main
# #############################################################################


class Test_main(hunitest.TestCase):
    """
    End-to-end tests for the `publish_class_links.py` executable.
    """

    def _run_main(self, argv: List[str]) -> None:
        """
        Run `publish_class_links._main()` with a mocked `sys.argv`.

        :param argv: command-line argument list to inject via
            `mock.patch("sys.argv", ...)`
        """
        parser = cspucli._parse()
        with mock.patch("sys.argv", argv):
            cspucli._main(parser)

    def test1(self) -> None:
        """
        Test that the script writes an HTML page with a GitHub-URL link per
        lesson artifact when all artifacts exist.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        lesson_name = "Lesson01.1-Intro"
        _create_lesson_source_files(class_dir, [lesson_name])
        _create_lesson_artifacts(class_dir, lesson_name, _ALL_LABELS)
        pdf_path = os.path.join(class_dir, "lectures_pdf", f"{lesson_name}.pdf")
        recap_path = os.path.join(
            class_dir, "lectures_recap", f"{lesson_name}.recap.md"
        )
        out_file = os.path.join(class_dir, "class_links.html")
        argv = [
            "publish_class_links.py",
            "--dir",
            class_dir,
            "--out_file",
            out_file,
        ]
        # Prepare outputs.
        expected_pdf_url = _mock_github_url(file_path=pdf_path, use_master=False)
        expected_recap_url = _mock_github_url(
            file_path=recap_path, use_master=False
        )
        # Run test.
        with mock.patch(
            "class_scripts.publish_class_links.dshgtogi._get_github_url",
            side_effect=_mock_github_url,
        ):
            self._run_main(argv)
        # Check outputs.
        actual = hio.from_file(out_file)
        self.assertIn(f'href="{expected_pdf_url}"', actual)
        self.assertIn(f'href="{expected_recap_url}"', actual)

    def test2(self) -> None:
        """
        Test that a missing artifact stops the script with `AssertionError`
        and no output file is written (default fail-fast behavior).
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        lesson_name = "Lesson01.1-Intro"
        _create_lesson_source_files(class_dir, [lesson_name])
        out_file = os.path.join(class_dir, "class_links.html")
        argv = [
            "publish_class_links.py",
            "--dir",
            class_dir,
            "--out_file",
            out_file,
        ]
        # Run test and check output.
        with self.assertRaises(AssertionError):
            self._run_main(argv)
        self.assertFalse(os.path.exists(out_file))

    def test3(self) -> None:
        """
        Test that `--do_not_fail_on_warnings` writes the page even when
        artifacts are missing, marking those lessons without a link.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        lesson_name = "Lesson01.1-Intro"
        _create_lesson_source_files(class_dir, [lesson_name])
        out_file = os.path.join(class_dir, "class_links.html")
        argv = [
            "publish_class_links.py",
            "--dir",
            class_dir,
            "--out_file",
            out_file,
            "--do_not_fail_on_warnings",
        ]
        # Run test.
        self._run_main(argv)
        # Check outputs.
        actual = hio.from_file(out_file)
        self.assertIn('<td class="missing">Slides (PDF)</td>', actual)

    def test4(self) -> None:
        """
        Test that `--use_master` is passed through to
        `to_github._get_github_url()`.
        """
        # Prepare inputs.
        class_dir = os.path.join(self.get_scratch_space(), "data605")
        lesson_name = "Lesson01.1-Intro"
        _create_lesson_source_files(class_dir, [lesson_name])
        _create_lesson_artifacts(class_dir, lesson_name, _ALL_LABELS)
        out_file = os.path.join(class_dir, "class_links.html")
        argv = [
            "publish_class_links.py",
            "--dir",
            class_dir,
            "--out_file",
            out_file,
            "--use_master",
        ]
        # Run test.
        with mock.patch(
            "class_scripts.publish_class_links.dshgtogi._get_github_url",
            side_effect=_mock_github_url,
        ) as mock_get_url:
            self._run_main(argv)
        # Check outputs.
        for call in mock_get_url.call_args_list:
            self.assertTrue(call.kwargs["use_master"])
