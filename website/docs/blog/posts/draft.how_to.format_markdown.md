---
title: "How to Format Markdown"
draft: true
authors:
  - gpsaggese
date: 2026-06-09
description: Tools and techniques for formatting Markdown files
categories:
  - Developer Tools
---

https://github.com/hukkin/mdformat
https://github.com/jlevy/flowmark

lint_txt.py

docs/tools/documentation_toolchain/all.notes_toolchain.how_to_guide.md

pytest ./helpers_root/helpers/test/test_hmarkdown_formatting.py::Test_format_md_comparison_and_performance -s --dbg

> lint_txt.py -h
usage: lint_txt.py [-h] [-i INPUT] [-o OUTPUT] [--input_files INPUT_FILES [INPUT_FILES ...]] [--from_file FROM_FILE] [--type TYPE] [-w WIDTH] [--backend {prettier,mdformat,flowmark}] [--mode MODE] [--use_dockerized_prettier] [--no_use_dockerized_prettier]
                   [--use_dockerized_markdown_toc] [--no_use_dockerized_markdown_toc] [--revert] [-a ACTION | -sa SKIP_ACTION | -e ENABLE_ACTION] [--all] [--dockerized_force_rebuild] [--dockerized_use_sudo] [-v {TRACE,DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--no_report_command_line]

See instructions at
docs/tools/documentation_toolchain/all.notes_toolchain.how_to_guide.md.
