# `PR_P2`: Cloud Deployment - Implementation Spec
- This document specifies the Python code, Docker assets, and cloud deployment config
  needed to implement `PR_P2` from `research/Noesis/plan.Noesis.md`
- Scope, as stated in the plan:
  - Containerize `PR_P1`'s API into a single Docker image
  - Deploy to a cloud target: a single-node container service (e.g. AWS ECS, Fly.io,
    or Render, to start); Kubernetes deferred until there is more than one process to
    orchestrate
  - Result: a `NoesisMarket`/`NoesisServer` instance reachable at a public URL
- Containerization/release approach: follow this repo's dev-system Docker flow
  (`devops/` dir, `dev.Dockerfile`/`prod.Dockerfile`, `poetry`, `invoke` release
  tasks, ECR/GHCR registries), documented in
  `docs/tools/dev_system/all.devops_docker.how_to_guide.md`,
  `docs/tools/dev_system/all.devops_docker.reference.md`,
  `docs/tools/dev_system/all.devops_docker_auto_release.explanation.md`,
  `docs/tools/dev_system/all.docker_optimizer_container.how_to_guide.md`,
  `docs/tools/docker/all.docker.tutorial.md`, and
  `docs/tools/docker/all.dockerized_flow.explanation.md`, instead of the lightweight
  `class_project/project_template/Dockerfile*` template
- Roadmap position: `v0.1`, cumulative on top of `PR_M1`, `PR_M2`, `PR_S1`, `PR_P1`
  (all `[x]` already)
- This is a specification only: no code in this document has been implemented; it
  describes what `PR_P2` needs to add on top of the current `research/Noesis/*.py`
  code

## Out of Scope
- Persistent datastore for the order book / contract log / request log: `PR_P2b`, a
  separate PR; this PR keeps the current in-memory `List`/`Dict` state
  (`architecture.md` Weakness 6), so a redeploy or crash still loses all pending
  state
- Real payment/credit gating on `POST /bids`: `PR_P3`/`PR_P4`
- Real fulfillment via `NoesisServer`'s `Gateway`: `PR_M8`; the deployed instance
  keeps `contract_dispatch.mock_fulfill()` as `create_app()`'s default
  `fulfillment_fn`
- Kubernetes, multi-region, autoscaling: the plan explicitly defers these until there
  is more than one process to orchestrate
- Provisioning the ECS cluster/service/load balancer themselves (see "Cloud Target"
  below): one-time AWS infrastructure setup, not Python or Docker-asset code

## Current State (what This PR Builds On)
- `platform_api.create_app(order_book, gateway, api_keys, *, fulfillment_fn=mock_fulfill) -> fastapi.FastAPI`
  is the only thing to containerize; it wraps an `OrderBook` and a `Gateway` behind
  HTTP, with `X-API-Key` auth on `POST /bids`, `POST /asks`, and `POST /completions`
- Gaps that block a cloud deploy today, per `architecture.md`:
  - No standalone launch script exists: nothing calls `create_app()` and hands the
    result to `uvicorn`; `create_app()` is exercised only via
    `fastapi.testclient.TestClient` in tests
  - `api_keys: Dict[str, str]` is a plain constructor argument, not sourced from
    environment/config; a container entrypoint needs to build it from something a
    container platform can set (an env var)
  - No health-check endpoint exists; every candidate cloud target polls one to decide
    whether the container is healthy
  - `research/Noesis` is not yet a "runnable dir" in this repo's sense
    (`docs/tools/dev_system/all.devops_docker.reference.md`'s "Code Organization"
    section): it has no `devops/` dir, no `changelog.txt`, and no `repo_config.yaml`
    of its own, all three needed by the `invoke` Docker tasks this PR reuses
  - State is entirely in-memory and per-process (unchanged by this PR); a redeploy or
    restart loses every pending order, contract, and round

## New Python Code

### `research/Noesis/main.py` (new)
- Entrypoint module that builds and exposes a module-level `app`, run via
  `uvicorn research.Noesis.main:app --host 0.0.0.0 --port 8000`
  - Follows this repo's existing pattern for a dockerized FastAPI service:
    `tutorials/tutorial_forecast_as_service/api/main.py` builds `app` at import time
    and is served the same way
    (`uvicorn tutorial_forecast_as_service.api.main:app ...`, see its
    `devops/compose/docker-compose.forecast.yml`)
  - Kept as a flat `research/Noesis/main.py`, not a nested `api/` subpackage like the
    tutorial's: every existing module in this directory (`batch_call_auction.py`,
    `contract_dispatch.py`, `passthrough_proxy.py`, `platform_api.py`) is a flat file
    with an `rn<abbrev>` import alias, and `main.py` should match that convention
    rather than introduce a new one
- Contents:
  - `hdbg.init_logger(verbosity=logging.INFO)` at import time (matches
    `tutorial_forecast_as_service/api/main.py`)
  - `_parse_api_keys(raw: str) -> Dict[str, str]` (private helper):
    - Parses `NOESIS_API_KEYS="key1:account1,key2:account2"`
      (`os.environ.get("NOESIS_API_KEYS", "")`) into the `Dict[str, str]`
      `create_app()` expects
    - An empty string parses to `{}` (no keys configured; every write endpoint then
      rejects every caller with `401`, a safe default)
    - `hdbg.dassert_in(":", entry, ...)` on each comma-separated entry, so a
      malformed value fails fast at process startup instead of silently starting with
      zero or the wrong keys
  - Module-level: `order_book = rnbacaau.OrderBook()`,
    `gateway = rnopapro.Gateway()`,
    `api_keys = _parse_api_keys(os.environ.get("NOESIS_API_KEYS", ""))`,
    `app = rnoplapi.create_app(order_book, gateway, api_keys)`

### `platform_api.py`: Add `GET /health` (extend Existing File)
- Add one unauthenticated endpoint inside `create_app()`:
  `GET /health -> {"status": "ok"}`
- Needed because every candidate cloud target polls an HTTP health check to decide
  whether to route traffic to the container or restart it:
  - AWS ECS: the task definition's `healthCheck`, or an ALB target group's health
    check (see "Cloud Target" below)
  - Fly.io / Render, if used instead: their own equivalent HTTP health-check settings
- Does not read `order_book`/`gateway` state, so it stays healthy before the first
  bid/ask is ever submitted
- Update the module docstring's endpoint list (`NoesisMarket: ...`,
  `NoesisServer: ...`) to add this line, following `.claude/skills/coding.rules.md`'s
  "Update Docstrings If Out-of-sync"

## Make `research/Noesis` a Runnable Dir
- `docs/tools/dev_system/all.devops_docker.reference.md`: "Each directory that is
  runnable contains the files: `changelog.txt`, `devops`"; the closest existing
  example of a single dockerized FastAPI service structured this way in this repo is
  `tutorials/tutorial_forecast_as_service/`, used as the template below (its Dash
  frontend and Prophet forecast engine do not apply here, only its directory shape)
- New real (non-symlinked) files:
  - `research/Noesis/changelog.txt`: seed with `# noesis_platform-1.0.0` / a date /
    "First release", matching
    `tutorials/tutorial_forecast_as_service/changelog.txt`'s format
  - `research/Noesis/repo_config.yaml`:
    `yaml     repo_info:   repo_name: research   github_repo_account: gpsaggese   github_host_name: github.com   invalid_words:   issue_prefix: UmdTask docker_info:   docker_image_name: noesis_platform s3_bucket_info:   unit_test_bucket_name: s3://cryptokaizen-unit-test   html_bucket_name: s3://cryptokaizen-html   html_ip: http://172.30.2.44 container_registry_info:   ecr: 623860924167.dkr.ecr.eu-north-1.amazonaws.com   ghcr: ghcr.io/cryptokaizen runnable_dir_info:   use_helpers_as_nested_module: 1   venv_tag: helpers   dir_suffix: noesis_platform     ` -
    `container_registry_info` and `s3_bucket_info` are copied from this repo's own
    top-level `repo_config.yaml`, not invented: without `container_registry_info`,
    `helpers.repo_config_utils.RepoConfig       .get_container_registry_url()` has
    nothing to read once `invoke` is run from inside `research/Noesis/` (see the bug
    noted below, where `tutorials/tutorial_forecast_as_service/repo_config.yaml`
    omits it) - `issue_prefix: UmdTask` reuses the top-level repo's prefix, since
    `research/Noesis` has no GitHub issue tracker of its own
  - `research/Noesis/.dockerignore`: `text # The build context for DEV is only
    devops, so we ignore everything but
    # devops
    ** !devops/** !helpers_root/devops/\*\*
    `(copied verbatim from`tutorials/tutorial_forecast_as_service/.dockerignore`)
- New symlinks, reusing the generic `invoke` task definitions and pytest config
  instead of duplicating them (same intent as
  `tutorials/tutorial_forecast_as_service`'s top-level symlinks):
  - `research/Noesis/tasks.py -> ../../tasks.py`
  - `research/Noesis/conftest.py -> ../../conftest.py`
  - `research/Noesis/invoke.yaml -> ../../helpers_root/invoke.yaml`
  - `research/Noesis/pytest.ini -> ../../helpers_root/pytest.ini`
  - **Correction vs. the precedent**: `tutorials/tutorial_forecast_as_service`'s own
    `invoke.yaml -> ../helpers_root/invoke.yaml` and
    `pytest.ini -> ../helpers_root/pytest.ini` are broken symlinks (verified:
    `os.path.exists()` is `False` for both; they resolve to the nonexistent
    `tutorials/helpers_root/...` because they are one `../` short of the real
    `helpers_root/` at the repo root). Its `tasks.py -> ../../tasks.py` and
    `conftest.py -> ../../conftest.py` use the correct depth and do resolve
    `research/Noesis/` sits at the same depth from the repo root as
    `tutorials/tutorial_forecast_as_service/` (`<top-dir>/<project-dir>/`), so the
    fix is to use `../../helpers_root/...` (one more `../` than the buggy precedent)
    for anything pointing at `helpers_root/`, confirmed by resolving
    `research/Noesis/../../helpers_root` to the real `helpers_root/` dir

## Docker
- New dir `research/Noesis/devops/`, modeled on
  `tutorials/tutorial_forecast_as_service/devops/`, with the same `docker_build/` /
  `docker_run/` / `compose/` split described in
  `docs/tools/dev_system/all.devops_docker.reference.md`'s "Code Organization"
  section
- `research/Noesis/devops/docker_build/`:
  - Symlink the boilerplate build files this repo already shares across every
    runnable dir, at the **corrected** depth (see the symlink note above;
    `docker_build/` is one level deeper than the dir's own root, so these need
    `../../../../helpers_root/...`, not the precedent's broken
    `../../../helpers_root/...`): `dev.Dockerfile`, `prod.Dockerfile`,
    `dockerignore.dev`, `dockerignore.prod`, `etc_sudoers`, `fstab`,
    `create_users.sh`, `install_cprofile.sh`, `install_dind.sh`,
    `install_os_packages.sh`, `install_publishing_tools.sh`,
    `install_python_packages.sh`, `update_os.sh`, `poetry.toml`
  - New real `pyproject.toml` (project-specific dependencies, not boilerplate, so not
    symlinked, matching how
    `tutorials/tutorial_forecast_as_service/devops/docker_build/pyproject.toml` is a
    real file while its neighbors are symlinks): a `[tool.poetry]` section declaring
    `fastapi`, `pydantic`, `uvicorn = {version = "*", extras = ["standard"]}`, plus
    the test dependencies already needed to run `research/Noesis/test/` (`pytest`,
    and whatever `helpers.hunit_test` already pulls in for the rest of this repo's
    dev image)
    - This is the resolution for the gap `architecture.md` already flags:
      `platform_api.py`'s docstring points to a `research/Noesis/requirements.txt`
      that does not exist; this PR resolves it with a `poetry`-managed
      `pyproject.toml` instead of a plain `requirements.txt`, matching how every
      other runnable dir in this repo declares dependencies. Update that docstring
      line to point here once implemented
  - `poetry.lock` / `pip_list.txt`: generated, not hand-written, by
    `invoke docker_build_local_image --version <VERSION> --poetry-mode update` (see
    "Release Flow" below), same as every other runnable dir
- `research/Noesis/devops/docker_run/`:
  - Symlink the boilerplate run files at the corrected depth: `bashrc`,
    `docker_setenv.sh`, `entrypoint.sh`, `run_jupyter_server.sh`, `test_setup.sh`
  - New real `run_docker_noesis.sh` (local dev launcher), modeled on
    `tutorials/tutorial_forecast_as_service/devops/docker_run/run_docker_forecast.sh`:
    brings up the compose override below (`docker compose ... up -d noesis_api`),
    prints its status, tails its logs; unlike the precedent, actually create the
    `devops/env/default.env` its `--env-file` flag references (the precedent's script
    references `devops/env/default.env`, but that dir does not exist in
    `tutorials/tutorial_forecast_as_service/`, a second gap this PR should not
    reproduce)
- `research/Noesis/devops/env/default.env` (new, real, minimal): a placeholder so
  `run_docker_noesis.sh`'s `--env-file` flag resolves; `NOESIS_API_KEYS` itself stays
  out of this file (not committed) and is passed via `docker compose run -e` / the
  shell environment instead
- `research/Noesis/devops/compose/docker-compose.noesis.yml` (new, real), modeled on
  `tutorials/tutorial_forecast_as_service/devops/compose/docker-compose.forecast.yml`:
  ```yaml
  version: '3'
  services:
    noesis_api:
      extends:
        file: tmp.docker-compose.yml
        service: app
      command: >
        uvicorn research.Noesis.main:app
        --host 0.0.0.0 --port 8000
      ports:
        - "8000:8000"
  ```
  - `tmp.docker-compose.yml` is the base compose file `invoke docker_bash` generates
    from this repo's shared compose templates
    (`docs/tools/dev_system/all.devops_docker.reference.md`'s "Detailed Description
    of Files"); `noesis_api` only overrides the `command` and `ports`

## Release Flow
- Reuses the generic `invoke` Docker tasks already vendored into this repo's
  `tasks.py` (symlinked above), run from inside `research/Noesis/`, the same tasks
  `docs/tools/dev_system/all.devops_docker.how_to_guide.md`'s "invoke targets"
  section documents:
  1. `cd research/Noesis`
  2. `i docker_build_local_image --version 1.0.0`: builds
     `noesis_platform:local-<user>-1.0.0` from `devops/docker_build/dev.Dockerfile`
  3. `i docker_bash --stage local --version 1.0.0`, then inside:
     `pytest research/Noesis/test` as a smoke test before release
  4. `i docker_tag_local_image_as_dev --version 1.0.0`
  5. `i docker_push_dev_image --version 1.0.0`: pushes to `repo_config.yaml`'s
     `container_registry_info.ecr`
     (`623860924167.dkr.ecr.eu-north-1.amazonaws.com/noesis_platform:dev-1.0.0`)
  6. `i docker_build_prod_image --version 1.0.0`: self-contained image, code copied
     in rather than bind-mounted (per `all.devops_docker.how_to_guide.md`'s
     dev-vs-prod distinction)
  7. `i docker_push_prod_image --version 1.0.0`
  - Or the end-to-end wrappers `i docker_release_dev_image --version 1.0.0` /
    `i docker_release_prod_image --version 1.0.0`, which run the equivalent steps
    plus the QA/test gates `all.devops_docker.how_to_guide.md`'s "Overview of how to
    release an image" describes
- This reuses this repo's existing AWS account and ECR/GHCR registries (same ones
  `research/Noesis` shares with every other runnable dir here); it does not stand up
  new cloud infrastructure by itself, it only produces and publishes the versioned
  image

## Cloud Target
- Recommendation: AWS ECS, the first option `plan.Noesis.md` lists, and the only one
  this repo's `invoke` tasks have built-in tooling for
  (`helpers/lib_tasks/lib_tasks_aws.py`'s `aws_create_prod_task_definition`,
  `helpers/lib_tasks/lib_tasks_docker_release.py`'s
  `docker_release_prod_task_definition`, and `helpers.haws.update_task_definition()`,
  which `docs/tools/dev_system/all.devops_docker.how_to_guide.md`'s "invoke targets"
  section documents as `docker_update_prod_task_definition`)
- What actually works out of the box vs. what needs setup first, checked against the
  code rather than assumed:
  - `aws_create_prod_task_definition` / `aws_create_preprod_task_definition` /
    `aws_create_test_task_definition` register a new ECS task definition family
    (`noesis_platform-prod`, etc.) from a **shared, org-wide** template: they call
    `_get_ecs_task_definition_template()` and `_get_efs_mount_config_template()`
    (`helpers/lib_tasks/lib_tasks_aws.py`), which read
    `ecs_task_definition_template.json` and `efs_mount_config_template.json` off
    `repo_config.yaml`'s `s3_bucket_info.shared_configs_bucket_name`
  - That key is **not set** in this repo's own `repo_config.yaml` (root),
    `helpers_root/repo_config.yaml`, or
    `tutorials/tutorial_forecast_as_service/repo_config.yaml`: none of the three
    define `shared_configs_bucket_name`. So this task-definition automation is
    inherited library code from the `helpers`/`cmamp` template, not something already
    wired up for any runnable dir in this teaching repo, `research/Noesis` included
  - `docker_update_prod_task_definition` additionally takes `airflow_dags_s3_path`
    and is built around this org's Airflow-based production deployment flow (per its
    own "TODO(gp): This might become obsolete" comment); it is not a generic "point a
    task definition at a new image" tool despite the how-to guide listing it as one,
    and does not fit a standalone FastAPI prototype like `NoesisPlatform`
  - `docker_release_prod_task_definition` (and its `test`/`preprod` siblings) only
    **update** an already-registered task definition's image; they do not create or
    update a running ECS **service**, so even once a task definition exists, rolling
    a new image out to a live service still needs a separate
    `aws ecs update-service --force-new-deployment` (or equivalent), which none of
    these invoke tasks do
- Given the above, two viable paths, both keeping the "Result" line true (a
  `NoesisMarket`/`NoesisServer` instance reachable at a public URL):
  1. Provision the missing org-wide template (`shared_configs_bucket_name` plus its
     S3 JSON templates) so `aws_create_prod_task_definition` and
     `docker_release_prod_task_definition` work as designed; this is a one-time
     AWS/Causify-infra setup task, out of scope for this PR's Python/Docker code
  2. Skip that template and register the ECS task definition and service directly
     (`aws ecs register-task-definition` / `aws ecs create-service`, or their
     Terraform/CDK equivalent), pointing the container definition at the image
     `docker_push_prod_image` above already publishes to ECR, with
     `containerPort: 8000` and a `healthCheck`/ALB target group pointed at
     `GET /health`; simpler for a single-container research prototype that does not
     need the EFS mounts and CloudWatch log-group naming baked into the org template
  - This spec recommends path 2 for `v0.1`: it needs nothing beyond what
    `research/Noesis` itself controls, whereas path 1 depends on provisioning shared
    infrastructure this repo does not have wired up yet for any project
- Fly.io and Render remain valid alternatives per the plan's own "to start" wording,
  but neither has any existing tooling in this repo the way ECS does; picking one of
  them instead would mean building the release/deploy tooling from scratch rather
  than reusing what `docker_release_dev_image` / `docker_build_prod_image` already
  provide

## Configuration and Secrets
- `NOESIS_API_KEYS`: the only required secret; holds the same `Dict[str, str]`
  `PR_P1`'s `create_app()` already accepts as a plain Python argument, parsed by
  `main.py`'s `_parse_api_keys()` above
  - Locally: passed via `docker compose run -e NOESIS_API_KEYS=...` or the shell
    environment, never committed to `devops/env/default.env`
  - On ECS: set as a task definition `secrets` entry backed by AWS Secrets Manager or
    Parameter Store, not a plain `environment` value
- `--host` / `--port` are not exposed as flags in this design (unlike an
  argparse-based script): `main.py`'s `app` object is host/port-agnostic, and
  `research/Noesis/devops/compose/docker-compose.noesis.yml`'s `command:` line, or
  the ECS container definition's `containerPort`, is where the bind address/port is
  actually set
- No other configuration: `fulfillment_fn` stays hardcoded to
  `contract_dispatch.mock_fulfill` (`create_app()`'s existing default); wiring a real
  fulfillment layer is `PR_M8`, out of scope here

## Unit Tests
- New file `research/Noesis/test/test_main.py`, naming per
  `.claude/skills/testing.rules.md`
- `Test__parse_api_keys(hunitest.TestCase)`:
  - `test1`: a well-formed `"key1:acct1,key2:acct2"` string parses to
    `{"key1": "acct1", "key2": "acct2"}`
  - `test2`: an empty string parses to `{}`
  - `test3`: a malformed entry (missing `:`) raises `AssertionError`
- Extend `research/Noesis/test/test_platform_api.py` (existing file, add a case to
  its existing class rather than a new one):
  - `test`: `GET /health` on an app built via `create_app()` returns status `200` and
    body `{"status": "ok"}` without an `X-API-Key` header
- Not unit-tested directly: `main.py`'s module-level `app` construction (it reads
  `NOESIS_API_KEYS` as an import-time side effect, which is awkward to isolate in a
  test without monkeypatching the environment before import); `_parse_api_keys()` is
  factored out specifically so the parsing logic is testable without that

## Risks and Limitations to Call Out
- The deployed instance still runs `PR_M2`'s mocked fulfillment (`mock_fulfill()`'s
  randomized pass/fail) and `PR_S1`'s stub/test providers, not a real LLM call: a
  public URL makes the prototype reachable, it does not make its answers real; state
  this wherever the deployment is announced
- No persistence (`PR_P2b`, a separate PR): a redeploy or crash restart loses every
  pending bid/ask, contract, and request log; acceptable for a `v0.1` demo, not for
  anything a buyer/seller would rely on
- No rate limiting or abuse protection beyond the existing `X-API-Key` check on write
  endpoints; read endpoints (`GET /contracts/{id}`, `GET /rounds/{tier}/latest`,
  `GET /logs`) stay unauthenticated once public, matching `PR_P1`'s existing scope
  and `architecture.md`'s Weakness 9 (an open item this PR does not resolve)
- This PR is the first time anything under `research/` becomes a "runnable dir" in
  this repo's dev-system sense; the only close precedent
  (`tutorials/tutorial_forecast_as_service/`) has the two concrete bugs noted above
  (broken `helpers_root`-relative symlinks, a `run_docker_forecast.sh` referencing a
  `devops/env/` that does not exist), so this is closer to a new, mostly-untested
  integration than a copy of a working setup; budget time in implementation for
  fixing issues this spec did not anticipate
- The ECS task-definition automation this repo ships is coupled to org-wide shared
  infrastructure (`shared_configs_bucket_name`, Airflow DAG deployment) that is not
  configured for this teaching repo; do not assume
  `docker_release_prod_task_definition` alone reaches a running, publicly reachable
  service (see "Cloud Target" above)

## Result (to Fill in Once Implemented)
- A `NoesisMarket`/`NoesisServer` instance reachable at a public URL, per
  `plan.Noesis.md`'s `PR_P2` Result line
- Record what was actually implemented vs. deferred, e.g. whether the ECS task
  definition/service was created via path 1 or path 2 above, and whether AWS ECS was
  used or the team switched to Fly.io/Render instead
