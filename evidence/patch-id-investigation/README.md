# Git Patch ID Investigation

## Objective

This exercise demonstrates how Git uses patch IDs to identify equivalent changes introduced by different commits.

The investigation creates the same code change independently on two branches, compares the resulting commit hashes and patch IDs, and uses `git cherry` to identify equivalent patches across branches.

## Investigation Scenario

Two developers independently introduce the same functionality in separate branches.

Although both commits contain the same code change, they have different commit hashes because their commit messages and commit metadata differ.

The objective is to determine whether the commits introduce equivalent patches without relying only on their commit hashes.

## 1. Create the First Patch

On branch `exercise/patch-id-investigation`, the following function was added to `app.py`:

```python
def get_release_channel():
    return "stable"
```

The change was committed:

```text
aa7303b feat: add release channel helper
```

## 2. Create an Independent Duplicate Patch

A second branch was created from the original base commit:

```powershell
git switch -c exercise/patch-id-duplicate HEAD~1
```

The same function was independently added to `app.py`:

```python
def get_release_channel():
    return "stable"
```

The change was committed with a different commit message:

```text
0b68578 feat: expose stable release channel
```

Both commits introduced the same four-line addition, but their commit hashes were different.

## 3. Compare Patch IDs

The patch ID for each commit was calculated using:

```powershell
git show aa7303b --pretty=format: --patch | git patch-id --stable
git show 0b68578 --pretty=format: --patch | git patch-id --stable
```

Both commands produced the same patch ID:

```text
a8b827aaa28d8120a62743aa6b2b3da61ab6b7e1 0000000000000000000000000000000000000000
```

### Results

| Attribute | First Commit | Second Commit |
|---|---|---|
| Branch | exercise/patch-id-investigation | exercise/patch-id-duplicate |
| Commit hash | aa7303b | 0b68578 |
| Commit message | feat: add release channel helper | feat: expose stable release channel |
| Patch ID | a8b827aaa28d8120a62743aa6b2b3da61ab6b7e1 | a8b827aaa28d8120a62743aa6b2b3da61ab6b7e1 |

The matching patch IDs demonstrate that Git considers the changes equivalent, despite the different commit hashes.

## 4. Investigate Equivalent Patches with git cherry

After switching back to the first branch, the following command was executed:

```powershell
git cherry exercise/patch-id-investigation exercise/patch-id-duplicate
```

Output:

```text
- 0b68578c202449277141f302f28a6826df9141b0
```

### Interpretation

The `-` prefix indicates that an equivalent patch already exists in the current branch.

The `+` prefix would indicate that no equivalent patch was found in the current branch.

This demonstrates how `git cherry` uses patch equivalence to identify changes that have already been applied, even when commit hashes differ.

## 5. Verify the Commit History

The commit graph was inspected using:

```powershell
git log --graph --oneline --decorate --all -5
```

Observed history:

```text
* 0b68578 (exercise/patch-id-duplicate) feat: expose stable release channel
| * aa7303b (HEAD -> exercise/patch-id-investigation) feat: add release channel helper
|/
*   c1df342 (origin/main, origin/HEAD, main) Merge pull request #4 from simple-tech-with-tarun/exercise/reflog-recovery
```

The graph confirms that both commits were created independently from the same base commit.

## 6. Key Learnings

- Commit hashes identify complete commit objects, including their metadata and parent references.
- Patch IDs provide a way to identify equivalent changes independently of commit identity.
- Different commits can produce the same patch ID when they introduce equivalent changes.
- `git patch-id --stable` calculates a stable patch identifier from a patch.
- `git cherry` uses patch equivalence to identify changes that are already represented in another branch.
- Patch IDs are useful when investigating cherry-picks, duplicated changes, and independently applied patches.

## 7. Important Limitations

A matching patch ID does not mean two commits are identical.

Patch IDs represent patch content rather than complete commit history. They do not establish that two commits have the same parent, metadata, surrounding code context, or resulting repository state.

Patch ID comparison is a practical investigation technique, not a substitute for reviewing the actual commits and repository history.

### Rebase and Cherry-Pick Effects on Commit Identity

Rebase and cherry-pick can reproduce an existing change in a different commit.

- A cherry-pick creates a new commit with a different commit hash because the new commit has different parent and committer information.
- A rebase recreates commits on a new base, changing their parent relationships and normally producing new commit hashes.
- Even when the resulting changes are equivalent, patch IDs can remain the same.
- Patch ID comparison helps identify equivalent changes across rewritten histories, but it does not prove that the resulting repository states are identical.

Commit identity and patch equivalence must therefore be investigated separately.

## Conclusion

The investigation successfully demonstrated how Git identifies equivalent patches across independently created commits.

Two commits with different hashes produced the same stable patch ID, and `git cherry` identified the duplicate change.

This technique is useful for repository forensics, duplicate change investigation, cherry-pick verification, and historical code analysis.

**Investigation Result:** Successful
