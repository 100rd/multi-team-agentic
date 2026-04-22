# SDLC Profiles

Reusable SDLC templates consumed by agent teams. A profile is a YAML file that
declares the **phases, gates, roles and tools** for a class of projects. Per-project
`project/configs/<name>/PROJECT.yaml` picks a profile by name and can override
individual fields.

## Layout

```
.claude/profiles/
├── _schema.yaml            ← JSON Schema describing the profile format
├── dev/                    ← consumed by /dev-team
│   ├── go-service.yaml
│   ├── rust-library.yaml
│   ├── typescript-nextjs.yaml
│   └── python-fastapi.yaml
├── infra/                  ← consumed by /infra-team
│   ├── terraform-module.yaml
│   └── eks-platform.yaml
└── pipeline/               ← consumed by /pipeline (added on demand)
```

## Contract with teams

1. Team Lead reads `project/configs/<name>/PROJECT.yaml`.
2. Loads `.claude/profiles/<team>/<profile>.yaml`.
3. If profile has `extends:` — loads parent first, then merges child on top.
4. Merges `overrides` block from PROJECT.yaml onto the profile.
5. Passes merged config to the `sdlc-runner` skill.
6. Runner walks phases in order, evaluates gates, spawns teammates per `lead_role`.

## Phase semantics

| Field | Meaning |
|-------|---------|
| `cmd` / `cmds` | Shell command(s) whose exit=0 defines success |
| `gates.*` | Named sub-checks, all must pass |
| `blocks_next: true` (default) | Failure stops the pipeline |
| `requires_human_approval` | Pipeline pauses for `y/n` |
| `never_apply: true` | Hard guarantee of no destructive side effects |
| `depends_on: [phase]` | Explicit DAG edges (implicit is sequential order) |

## Inheritance (`extends:`)

```yaml
# .claude/profiles/dev/go-k8s-operator.yaml
extends: go-service
name: go-k8s-operator
phases:
  deploy_test:                         # adds/overrides only this phase
    cmds:
      - kind create cluster
      - make kind-deploy
```

Child inherits every field from the parent; any key set in the child **replaces**
the parent's value. Arrays are replaced, not merged (unless an explicit
`_merge: append` marker is used in the future).

## Per-project overrides

```yaml
# project/configs/my-operator/PROJECT.yaml
name: my-operator
profile: go-k8s-operator
tickets:
  repo: org/my-operator
overrides:
  phases:
    test_gate:
      coverage:
        min_percent: 80                # tighter than profile default (70)
    deploy_test:
      enabled: true                    # was optional in profile
env:
  KIND_CLUSTER: my-operator-kind
```

## Adding a new profile

1. Pick the team directory (`dev/` or `infra/`).
2. Copy an existing profile as a starting point.
3. Validate against `_schema.yaml` (TODO: add CI check).
4. Reference it from a `PROJECT.yaml` and try `/dev-team` or `/infra-team`.
