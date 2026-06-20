Write a script to 

1) open an iterm terminal with about 120 characters wide

2) execute in it a certain command

3) take a screenshot of only the iterm terminal and save it in a file

Follow the approach

import subprocess
import time
import os

def run_script_in_iterm(script_path: str, screenshot_path: str, wait_seconds: int = 5):
    # Open iTerm and run script
    apple_script = f"""
    tell application "iTerm"
        activate
        create window with default profile
        tell current window
            tell current session
                write text "bash {script_path}"
            end tell
        end tell
    end tell
    """

    subprocess.run(["osascript", "-e", apple_script])

    # Wait for script execution
    time.sleep(wait_seconds)

    # Take screenshot
    subprocess.run(["screencapture", "-x", screenshot_path])

# Usage
run_script_in_iterm("/path/to/script.sh", "/tmp/screenshot.png", wait_seconds=10)


4) Run the script calling 

`glow TODO.convert_slides_into_book.md`

and saving the file in screenshot1.png

# Conventions
- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`

- When writing unit tests for follow the instructions in
  `.claude/skills/testing.rules.md`

# Create a plan, if needed
- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications
  - When the task is complex, create a `plan.md` with 5 bullet points explaining
    what the plan is
