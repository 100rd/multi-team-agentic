---
name: sdlc-runner
description: |
  Run a project through an SDLC profile (phases, gates, roles) declared in
  project/configs/<name>/PROJECT.yaml and .claude/profiles/<team>/<profile>.yaml.
  Invoke when a team Lead (dev-team, infra-team, pipeline-team) starts work on
  a named project. Returns merged config and phase plan; the Lead then spawns
  teammates and walks the phases.
model: sonnet
context: fork
user-invocable: true
tools: Read, Grep, Glob, Bash
---

# SDLC Runner

You are the **phase engine** for agent teams. Your inputs: a project name. Your
output: a merged profile config and a concrete phase-by-phase execution plan
that the team Lead follows.

## Inputs

- `$1` — project name (must match a folder under `project/configs/`).
- Environment: current working dir is `multi-team-agentic/` repo root.

## Algorithm

### 1. Load per-project config

```
project/configs/$1/PROJECT.yaml
```

Fail with a clear error if the file does not exist. Required fields:
- `name`
- `profile` (or `profile: auto` to trigger detection)
- `working_dir` (relative to `multi-team-agentic/` — typically `../<name>` or `project/<name>`)

### 2. Resolve profile

Determine the team from the caller (dev-team, infra-team, pipeline-team).

- If `profile` is a name → load `.claude/profiles/<team>/<profile>.yaml`.
- If `profile: auto` → walk `.claude/profiles/<team>/*.yaml`, evaluate each
  profile's `detect:` block against `working_dir`. Pick the first match. If no
  match, fail.

### 3. Resolve inheritance

If the profile has `extends: <parent>`:
1. Load `<parent>` from the same team directory.
2. Recursively resolve the parent's `extends` (guard against cycles, max depth 5).
3. Merge child on top of parent **field by field**:
   - Scalars: child replaces parent.
   - Objects: deep-merge, child keys win.
   - Arrays: child replaces parent entirely (no implicit append).

### 4. Apply per-project overrides

PROJECT.yaml may contain an `overrides:` block with the same shape as the
profile. Apply it on top of the resolved profile using the same merge rules.

### 5. Validate

- Every `depends_on` reference must name an existing phase.
- Every `lead_role` must appear in `team_roles.required` or `team_roles.optional`.
- Every `tools.required` must resolve via `command -v` on the current host;
  missing ones produce a blocker, not a warning.

### 6. Emit the plan

Print to the Lead:

```
PROJECT:      <name>
PROFILE:      <profile>   (extends chain: parent -> child)
WORKING_DIR:  <path>
TEAM:         <team>
ROLES:        required=[…]  optional=[…]

PHASES (in order):
  1. scaffold         gate=`go build ./...`             blocks_next=yes
  2. implement        source=github-issues               loop=all_issues_closed
  3. build_gate       gate=`go build -o bin/ ./...`      artifacts=bin/
  4. lint_gate        gates=2                             blocks_next=yes
  5. test_gate        coverage>=70%                      blocks_next=yes
  6. deploy_test      HUMAN APPROVAL                     enabled=false (skip)
  7. ready_for_review gates=2                             never_apply=false

MISSING TOOLS: (empty or list)
WARNINGS:      (empty or list)
```

## Phase execution rules (given to the Lead)

1. **Sequential by default.** Phase N+1 does not start until phase N succeeds.
2. **`depends_on` makes it explicit**, and enables parallel phases that share
   a common prerequisite (e.g. `lint_gate` and `test_gate` both depend on
   `implement` — they can run concurrently via teammates in worktrees).
3. **A failed gate halts the pipeline** unless `blocks_next: false`.
4. **`requires_human_approval: true`** — the Lead pauses and prints a
   CRITICAL DECISION block (see `.claude/rules/critical-decisions.md`).
5. **`never_apply: true`** — combined with existing permission denies in
   `.claude/settings.json`, this is a belt-and-suspenders guarantee that the
   phase cannot mutate production.
6. **Role assignment.** When a phase has `lead_role`, the Lead spawns that
   teammate (from `team_roles`) with `isolation: "worktree"` if they write
   files, no isolation if they only read.

## What this skill does NOT do

- It does not spawn teammates itself. That is the team Lead's job.
- It does not run any `cmd` / `cmds` from the profile. The Lead delegates
  that to the teammate assigned to the phase.
- It does not modify PROJECT.yaml. Overrides are read-only here.

## Failure modes

| Situation | Behaviour |
|-----------|-----------|
| PROJECT.yaml missing | Fail: "project/configs/<name>/PROJECT.yaml not found" |
| Profile reference unresolved | Fail with list of available profiles for that team |
| `extends` cycle | Fail at depth > 5 |
| `depends_on` target missing | Fail with typo hint |
| `tools.required` not installed | Fail with `brew install`/`cargo install` hints where known |
