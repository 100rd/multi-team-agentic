# Projects Index

Lean registry of projects worked on by this multi-agent system. Details for
each project live in `project/configs/<name>/PROJECT.yaml`. Source code lives
in `project/<name>/` and is **never** polluted with Claude config.

## Active projects

| Name | Profile | Status | GitHub | Config |
|------|---------|--------|--------|--------|
| _example-go-operator_ | `go-service` (planned: `go-k8s-operator`) | template | _n/a_ | [configs/_template](configs/_template/PROJECT.yaml) |

<!-- Add a row per project. Source of truth is the file under project/configs/,
     this table is just for humans. -->

## How to add a new project

1. Clone the repo into `project/<name>/` (manual step).
2. Copy `project/configs/_template/` to `project/configs/<name>/`.
3. Edit `PROJECT.yaml`: set `name`, `profile`, `working_dir`, `tickets.repo`.
4. Append a row to the table above.
5. Run `/dev-team <name> "ship v0.1"` or `/infra-team <name> "initial design"`.

## Profiles available

See `.claude/profiles/README.md` for the full list and how to extend them.

- **dev-team**: `go-service`, `rust-library`, `typescript-nextjs`, `python-fastapi`
- **infra-team**: `terraform-module`, `eks-platform`
