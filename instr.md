Create a script `helpers_root/dev_scripts_helpers/docker_cleanup.py` that
reclaims disk space by removing unused Docker / Apple `container` data
(stopped containers, unused networks, dangling volumes, dangling images,
build cache).

# CLI interface

- `--docker_engine {docker,apple,all}` (default: `all`)
  - Selects which engine(s) to clean.
  - Reuse `helpers.hdocker.get_docker_engine()` / `set_docker_engine()` for
    engine selection and `get_docker_command()` to resolve the CLI binary
    (`docker` -> `docker`, `apple` -> `container`). Do not hardcode the
    binary name.
  - `all` iterates over both engines, skipping (with a warning, not a
    crash) any engine whose CLI is not installed or not running. Reuse
    `helpers.hdocker.is_docker_running()` for the running check.
- `--dry_run` (default: `True`)
  - When `True`: only print what would be deleted and how much space it
    would reclaim. Do not run any destructive command.
  - When `False` (pass `--dry_run False` / `--no_dry_run`, follow the repo's
    `hparser` boolean-flag convention): actually perform the deletions.
- Follow repo conventions: build the CLI with `helpers.hparser`, log via
  `helpers.hdbg` / `logging`, and add a test file under
  `dev_scripts_helpers/system_tools/test/test_docker_cleanup.py` (or
  wherever the script ends up living) per `helpers_root/CLAUDE.md`.

# Engine command mapping

The two engines are NOT symmetric. Apple's `container` CLI has no `network`
subcommand (no plugin installed by default) and no build-cache prune
equivalent (`container builder` only manages the builder instance itself,
not a cache). Skip those steps for the `apple` engine and print a one-line
"not supported by apple engine" note instead of erroring.

| Step                       | `docker` engine                                                          | `apple` engine                                  |
|-----------------------------|---------------------------------------------------------------------------|--------------------------------------------------|
| Report disk usage            | `docker system df`                                                        | `container system df`                             |
| List running/paused/restarting containers | `docker ps -a --filter "status=running" --filter "status=paused" --filter "status=restarting"` | `container list --all` (no per-status filter available; list all and note the limitation) |
| Remove stopped containers     | `docker container prune -f`                                              | `container prune`                                 |
| Remove unused networks        | `docker network prune -f`                                                | **N/A** — no network plugin; skip with a log line |
| Remove dangling volumes        | `docker volume rm $(docker volume ls --filter dangling=true -q)` (no-op if the list is empty — do NOT run `rm` with zero args) | `container volume prune` (built-in; no manual filtering needed) |
| Remove build cache            | `docker builder prune -a -f`                                             | **N/A** — no build-cache prune; skip with a log line |
| Remove dangling images         | `docker rmi -f $(docker images --filter dangling=true -q)` (no-op if the list is empty) | `container image prune` (dangling only; pass `--all` only if the script's policy is to remove ALL unused images, not just dangling ones — confirm before wiring that up) |
| List all images (repo, size, created) | `docker images --format "{{.ID}} {{.Repository}}:{{.Tag}} {{.Size}}"` + `docker inspect -f '{{.Created}}'` per image | `container image list --format json` — parse `configuration.name`, `configuration.creationDate`, and sum `variants[].size`; no per-image inspect call needed |

# Per-operation behavior

For each step above:
1. Compute space attributable to that step (e.g. via `system df` / `image
   list` / `volume list` before running the removal).
2. In `--dry_run` mode: print the items that *would* be deleted and the
   space that would be reclaimed, then stop — do not execute the
   destructive command.
3. In non-dry-run mode: run the destructive command, then print the space
   actually reclaimed.
4. Never run a removal command with an empty argument list (guard `docker
   volume rm` / `docker rmi` — skip with "nothing to remove" if the
   filtered list is empty).

# Reports

- Print `system df` (or `container system df`) once before any operation
  and once after all operations, per engine, so the user sees total space
  reclaimed. Do not duplicate this as a stray step in the middle of the
  image-cleanup section.
- The "list all images" report must be sorted by size (descending) and
  separately available sorted by creation date (descending) — expose both
  via a `--sort_images {size,date}` flag or print both orderings.

# Example (docker engine, informational only, not commands to hardcode)

```
> docker system df
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          26        1         25.21GB   13.03GB (51%)
Containers      130       0         0B        0B
Local Volumes   6         0         15.59GB   15.59GB (100%)
Build Cache     91        0         6.317GB   2.541GB
```
