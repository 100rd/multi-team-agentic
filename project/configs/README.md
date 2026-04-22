# Per-project AI config

One folder per project. The folder name **must** match the row in
`project/project.md` and the code directory under `project/<name>/`.

## Structure

```
project/configs/
└── <name>/
    ├── PROJECT.yaml            # REQUIRED: profile selection + overrides
    ├── conventions.md          # OPTIONAL: project-specific coding rules
    └── custom-skills/          # OPTIONAL: project-scoped skills
        └── <skill>/SKILL.md
```

## PROJECT.yaml contract

Minimum viable file:

```yaml
name: my-operator
profile: go-service
working_dir: ../my-operator          # relative to project/configs/<name>/
tickets:
  repo: org/my-operator
```

See `_template/PROJECT.yaml` for a fully-annotated example with every field.

## What goes here vs. in the code repo

| Lives in `project/configs/<name>/` | Lives in the code repo `project/<name>/` |
|------------------------------------|------------------------------------------|
| PROJECT.yaml (profile, overrides)  | source code, build files, tests           |
| AI conventions / prompts           | `README.md`, `CONTRIBUTING.md`            |
| Project-scoped skills              | CI config (`.github/workflows/`)          |

The code repo stays **100% Claude-agnostic** — anyone can clone it without
knowing this orchestration system exists.
