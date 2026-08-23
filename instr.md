Extend create_project.py with

- Add --src_dir which by default is $GIT_ROOT/class_project_project_template
  Make sure src_dir always exists

--action copy_docker_files
  add an option that copies all and only the Docker files from src_dir to dst_dir

--action create_links
  for all the files in dst_dir that are the same of the corresponding files in
  src_dir, create a link from dst_dir to src_dir

--action compare_docker_files
  report a table with all the files in src_dir and dst_dir and show which ones are
  the same, which one are links, ...

--dry_run to show what would be done without doing it

- Create a create_project.README.md to explain how the script works following the
  proper rules in .claude/rules.md
