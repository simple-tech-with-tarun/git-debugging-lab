# Git Debugging Lab

A hands-on repository for learning advanced Git history investigation, recovery, debugging, code attribution, and repository forensics.

This repository contains deliberately constructed Git histories and practical exercises that demonstrate how to investigate unexpected repository states and recover seemingly lost work.

## Learning Objectives

- Investigate Git commit history and branching strategies.
- Identify changes responsible for regressions.
- Understand merge conflicts and branch divergence.
- Recover unreachable Git objects.
- Inspect Git trees, blobs, and commits.
- Understand dangling objects and repository forensics.
- Preserve and verify recovered source files.

## Repository Exercises

### 1. Repository History Investigation

Explore commit history, branch relationships, merge operations, and changes across different development paths.

Topics:
- Git log and history inspection
- Branch divergence
- Merge commits
- Hotfix workflows
- Code attribution

### 2. Advanced History Investigation

Explore an intentionally constructed development history containing alternative environment configurations and production hotfixes.

Topics:
- Feature and hotfix branches
- Testing versus production configuration
- Merge history investigation
- Comparing divergent branches

[View exercise branch](https://github.com/simple-tech-with-tarun/git-debugging-lab/tree/exercise/advanced-history-investigation)

### 3. Repository Forensics

Investigate repository states and application changes through Git history and object inspection.

[View exercise branch](https://github.com/simple-tech-with-tarun/git-debugging-lab/tree/exercise/repository-forensics)

## Evidence and Recovery Exercises

### Dangling Tree Recovery

Recover and inspect source files stored in an unreachable Git tree object.

This exercise demonstrates how Git objects can remain available even after they are no longer referenced by normal branches or tags.

Topics:
- `git fsck`
- Unreachable Git objects
- Tree and blob inspection
- `git cat-file`
- `git ls-tree`
- `git hash-object`
- Recovery verification

**Evidence location:** `evidence/dangling-tree-recovery/`

See the [Dangling Tree Recovery documentation](evidence/dangling-tree-recovery/README.md) for the investigation steps, object IDs, and verification results.

The evidence directory includes:
- Original recovery ZIP archive
- Extracted recovered source files
- Original recovered README
- Unresolved merge-conflict snapshot

## Repository Structure

```text
git-debugging-lab/
├── README.md
├── evidence/
│   └── dangling-tree-recovery/
│       ├── README.md
│       ├── conflict-snapshot.zip
│       └── conflict-snapshot/
│           ├── README.md
│           ├── app.py
│           ├── config.py
│           └── metadata.py
└── exercises/
```

Additional investigation scenarios are maintained in dedicated Git branches.

## Useful Git Commands

| Command | Purpose |
|---|---|
| `git log --graph --oneline --all` | Visualize repository history |
| `git show <commit>` | Inspect a commit |
| `git diff <branch1> <branch2>` | Compare branches |
| `git fsck --full --unreachable` | Find unreachable objects |
| `git cat-file -p <object>` | Inspect Git objects |
| `git ls-tree -r <tree>` | Inspect tree contents |
| `git hash-object <file>` | Calculate a Git blob object ID |

## Related Learning Repositories

This repository is part of a broader Git learning collection:

- [Git Foundations](https://github.com/simple-tech-with-tarun/git-foundations)
- [Git Packfile Lab](https://github.com/simple-tech-with-tarun/git-packfile-lab)
- [Git Cruft Pack Lab](https://github.com/simple-tech-with-tarun/git-cruft-pack-lab)

Each repository focuses on a different aspect of Git internals and practical workflows.

## Purpose

The goal is to develop practical skills in understanding Git beyond everyday commit, push, pull, and merge operations.

All exercises are designed for experimentation, investigation, and learning.
