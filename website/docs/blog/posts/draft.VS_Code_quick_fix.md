Create .vscode/tasks.json:

```
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Load Quickfix",
      "type": "shell",
      "command": "cat quickfix.txt",
      "problemMatcher": {
        "pattern": {
          "regexp": "^(.*):(\\d+):(\\d+):\\s+(error|warning):\\s+(.*)$",
          "file": 1,
          "line": 2,
          "column": 3,
          "severity": 4,
          "message": 5
        }
      }
    }
  ]
}

main.c:10:5: error: expected ';'
main.c:20:2: warning: unused variable

- Ctrl + Shift + P → “Run Task”
- Select Load Quickfix

