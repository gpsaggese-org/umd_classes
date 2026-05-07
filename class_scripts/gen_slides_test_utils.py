"""
Shared utilities for slide generation testing.

Import as:

import class_scripts.gen_slides_test_utils as csgentuit
"""

import logging
import os
import re

import class_scripts.common_utils as csccouti
import helpers.hdbg as hdbg

_LOG = logging.getLogger(__name__)


def get_lesson_files(course_dir: str) -> list[str]:
    """
    Discover all lesson files in a course directory.

    :param course_dir: Course directory (data605 or msml610)
    :return: Sorted list of lesson file paths
    """
    lectures_source_dir = os.path.join(course_dir, "lectures_source")
    hdbg.dassert_dir_exists(lectures_source_dir)
    lesson_files = []
    for file in os.listdir(lectures_source_dir):
        if re.match(r"^Lesson\d+", file):
            file_path = os.path.join(lectures_source_dir, file)
            lesson_files.append(file_path)
    return sorted(lesson_files)


def get_lesson_numbers(course_dir: str) -> list[str]:
    """
    Get all lesson numbers in a course.

    :param course_dir: Course directory (data605 or msml610)
    :return: Sorted list of lesson numbers like ["01.1", "01.2", ...]
    """
    lectures_source_dir = os.path.join(course_dir, "lectures_source")
    hdbg.dassert_dir_exists(lectures_source_dir)
    lessons = []
    for file in os.listdir(lectures_source_dir):
        match = re.match(r"Lesson(\d+(?:\.\d+)?)", file)
        if match:
            lesson_num = match.group(1)
            lessons.append(lesson_num)
    return sorted(set(lessons))


def collect_all_lessons() -> dict[str, list[str]]:
    """
    Collect all lessons organized by course.

    :return: Dict with course dirs as keys and lesson lists as values
    """
    all_lessons = {}
    for course_dir in csccouti.VALID_DIRS:
        all_lessons[course_dir] = get_lesson_numbers(course_dir)
    return all_lessons
