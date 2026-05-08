For the tests in data605 and msml610 add integration super slow tests that

- makes sure all the lessons can be rendered as pdf
- an integration test that generates the md for all the slides
  after the pre-process stage and checks their result with self.check_output()
- an integration test that generates the tex code for all the slides
  before rendering stage and checks their result with self.check_output()

- Look for code and commands in /Users/saggese/src/umd_classes1/class_scripts/ to
  avoid to create duplicated code

- Add some end-to-end tests for the commands in /Users/saggese/src/umd_classes1/class_scripts/

Add the same logic also for data605 lessons

- When writing code you must always follow the instructions in
  `@.claude/skills/coding.rules.md`

- Generate unit tests for the new code following the instructions in
  `@.claude/skills/testing.rules.md`
