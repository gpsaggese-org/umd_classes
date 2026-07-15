# GitHub CLI - Complete Command Reference

A comprehensive guide to the most useful GitHub CLI commands for managing repositories, issues, pull requests, and workflows.

## Authentication & Setup

```bash
gh auth status             # Check authentication status
```

## Repository Management

```bash
gh repo view                         # View repository details
gh repo list                         # List your repositories
```

- View repository details
  ```
  > gh repo view
  gpsaggese/gpsaggese.github.io
  No description provided

     GP's University of Maryland Machine Learning Classes

    ## Courses
    ...
  ```

## Issues

```bash
gh issue list                        # List issues
gh issue create                      # Create a new issue
gh issue view <number>               # View a specific issue
gh issue close <number>              # Close an issue
gh issue comment <number>            # Add a comment to an issue
gh issue edit <number>               # Edit an issue
```

## Pull Requests

```bash
gh pr list                           # List pull requests
gh pr create                         # Create a new PR
gh pr view <number>                  # View a PR
gh pr merge <number>                 # Merge a PR
gh pr status                         # Check PR status
```

## Workflows & Actions

```bash
gh workflow list                     # List GitHub Actions workflows
gh run list                          # List workflow runs
gh run view <run-id>                 # View a specific run
gh run watch <run-id>                # Watch a run in progress
```

## Useful Flags & Options

| Flag | Description |
|------|-------------|
| `-R, --repo <owner/repo>` | Specify repository (useful when not in a repo directory) |
| `--json` | Format output as JSON |
| `--limit <number>` | Limit the number of results |
| `-a, --assignee <user>` | Filter by assignee |
| `-L, --label <label>` | Filter by label |
| `-s, --state <state>` | Filter by state (open, closed, merged) |
| `--author <user>` | Filter by author |
| `--head <branch>` | Filter by head branch |
| `--base <branch>` | Filter by base branch |

### Useful One-Liners

  ```bash
  # List all open PRs with JSON output
  gh pr list --state open --json number,title,author

  # Create an issue with a label
  gh issue create --title "Bug Report" --label "bug"

  # List PRs and filter by assignee
  gh pr list --assignee @me
  ```

### Working with Multiple Repositories

  ```bash
  # Use -R flag to specify a different repo
  gh issue list -R owner/another-repo

  # List issues from multiple repos
  gh issue list -R owner/repo1
  gh issue list -R owner/repo2
  ```

## Common Workflows

- Creating a Pull Request
  ```bash
  # 1. Create and checkout a new branch
  git checkout -b feature/my-feature

  # 2. Make your changes
  # ...

  # 3. Commit and push
  git add .
  git commit -m "Add my feature"
  git push origin feature/my-feature

  # 4. Create PR using GitHub CLI
  gh pr create --title "Add my feature" --body "Description of changes"
  ```

- Managing Issues
  ```bash
  # Create an issue
  gh issue create --title "Bug title" --body "Bug description" --label "bug,urgent"

  # Add a comment
  gh issue comment 10 --body "I'm working on this"

  # Close the issue
  gh issue close 10

  # Reopen the issue
  gh issue reopen 10
  ```

## Additional Resources

- [Official GitHub CLI Documentation](https://cli.github.com/)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub API Reference](https://docs.github.com/en/rest)
