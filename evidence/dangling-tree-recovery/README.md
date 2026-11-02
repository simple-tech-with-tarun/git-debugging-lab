Get-Content .\evidence\dangling-tree-recovery\conflict-snapshot\README.md
PS C:\Users\ertar\Documents\GitHub\git-debugging-lab> Get-Content .\evidence\dangling-tree-recovery\conflict-snapshot\README.md
# Dangling Tree Recovery

## Objective

Recover and inspect source files stored in an unreachable Git tree object.

This exercise demonstrates how Git objects can remain available after becoming unreachable from the repository's normal references.

## 1. Discover unreachable objects

Run:

```powershell
git fsck --full --no-reflogs --unreachable
```

The investigation identified:

| Object | SHA |
|---|---|
| Tree | `d3e08fc9fafc7f196cb3b0d42f796df595e7eb83` |
| Blob | `087d32c3c98d1dc54323a4d375b64b6101266616` |

## 2. Inspect the unreachable tree

```powershell
git ls-tree -r d3e08fc9fafc7f196cb3b0d42f796df595e7eb83
```

The tree contained four files:

| File | Blob SHA |
|---|---|
| README.md | `7b1dba218aa0d8a5f3c4803d586954e2e47b101e` |
| app.py | `d11b3470836d1bf11f382dc0f21e00b43128a35e` |
| config.py | `087d32c3c98d1dc54323a4d375b64b6101266616` |
| metadata.py | `80254beffe7533c1e15a9fb041b3079c93ddc4f6` |

## 3. Inspect recovered content

Inspect the conflicting configuration:

```powershell
git cat-file -p 087d32c3c98d1dc54323a4d375b64b6101266616
```

The recovered configuration contained unresolved merge-conflict markers:

```text
    <<<<<<< HEAD
    DEFAULT_ENVIRONMENT = "testing"
    =======
    DEFAULT_ENVIRONMENT = "production"
    >>>>>>> hotfix/application-environment
```

This demonstrates that the recovered tree preserved a snapshot containing an unresolved merge conflict.

## 4. Verify recovered files

The extracted snapshot is stored in:

`conflict-snapshot/`

Verify its contents against the Git blob objects:

```powershell
$files = @("README.md", "app.py", "config.py", "metadata.py")

foreach ($file in $files) {
    git hash-object ".\evidence\dangling-tree-recovery\conflict-snapshot\$file"
}
```

All four resulting hashes matched the blob IDs recorded in the unreachable tree.

## 5. Evidence artifacts

- `conflict-snapshot.zip` â€” original recovery archive.
- `conflict-snapshot/` â€” extracted and verified source snapshot.

The original snapshot is preserved without modifying its contents.

## Key Learnings

- Git stores repository content as objects.
- A tree object records file names, modes and blob references.
- `git fsck` can identify unreachable objects.
- `git ls-tree` reveals the contents of a tree.
- `git cat-file` allows inspection of Git objects.
- `git hash-object` can verify recovered file contents.
- Unreachable does not necessarily mean immediately deleted.
