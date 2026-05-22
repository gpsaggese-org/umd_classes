#!/usr/bin/env python

"""
Create a project / tutorial to a specified destination directory.

# Create a project in a target directory
> create_project.py --dst_dir /path/to/destination
"""

import argparse
import logging
import os

import helpers.hdbg as hdbg
import helpers.hparser as hparser
import helpers.hprint as hprint
import helpers.hsystem as hsystem

_LOG = logging.getLogger(__name__)


# #############################################################################
# Helper functions
# #############################################################################


def _get_source_dir() -> str:
    """
    Get the absolute path to the source directory containing Docker files.

    :return: absolute path to class_project/project_template/
    """
    # Get the directory where this script is located.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dir_name = os.path.join(script_dir, "project_template")
    return dir_name


def _copy_files(
    src_dir: str,
    dst_dir: str,
    *,
    overwrite: bool = False,
) -> None:
    """
    Copy entire directory from source to destination.

    :param src_dir: source directory path
    :param dst_dir: destination directory path
    :param overwrite: whether to overwrite if destination already exists
    """
    # Verify source directory exists.
    hdbg.dassert_dir_exists(src_dir, "Source directory does not exist:", src_dir)
    # Check if destination directory already exists.
    if not overwrite:
        hdbg.dassert_path_not_exists(
            dst_dir,
            "Destination directory already existss (use --overwrite to replace)",
        )
    else:
        if os.path.exists(dst_dir):
            # Remove existing directory to allow fresh copy.
            _LOG.debug("Removing existing destination directory: '%s'", dst_dir)
            hsystem.system(f"rm -rf {dst_dir}")
    # Copy the entire directory using cp -a.
    _LOG.info("Copying directory from '%s' to '%s'", src_dir, dst_dir)
    cmd = f"cp -a {src_dir} {dst_dir}"
    hsystem.system(cmd)
    _LOG.info("Successfully copied directory to '%s'", dst_dir)


def _rename_template_files(project_name: str, dst_dir: str) -> None:
    """
    Rename template files to use project name.

    Renames files containing "template" prefix to use the project name
    (derived from destination directory name) instead.

    :param dst_dir: destination directory path
    """
    # Extract project name from destination directory.
    # Template files to rename.
    template_files = [
        "template_utils.py",
        "template.example.ipynb",
        "template.API.ipynb",
        "template.example.py",
        "template.API.py",
    ]
    for template_file in template_files:
        src_path = os.path.join(dst_dir, template_file)
        # Skip if template file doesn't exist.
        hdbg.dassert_file_exists(src_path)
        # Create new filename by replacing template with project name.
        new_filename = template_file.replace("template", project_name)
        dst_path = os.path.join(dst_dir, new_filename)
        _LOG.info("Renaming '%s' -> '%s'", template_file, new_filename)
        hsystem.system(f"mv {src_path} {dst_path}")
    _LOG.info("Successfully renamed template files")


def customize_files(project_name: str, dst_dir: str) -> None:
    """
    Customize files in the project directory.

    Updates docker_name.sh to use project-specific image name.

    :param project_name: project name
    :param dst_dir: destination directory path
    """
    docker_file = os.path.join(dst_dir, "docker_name.sh")
    if not os.path.exists(docker_file):
        _LOG.debug("docker_name.sh not found in '%s'", dst_dir)
        return
    # Read the file.
    with open(docker_file, "r") as f:
        content = f.read()
    # Replace IMAGE_NAME template with project-specific name.
    content = content.replace(
        "IMAGE_NAME=umd_project_template",
        f"IMAGE_NAME=umd_project_{project_name}",
    )
    # Write back the modified content.
    with open(docker_file, "w") as f:
        f.write(content)
    _LOG.info("Updated docker_name.sh with project name")


# #############################################################################


def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dst_dir",
        action="store",
        required=True,
        help="Destination directory where files will be copied",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite destination directory if it already exists",
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    project_name = os.path.basename(args.dst_dir)
    _LOG.info("Project name='%s'", project_name)
    # Get source directory.
    src_dir = _get_source_dir()
    # Copy files to destination.
    _copy_files(
        src_dir,
        args.dst_dir,
        overwrite=args.overwrite,
    )
    # Rename template files to use project name.
    _rename_template_files(project_name, args.dst_dir)
    # Customize project files.
    customize_files(project_name, args.dst_dir)
    #
    text = f"""
    Next steps:
    - Commit the changes
      ```
      > git add tutorials/{project_name}
      > git commit -am "Add template"
      > git push
      ```
    - Change `tutorials/{project_name}/requirements.txt`
    - Edit `tutorials/{project_name}/{project_name}*.py
    """
    print(hprint.dedent(text))


if __name__ == "__main__":
    _main(_parse())
