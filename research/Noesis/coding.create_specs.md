- Create a markdown document describing the specs to implement in Python the
  PR described in `research/Noesis/plan.Noesis.md`
  ```
  ### `PR_P2`: [ ] Cloud Deployment
  ```
- Update `research/Noesis/architecture.md` following the instructions in
  `helpers_root/.claude/skills/readme.write_architecture/SKILL.md`
- Follow the coding and unit test conventions in `.claude/instr.md`
- Do not implement any code

## Plan
- [x] Read `plan.Noesis.md`'s `PR_P2` entry, `architecture.md`, and the
  existing `research/Noesis/*.py` modules to scope what "Cloud Deployment"
  needs on top of `PR_P1`
- [x] Read the Docker/deployment conventions this repo already has:
  `class_project/project_template/Dockerfile*`, its `docker_*.sh` scripts,
  and a sibling directory that already copies the template
  (`tutorials/shap/`), plus the `TODO(gp)` docs in `plan.Noesis.md`
- [x] Write `research/Noesis/spec.PR_P2.md` with the implementation spec:
  new Python entrypoint/health-check, config, Docker assets, cloud target,
  unit tests
- [x] Refresh `research/Noesis/architecture.md` for accuracy (no PR
  references), fixing any drift found against the current code
- [x] `git add` the new spec file (no commit)

## Result
- Created `research/Noesis/spec.PR_P2.md`: full implementation spec for
  `PR_P2` (Cloud Deployment)
  - New Python: `server.py` entrypoint (`_parse()`/`_main()`,
    `_parse_api_keys()`), a `GET /health` endpoint added to
    `platform_api.create_app()`, and a new `requirements.txt`
  - Docker: which `class_project/project_template` files to copy, which
    base Dockerfile to start from, and the deltas needed (drop Jupyter,
    add `server.py` `CMD`, swap `EXPOSE`)
  - Cloud target: recommends Fly.io (with `fly.toml` sketch), notes
    Render/ECS as swap-ins per the plan's own "to start" wording, since
    `plan.Noesis.md` leaves the provider as an open question
  - Also scoped: config/secrets handling, unit tests to add, and
    risks/limitations (mocked fulfillment, no persistence, no rate
    limiting) worth flagging when the deployment goes up
- Refreshed `research/Noesis/architecture.md`: verified it against the
  current `research/Noesis/*.py` code (no drift found) except one stale
  claim, fixed: the `pydantic` row in the External Dependencies table
  pointed to `research/Noesis/requirements.txt` as if it existed; that
  file does not exist yet, so the row now says so instead
- Not done: no Python code, Dockerfile, or deployment config was written;
  per the instructions, `spec.PR_P2.md` is a specification only, ready
  for a follow-up implementation pass

## Follow-up: Switch Docker/Cloud Sections to the Dev-System Flow
- User asked to replace the `class_project/project_template/Dockerfile*`
  approach with this repo's heavier dev-system release flow
  (`docs/tools/dev_system/all.devops_docker*`,
  `docs/tools/docker/all.docker*`); rewrote `spec.PR_P2.md`'s Docker,
  Cloud Target, Configuration, and Unit Tests sections accordingly
- Grounded the rewrite in a real, working precedent already in this repo
  (`tutorials/tutorial_forecast_as_service/`, a dockerized FastAPI
  service using this exact flow) rather than the abstract docs alone;
  verified (not assumed) two concrete bugs in that precedent
  (`os.path.exists()` checks) so the new spec fixes rather than repeats
  them:
  - `invoke.yaml`/`pytest.ini` and every `devops/{docker_build,docker_run}/*`
    symlink there is one `../` short of the real `helpers_root/`
  - `run_docker_forecast.sh` references a `devops/env/default.env` that
    does not exist
- Also verified the repo's ECS task-definition invoke tasks
  (`aws_create_prod_task_definition`, `docker_release_prod_task_definition`)
  depend on an org-wide `shared_configs_bucket_name` that is not set in
  any `repo_config.yaml` in this repo, so `spec.PR_P2.md` now flags that
  path as not usable out of the box and recommends registering the ECS
  task definition/service directly instead
- Not done: still a specification only, no files/symlinks created
