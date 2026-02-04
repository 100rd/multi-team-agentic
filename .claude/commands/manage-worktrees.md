---
name: manage-worktrees
description: List, create, clean up, and manage git worktrees across all project repositories
---

# Manage Worktrees Command

Direct control over git worktrees for advanced users and manual interventions.

## What This Command Does

1. **List Worktrees** - Show all active worktrees
2. **Create Worktree** - Manually create for specific repo
3. **Remove Worktree** - Clean up specific worktree
4. **Cleanup Merged** - Remove all merged worktrees
5. **Sync Status** - Update from git state

## Usage

- `/manage-worktrees`
- "Show me all worktrees"
- "Clean up worktrees"
- "Remove merged worktrees"

## Subcommands

### List All Worktrees
```
/manage-worktrees list

Active Worktrees:
├─ frontend/
│  ├─ feature-auth (3 days old, 12 commits ahead)
│  └─ bugfix-search (1 day old, 2 commits ahead)
├─ backend/
│  ├─ feature-auth (3 days old, 15 commits ahead)
│  └─ feature-payment (new, 3 commits ahead)
└─ mobile/
   └─ feature-auth (2 days old, 8 commits ahead)

Total: 5 active worktrees across 3 repositories
```

### Create New Worktree
```
/manage-worktrees create

Which repository? backend
Feature name? performance-optimization
Base branch? (default: main) develop

Creating worktree...
✓ Created: worktrees/backend/feature-performance-optimization
✓ Branch: feature/performance-optimization
✓ Based on: origin/develop
```

### Remove Specific Worktree
```
/manage-worktrees remove

Select worktree to remove:
1. frontend/feature-auth
2. frontend/bugfix-search
3. backend/feature-auth
> 2

Removing frontend/bugfix-search...
✓ Worktree removed
✓ Branch deleted (was merged)
```

### Cleanup All Merged
```
/manage-worktrees cleanup

Scanning for merged worktrees...
Found 3 merged worktrees:
- frontend/feature-old-ui (merged 5 days ago)
- backend/bugfix-memory-leak (merged 3 days ago)
- mobile/feature-onboarding (merged 1 week ago)

Proceed with cleanup? (y/N) y

✓ Removed 3 merged worktrees
✓ Freed 1.2 GB of disk space
```

## Worktree Information

Each worktree shows:
- **Repository** - Which repo it belongs to
- **Feature Name** - The feature being developed
- **Age** - How long it's been active
- **Commits** - Number ahead of base branch
- **Status** - Clean/Modified/Conflicts
- **Size** - Disk space usage
- **Last Activity** - Last commit time

## Advanced Operations

### Force Remove
```
/manage-worktrees remove --force
```
Remove even with uncommitted changes

### Prune Invalid
```
/manage-worktrees prune
```
Remove worktrees pointing to missing directories

### Archive Old
```
/manage-worktrees archive --older-than=30d
```
Archive worktrees older than 30 days

## Best Practices

1. **Regular Cleanup** - Run cleanup weekly
2. **Check Before Remove** - Ensure changes are committed
3. **Coordinate with Team** - Don't remove active worktrees
4. **Monitor Disk Space** - Worktrees consume space
5. **Keep Organized** - One feature per worktree

## Troubleshooting

### Common Issues

**"Worktree is dirty"**
- Commit or stash changes first
- Use --force to override (data loss risk)

**"Branch not fully merged"**
- Ensure PR is merged
- Check if rebasing is needed

**"Worktree not found"**
- May have been manually deleted
- Run prune to clean registry

## Integration with Orchestrator

The Prime Orchestrator typically manages worktrees automatically. Use this command for:
- Manual interventions
- Troubleshooting
- Cleanup operations
- Advanced workflows

## Safety Features

- Prevents removal of worktrees with uncommitted changes
- Warns before deleting unmerged branches
- Creates backup refs before deletion
- Logs all operations for audit