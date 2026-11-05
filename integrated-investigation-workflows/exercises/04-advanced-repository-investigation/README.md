# Advanced Repository Investigation

A practical Git investigation exercise demonstrating how to recover lost commits and reconstruct repository history using reflogs, Git object inspection, reachability analysis, and commit recovery techniques.

## Objectives

- Investigate commits that are no longer reachable from a branch.
- Use reflogs to locate previously referenced commits.
- Inspect Git commit, tree, and blob objects.
- Understand reachable and unreachable Git objects.
- Use `git fsck` to identify unreachable objects.
- Recover lost work without manually recreating files.
- Verify recovered source code and tests.

## Scenario

A deployment metadata implementation was committed successfully but subsequently disappeared from the current branch history after a hard reset.

The lost implementation contained:

- A deployment status accessor.
- A deployment region accessor.
- A deployment metadata function combining both values.
- Tests validating the implementation.

The objective was to investigate the repository, locate the missing commit, inspect its underlying Git objects, and recover the implementation.

## 1. Establish the Baseline

The initial application contained:

```python
def get_deployment_status():
    return "ready"
```

The baseline test verified that the deployment status returned the expected value.

Baseline commit:

`871f257` - `test: add advanced repository investigation baseline`

## 2. Implement and Commit the Changes

The application was extended with deployment metadata functionality:

```python
def get_deployment_status():
    return "ready"


def get_deployment_region():
    return "ap-south-1"


def get_deployment_metadata():
    return {
        "status": get_deployment_status(),
        "region": get_deployment_region(),
    }
```

Three tests were implemented:

- `test_deployment_status()`
- `test_deployment_region()`
- `test_deployment_metadata()`

The tests passed before committing.

Commit:

`1fbe7f4` - `feat: add deployment metadata recovery scenario`

## 3. Simulate Lost Work

The commit was removed from the current branch history:

```powershell
git reset --hard HEAD~1
```

The branch returned to:

`871f257`

The working tree was reset to the baseline implementation.

The original commit was no longer part of the branch history.

## 4. Locate the Commit Using Reflog

The reflog was inspected:

```powershell
git reflog --oneline -10
```

Relevant output:

```text
871f257 HEAD@{0}: reset: moving to HEAD~1
1fbe7f4 HEAD@{1}: commit: feat: add deployment metadata recovery scenario
```

The reflog retained the reference to the lost commit, making it possible to identify its original commit hash.

## 5. Inspect the Lost Commit

The commit object was inspected directly:

```powershell
git cat-file -p 1fbe7f4
```

The output identified:

- Commit tree: `5970aee0eae2da0b9b738eeb1754f99f6254946e`
- Parent commit: `871f257b6e6701caccc244088e49b402c9ddfc8c`
- Original commit message and metadata.

The complete changes were also inspected:

```powershell
git show -p 1fbe7f4
```

## 6. Inspect the Commit Tree

The files stored in the commit were identified using:

```powershell
git ls-tree -r 1fbe7f4 -- .\integrated-investigation-workflows\exercises\04-advanced-repository-investigation\
```

The output identified two blob objects:

| File | Blob SHA |
|---|---|
| `application.py` | `494a7fb51489c0264411aa2731a20a96a03a3a54` |
| `test_recovery.py` | `e452efbf4a2f754b9cf6e9e27f626226abe0830d` |

## 7. Recover File Contents from Git Objects

Both blobs were inspected independently:

```powershell
git cat-file -p 494a7fb51489c0264411aa2731a20a96a03a3a54
```

```powershell
git cat-file -p e452efbf4a2f754b9cf6e9e27f626226abe0830d
```

Both files were intact in the Git object database, even though the branch no longer contained the implementation.

## 8. Investigate Object Reachability

First, unreachable objects were inspected:

```powershell
git fsck --unreachable
```

The original lost commit was not reported because the reflog still referenced it.

Next, reflog references were excluded:

```powershell
git fsck --no-reflogs --unreachable
```

This time, Git identified:

```text
unreachable commit 1fbe7f460ac4f241f8a8798c71aa82b913c8917f
unreachable tree 5970aee0eae2da0b9b738eeb1754f99f6254946e
unreachable blob 494a7fb51489c0264411aa2731a20a96a03a3a54
unreachable blob e452efbf4a2f754b9cf6e9e27f626226abe0830d
```

This confirmed that the original commit and its associated objects were unreachable from the current refs when reflogs were excluded.

## 9. Recover the Lost Commit

The original commit was restored to the current branch using:

```powershell
git cherry-pick 1fbe7f4
```

Git created a new commit:

`f715606` - `feat: add deployment metadata recovery scenario`

The new commit has a different SHA because cherry-pick creates a new commit object while applying the original changes.

## 10. Validate the Recovery

The recovered implementation was tested:

```powershell
python .\integrated-investigation-workflows\exercises\04-advanced-repository-investigation\test_recovery.py
```

Result:

```text
PASS: deployment recovery tests are correct
```

All three tests passed.

## Findings

The investigation established the following:

1. A hard reset can remove a commit from the current branch history without immediately deleting its underlying Git objects.
2. Reflogs preserve references to previous HEAD positions and can help locate commits that are no longer part of branch history.
3. Git commits reference trees, and trees reference blobs containing file contents.
4. `git cat-file` allows direct inspection of Git objects without checking out their contents.
5. `git ls-tree -r` recursively lists files and their corresponding blob object IDs.
6. `git fsck --unreachable` identifies objects unreachable from its selected reference roots, including reflog references by default.
7. `git fsck --no-reflogs --unreachable` excludes reflog references when calculating reachability.
8. `git cherry-pick` can restore the changes from a recovered commit while creating a new commit with a different SHA.

## Conclusion

The lost deployment metadata implementation was successfully reconstructed and recovered using Git's reflog and object database.

The investigation demonstrated that Git retains valuable historical evidence beyond the visible branch history. By combining reflog inspection, object inspection, reachability analysis, and commit recovery, previously lost work can be restored without manually recreating the original implementation.

## Validation Status

- [x] Baseline implementation and tests established.
- [x] Deployment metadata implementation committed.
- [x] Commit removed from current branch history.
- [x] Lost commit located using reflog.
- [x] Commit, tree, and blob objects inspected.
- [x] Unreachable objects identified using `git fsck`.
- [x] Lost commit recovered using `git cherry-pick`.
- [x] Recovered implementation and tests verified.

