# Reflog-Based Commit Recovery

## Objective

Recover a commit that became unreachable from the current branch after a hard reset, using Git's reflog.

This exercise demonstrates how Git records updates to `HEAD`, how previously referenced commits can be located through the reflog, and how lost work can be restored without recreating the original changes.

## Scenario

A new application build identifier was added and committed. The branch was subsequently reset to its previous commit using `git reset --hard HEAD~1`.

This removed the new commit from the branch's visible history and reverted the working tree.

The original commit was recovered by investigating the reflog and resetting the branch to the recovered commit.

## 1. Create a recoverable change

The following function was added to `app.py`:

```python
def get_build_identifier():
    return "forensic-recovery-001"
```

The change was formatted and checked using Ruff:

```powershell
python -m ruff format .\app.py
python -m ruff check .\app.py
```

Both checks passed.

## 2. Commit the change

```powershell
git add .\app.py
git commit -m "feat: add application build identifier"
```

Created commit:

| Detail | Value |
|---|---|
| Commit | `c8d39f0` |
| Message | `feat: add application build identifier` |
| File changed | `app.py` |
| Insertions | 4 |

## 3. Simulate lost work

The branch was deliberately reset to its previous commit:

```powershell
git reset --hard HEAD~1
```

Result:

```text
HEAD is now at bc58f9f
```

The build identifier function disappeared from the working tree and the commit was no longer reachable through the current branch history.

## 4. Investigate the reflog

The reflog was inspected using:

```powershell
git reflog --date=local -10
```

Relevant entries:

```text
bc58f9f HEAD@{...}: reset: moving to HEAD~1
c8d39f0 HEAD@{...}: commit: feat: add application build identifier
```

The reflog revealed the previous position of `HEAD` before the reset.

The original commit was identified as:

```text
c8d39f01bd40dadf3d36802ce245ed34f5ba04d3
```

## 5. Inspect the recovered commit

The commit metadata and change summary were inspected:

```powershell
git show --stat c8d39f0
```

The original file content was inspected directly from the commit:

```powershell
git show c8d39f0:app.py
```

The output confirmed that the recovered commit contained the `get_build_identifier()` function.

## 6. Restore the lost commit

The branch was restored to the original commit:

```powershell
git reset --hard c8d39f0
```

Result:

```text
HEAD is now at c8d39f0 feat: add application build identifier
```

The branch history once again included the recovered commit.

## 7. Verify the recovery

The restored history was checked:

```powershell
git log --oneline -5
```

The recovered commit appeared at the branch tip:

```text
c8d39f0 feat: add application build identifier
```

The working tree was verified:

```powershell
git status -sb
```

Result:

```text
## exercise/reflog-recovery
```

The recovered function was also executed:

```powershell
python -c "from app import get_build_identifier; print(get_build_identifier())"
```

Expected and observed output:

```text
forensic-recovery-001
```

## 8. Recovery evidence

| Evidence | Result |
|---|---|
| Original commit | `c8d39f0` |
| Commit after simulated loss | `bc58f9f` |
| Reflog investigation | Successful |
| Commit content inspection | Successful |
| Commit restoration | Successful |
| Application validation | Successful |
| Working tree | Clean |

## Key Learnings

- Git reflog records recent changes to local references, including movements of `HEAD`.
- A hard reset can remove a commit from the current branch history without immediately deleting its underlying Git object.
- The reflog can help locate commits that are no longer referenced by normal branches.
- `git show` can inspect a commit and retrieve file content directly from its object history.
- `git reset --hard <commit>` can restore a branch and working tree to a recovered commit.
- Reflog entries are local and subject to expiration and garbage collection. They should not be treated as permanent backups.

## Conclusion

The exercise successfully demonstrated recovery of a commit after a hard reset using Git reflog.

The original commit `c8d39f0` was located, inspected, restored, and functionally validated without recreating the lost change.

This provides a practical recovery workflow for investigating accidentally discarded local commits and understanding how Git preserves recently referenced history.
