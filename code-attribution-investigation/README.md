# Code Attribution and Historical Investigation

## Overview

This exercise explores advanced Git history investigation techniques used to identify code authorship, trace changes across file modifications and renames, investigate historical implementations, and understand individual contributions.

The objective is to move beyond basic commit history inspection and develop practical skills for understanding how code evolved, who introduced specific changes, and when those changes occurred.

## Learning Objectives

- Attribute individual lines of code to historical commits.
- Investigate moved and copied code across files.
- Identify changes while ignoring whitespace modifications.
- Search commit history using exact strings and regular expressions.
- Trace file history across renames.
- Retrieve files from historical commits.
- Investigate repository contributions by author.
- Customize Git history output for forensic analysis.

## 1. Code Attribution with Git Blame

`git blame` identifies the commit and author responsible for each line of a file.

### Basic usage

```bash
git blame application.py
```

Displays line-by-line attribution for the entire file.

### Inspect specific line ranges

```bash
git blame -L 5,7 application.py
```

Limits attribution to lines 5 through 7.

### Locate a function by name

```bash
git blame -L :apply_discount application.py
```

Uses a function name to select the relevant section.

### Detect moved lines

```bash
git blame -M application.py
```

Detects lines that were moved or copied within the same file and attempts to identify their earlier origin.

### Detect copied code

```bash
git blame -C pricing_utils.py
git blame -C -C pricing_utils.py
git blame -C -C -C pricing_utils.py
```

Searches for lines copied from other files. Repeating `-C` expands the search to include older commits, helping Git trace copied code back to its original source.

In this exercise, double `-C` successfully traced the copied `calculate_total()` function in `invoice_utils.py` back to its original implementation in `application.py`.

The copy-detection experiment was originally performed when the utility file was named `invoice_utils.py`. The file was subsequently renamed to `pricing_utils.py`.

### Ignore whitespace changes

```bash
git blame -w application.py
```

Ignores whitespace-only modifications when determining line attribution.

### Combine attribution options

```bash
git blame -w -M -L 10,11 application.py
```

Combines whitespace ignoring, moved-line detection, and line-range selection.

This was demonstrated using an intentional whitespace modification and a previous function movement.

## 2. Historical String and Pattern Searches

Git provides two useful options for searching commit history based on changes to file contents.

### Search using -S

```bash
git log --oneline -S"discount_amount" -- application.py
```

The `-S` option searches for commits where the number of occurrences of an exact string changes.

To inspect the corresponding changes:

```bash
git log -p -S"discount_amount" -- application.py
```

### Search using -G

```bash
git log --oneline -G"total.*discount" -- application.py
```

The `-G` option searches added and removed lines using regular expressions.

To inspect matching patches:

```bash
git log -p -G"total.*discount" -- application.py
```

### Comparing -S and -G

| Feature | -S | -G |
|---|---|---|
| Search method | Exact string | Regular expression |
| Matching criteria | Changes in occurrence count | Added or removed lines matching the expression |
| Typical use | Find when a string was introduced or removed | Find commits changing lines matching a pattern |

### Practical demonstration

The multiplication operands in the discount calculation were reversed:

```python
# Previous implementation
discount_amount = total * discount

# Updated implementation
discount_amount = discount * total
```

The occurrence count of `discount_amount` remained unchanged.

Consequently:

```bash
git log --oneline -S"discount_amount" -- application.py
```

did not identify the operand-reversal commit.

However:

```bash
git log --oneline -G"total \* discount" -- application.py
```

identified the commit because the removed line matched the regular expression.

The multiplication operator was escaped using `\*` because `*` has a special meaning in regular expressions.

## 3. File Rename Investigation

Git can detect file renames when comparing repository snapshots.

### Rename a file

```bash
git mv invoice_utils.py pricing_utils.py
git commit -m "refactor: rename invoice utility module"
```

### Inspect history without following renames

```bash
git log --oneline -- pricing_utils.py
```

This displays history associated with the current file path.

### Follow file history across renames

```bash
git log --follow --oneline -- pricing_utils.py
```

The `--follow` option allows Git to trace a file's history across detected renames.

### Practical demonstration

The exercise demonstrated that:

- `git log -- pricing_utils.py` showed only the rename commit.
- `git log --follow -- pricing_utils.py` also showed the earlier commit that created `invoice_utils.py`.

The rename was detected with 100% similarity because the file contents were unchanged.

## 4. Historical File Retrieval

Git allows individual files to be retrieved directly from historical commits without checking out another branch or modifying the working directory.

### Retrieve a file before a rename

```bash
git show 81cde3f:invoice_utils.py
```

This retrieves `invoice_utils.py` from commit `81cde3f`.

### Retrieve the renamed file

```bash
git show d43c690:pricing_utils.py
```

This retrieves the file under its new name from commit `d43c690`.

### Inspect commit changes

```bash
git show -p 81cde3f
git show -p d43c690
```

The `-p` option displays the patch associated with the commit.

This exercise demonstrated that historical file paths must match the repository snapshot being inspected.

## 5. Contribution Investigation

Git provides commands to summarize contributions and investigate individual authors.

### Summarize commits by author

```bash
git shortlog -s -n --all
```

Options:

| Option | Description |
|---|---|
| `-s` | Summary mode; displays commit counts |
| `-n` | Sorts by commit count |
| `--all` | Includes commits reachable from all references under `refs/` |

### Display commit subjects grouped by author

```bash
git shortlog --all
```

Displays commit subjects grouped by author.

### Investigate a specific revision

```bash
git shortlog -s -n HEAD
git shortlog -s -n 81cde3f
```

The first summarizes commits reachable from the current branch. The second summarizes commits reachable from the specified historical commit.

When no revision is supplied, `git shortlog` defaults to `HEAD`.

### Filter commits by author

```bash
git log --author="Tarun Bansal" --oneline
```

Displays commits matching the specified author.

### Customize commit history output

```bash
git log --all --format="%h | %an | %ad | %s" --date=short
```

Useful formatting placeholders:

| Placeholder | Description |
|---|---|
| `%H` | Full commit hash |
| `%h` | Abbreviated commit hash |
| `%an` | Author name |
| `%ae` | Author email |
| `%cn` | Committer name |
| `%ce` | Committer email |
| `%ad` | Author date |
| `%cd` | Committer date |
| `%s` | Commit subject |
| `%b` | Commit message body |

### Author and committer

Git records both an author and a committer for each commit.

- **Author:** The person who originally created the change.
- **Committer:** The person who applied or recorded the commit in the repository.

These identities can differ, for example, when a change is created by one developer and later applied by another developer through a patch or cherry-pick.

### Restrict history to a specific file

```bash
git log --all --format="%h | %an | %ad | %s" --date=short -- application.py
```

The `--` separator distinguishes Git options from the file path.

## 6. Key Takeaways

This exercise demonstrates how Git can be used as an investigation tool rather than simply a version-control system.

| Investigation requirement | Git command |
|---|---|
| Identify line authorship | `git blame` |
| Inspect selected lines | `git blame -L` |
| Detect moved lines | `git blame -M` |
| Detect copied code | `git blame -C` |
| Ignore whitespace changes | `git blame -w` |
| Find exact string changes | `git log -S` |
| Search matching changed lines | `git log -G` |
| Trace history across renames | `git log --follow` |
| Retrieve historical file contents | `git show <commit>:<path>` |
| Summarize author contributions | `git shortlog` |
| Filter commits by author | `git log --author` |
| Customize history output | `git log --format` |

## 7. Practical Investigation Lessons

- A line's latest modification does not necessarily identify its original author.
- Moving or copying code can make ordinary blame results misleading.
- Whitespace-only changes can obscure meaningful historical attribution.
- Exact-string searches and regular-expression searches identify different types of changes.
- Rename detection helps trace file history across path changes.
- Commit counts alone do not represent the amount or quality of a developer's contributions.

## Conclusion

Code attribution and historical investigation provide valuable insight into how a repository evolves.

By combining line attribution, historical searches, rename detection, snapshot inspection, and contribution analysis, developers can investigate unexpected code changes, understand historical implementations, and identify the commits responsible for specific behavior.

These techniques are particularly useful during debugging, code reviews, regression investigations, and repository forensics.
