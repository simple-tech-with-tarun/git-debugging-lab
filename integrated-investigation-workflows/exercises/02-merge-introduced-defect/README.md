# Merge-Introduced Defect Investigation

## 1. Problem Description

Two independent branches introduced changes to order processing:

- `feature/tax-calculation`: added optional tax calculation.
- `feature/order-total-refactor`: extracted discounted subtotal calculation.

Both changes were integrated through a merge commit. The resulting implementation calculated tax using the original subtotal instead of the discounted subtotal.

## 2. Reproduction

Test command:

```powershell
python .\integrated-investigation-workflows\exercises\02-merge-introduced-defect\test_order.py
```

Input:

- Price: 100
- Quantity: 2
- Discount: 10%
- Tax rate: 10%

Expected calculation:

- Original subtotal: 200
- Discounted subtotal: 180
- Tax: 18
- Expected total: 198

Actual calculation before the fix:

- Tax was calculated on 200, producing 20.
- Actual total: 200

The tax test failed with:

```text
AssertionError: Expected 198.0, got 200.0
```

## 3. Branch and Merge History

| Commit | Description |
|---|---|
| `bc4b53b` | Add merge investigation baseline |
| `e8c8449` | Extract discounted subtotal calculation |
| `8a6fd1d` | Add order tax calculation helper |
| `b41a8fa` | Apply optional tax to order total |
| `feac297` | Merge tax calculation and order refactor |
| `e3bb81d` | Correct tax calculation after discount |

The merge commit has two parents:

- First parent: `e8c8449`
- Second parent: `b41a8fa`

## 4. Investigation Commands and Evidence

### Inspect full history

```powershell
git log --oneline --graph --all -12
```

This exposed both feature branches and their integration through `feac297`.

### Inspect merge parents

```powershell
git rev-list --parents -n 1 feac297
git show --no-patch --pretty=raw feac297
```

Both commands confirmed the two-parent merge structure.

### Compare first-parent and full history

```powershell
git log --first-parent --oneline -8
git log --oneline --graph --all -12
```

First-parent history showed the main integration line. Full history exposed commits from both contributing branches.

### Inspect combined merge changes

```powershell
git show --cc feac297 -- .\integrated-investigation-workflows\exercises\02-merge-introduced-defect\application.py
```

This exposed the conflicting implementations and the committed resolution.

### Inspect the merge resolution

```powershell
git show --remerge-diff feac297 -- .\integrated-investigation-workflows\exercises\02-merge-introduced-defect\application.py
```

The reconstructed automatic merge contained:

```python
tax = calculate_tax(discounted_subtotal, tax_rate)
```

The committed merge resolution instead contained:

```python
tax = calculate_tax(subtotal, tax_rate)
```

This established that the incorrect tax input was introduced during manual conflict resolution.

### Compare the merge against its first parent

```powershell
git diff feac297^1 feac297 -- .\integrated-investigation-workflows\exercises\02-merge-introduced-defect\application.py
```

This showed the changes introduced on the first-parent integration line by the merge.

## 5. Root Cause

The merge combined two independent changes:

- A refactor that extracted discounted subtotal calculation.
- A tax feature that calculated tax on the discounted subtotal.

During conflict resolution, the tax calculation was changed to use the original subtotal:

```python
tax = calculate_tax(subtotal, tax_rate)
```

The correct implementation is:

```python
tax = calculate_tax(discounted_subtotal, tax_rate)
```

The defect was introduced by the merge resolution, not by Git's automatic merge algorithm.

## 6. Fix and Validation

The implementation was corrected in commit `e3bb81d`.

The test runner was updated to report success after both tests complete.

Final test command:

```powershell
python .\integrated-investigation-workflows\exercises\02-merge-introduced-defect\test_order.py
```

Output:

```text
PASS: all order tests are correct
```

## 7. Conclusion

The investigation combined:

- Full commit graph inspection.
- First-parent history analysis.
- Merge parent and ancestry inspection.
- Combined merge diff analysis.
- Reconstructed merge-resolution inspection.
- Reproduction through a focused test.
- Verification of the corrective change.

The evidence identifies `feac297` as the merge commit containing the defect and `e3bb81d` as the corrective commit.

The investigation demonstrates that a merge can introduce a defect through an incorrect manual conflict resolution even when the contributing implementations are individually designed around the intended behavior.

