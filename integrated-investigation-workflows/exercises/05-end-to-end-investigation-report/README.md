# Exercise 5: End-to-End Investigation Report

## Scenario

A checkout application was refactored to extract shipping calculations into a dedicated utility module. Independently, another branch introduced tax calculation support.

Both branches were integrated through a Git merge. During manual conflict resolution, the resulting implementation introduced a production regression: shipping charges were excluded from the taxable amount.

The investigation combines Git history analysis, regression detection, merge investigation, historical code reconstruction, code attribution, and commit recovery into one end-to-end workflow.

## Learning Objectives

By completing this exercise, you will learn how to:

- Investigate a regression across divergent Git branches.
- Identify a merge commit that introduced a defect.
- Use `git bisect` to identify the first bad revision.
- Inspect merge ancestry and conflict resolution.
- Use `git show --remerge-diff` to investigate manual merge resolutions.
- Reconstruct historical implementations using `git log` and `git show`.
- Attribute faulty code using `git blame`.
- Recover a lost commit using `git reflog` and `git cherry-pick`.
- Produce an evidence-backed investigation report.

## Repository Structure

```text
05-end-to-end-investigation-report/
+-- README.md
+-- application.py
+-- shipping_utils.py
+-- test_checkout.py
```

## Initial Implementation

The original checkout implementation calculated shipping directly inside `application.py`.

The order total was calculated as:

```python
subtotal = price * quantity
shipping = calculate_shipping(weight, distance)
return round(subtotal + shipping, 2)
```

The baseline test used:

- Price: 100
- Quantity: 2
- Weight: 2
- Distance: 10

Expected order total:

```text
Subtotal = 200.00
Shipping = (2 * 1.5) + (10 * 0.25)
Shipping = 5.50

Order total = 205.50
```

## Branch Development

Two independent changes were developed from the baseline commit.

### Branch 1: Shipping Refactor

Commit:

`f806642 refactor: extract shipping calculation utility`

The shipping calculation was extracted from `application.py` into `shipping_utils.py`.

The original function:

```python
def calculate_shipping(weight, distance):
    weight_cost = weight * 1.5
    distance_cost = distance * 0.25
    return weight_cost + distance_cost
```

Became:

```python
def estimate_shipping(weight, distance):
    weight_cost = weight * 1.5
    distance_cost = distance * 0.25
    return weight_cost + distance_cost
```

The calculation itself remained unchanged.

### Branch 2: Tax Calculation

Commit:

`39c4919 feat: add order tax calculation`

Tax calculation was introduced independently.

The implementation correctly calculated tax on the complete taxable amount:

```python
subtotal = price * quantity
shipping = calculate_shipping(weight, distance)
taxable_total = subtotal + shipping
tax = calculate_tax(taxable_total, tax_rate)

return round(taxable_total + tax, 2)
```

For a 10% tax rate:

```text
Subtotal = 200.00
Shipping = 5.50
Taxable amount = 205.50
Tax = 20.55

Expected total = 226.05
```

Both branches passed their respective tests before integration.

## Merge Integration

The branches were merged into:

`0718690 merge: integrate tax and shipping refactor`

The merge produced conflicts in:

- `application.py`
- `test_checkout.py`

The conflicts were resolved manually.

The resulting implementation was:

```python
from shipping_utils import estimate_shipping


def calculate_tax(amount, tax_rate):
    return amount * tax_rate


def calculate_order_total(price, quantity, weight, distance, tax_rate=0):
    subtotal = price * quantity
    shipping = estimate_shipping(weight, distance)
    tax = calculate_tax(subtotal, tax_rate)
    return round(subtotal + shipping + tax, 2)
```

This implementation introduced the regression because tax was calculated using `subtotal` rather than `subtotal + shipping`.

## Investigation 1: Verify Merge Ancestry

Command:

```bash
git rev-list --parents -n 1 0718690
```

Result:

```text
0718690 f806642 39c4919
```

The merge commit has two parents:

- First parent: `f806642` - shipping refactor.
- Second parent: `39c4919` - tax calculation.

This establishes the two independent development histories integrated by the merge.

Inspect the merge metadata:

```bash
git show --format=fuller --no-patch 0718690
```

Inspect the merge changeset:

```bash
git show --stat --oneline 0718690
```

The merge modified two files:

- `application.py`
- `test_checkout.py`

## Investigation 2: Reproduce the Regression

Command:

```powershell
python .\integrated-investigation-workflows\exercises\05-end-to-end-investigation-report\test_checkout.py
```

Observed result:

```text
AssertionError: Expected 226.05, got 225.5
```

The difference is:

```text
226.05 - 225.50 = 0.55
```

The missing amount is exactly 10% of the shipping charge:

```text
5.50 * 0.10 = 0.55
```

This indicates that shipping was excluded from the taxable amount.

## Investigation 3: Identify the First Bad Commit

Git bisect was used to investigate the regression.

Start bisect by marking the merge commit as bad and both parent commits as good:

```bash
git bisect start 0718690 f806642 39c4919
```

Run the checkout tests automatically:

```powershell
git bisect run python .\integrated-investigation-workflows\exercises\05-end-to-end-investigation-report\test_checkout.py
```

Observed result:

```text
0718690 is the first bad commit
bisect found first 'bad' commit
```

This establishes that:

- The shipping refactor branch was good.
- The tax calculation branch was good.
- The integrated merge commit was bad.

The regression was introduced during integration.

Exit bisect mode:

```bash
git bisect reset
```

## Investigation 4: Inspect the Merge Resolution

Command:

```bash
git show --remerge-diff 0718690 -- integrated-investigation-workflows/exercises/05-end-to-end-investigation-report/application.py
```

The reconstructed merge conflict exposed the difference between the competing implementations and the manual resolution.

The faulty resolution:

```python
shipping = estimate_shipping(weight, distance)
tax = calculate_tax(subtotal, tax_rate)
return round(subtotal + shipping + tax, 2)
```

The correct tax calculation:

```python
taxable_total = subtotal + shipping
tax = calculate_tax(taxable_total, tax_rate)
return round(taxable_total + tax, 2)
```

The manual resolution preserved the shipping refactor but failed to include shipping in the taxable amount.

This is the direct evidence of the merge-introduced defect.

## Investigation 5: Attribute the Faulty Code

Command:

```bash
git blame -L 7,13 0718690 -- integrated-investigation-workflows/exercises/05-end-to-end-investigation-report/application.py
```

Relevant output:

```text
39c4919  def calculate_order_total(...)
dff1648      subtotal = price * quantity
f806642      shipping = estimate_shipping(weight, distance)
0718690      tax = calculate_tax(subtotal, tax_rate)
0718690      return round(subtotal + shipping + tax, 2)
```

The faulty tax calculation and return expression are attributed to the merge commit `0718690`.

This supports the conclusion from bisect and merge-diff investigation.

## Investigation 6: Reconstruct Historical Shipping Code

Inspect the application at the baseline commit:

```bash
git show dff1648:integrated-investigation-workflows/exercises/05-end-to-end-investigation-report/application.py
```

Inspect the extracted shipping utility:

```bash
git show f806642:integrated-investigation-workflows/exercises/05-end-to-end-investigation-report/shipping_utils.py
```

Inspect application history:

```bash
git log --oneline --follow -- integrated-investigation-workflows/exercises/05-end-to-end-investigation-report/application.py
```

Inspect utility history:

```bash
git log --oneline --follow -- integrated-investigation-workflows/exercises/05-end-to-end-investigation-report/shipping_utils.py
```

The original shipping function and extracted utility use identical formulas:

```python
weight_cost = weight * 1.5
distance_cost = distance * 0.25
```

The shipping refactor did not introduce the regression.

The defect was isolated to the tax integration performed during merge resolution.

## Root Cause

The merge resolution calculated tax on the order subtotal alone:

```python
tax = calculate_tax(subtotal, tax_rate)
```

It should have calculated tax on the subtotal plus shipping:

```python
taxable_total = subtotal + shipping
tax = calculate_tax(taxable_total, tax_rate)
```

The merge introduced a regression by omitting shipping from the taxable amount.

## Corrective Fix

The implementation was corrected:

```python
def calculate_order_total(price, quantity, weight, distance, tax_rate=0):
    subtotal = price * quantity
    shipping = estimate_shipping(weight, distance)
    taxable_total = subtotal + shipping
    tax = calculate_tax(taxable_total, tax_rate)
    return round(taxable_total + tax, 2)
```

Fix commit:

`9867bfa fix: include shipping in taxable order total`

The checkout tests passed after the correction.

## Investigation 7: Recover a Lost Fix Commit

To demonstrate repository forensics, the fix commit was deliberately removed from the branch tip.

First, verify the working tree:

```bash
git status -sb
```

Simulate accidental loss:

```bash
git reset --hard HEAD~1
```

Inspect recent history:

```bash
git log --oneline -5
```

The fix commit was no longer part of the current branch history.

Inspect the reflog:

```bash
git reflog --oneline -5
```

The reflog revealed the original fix commit:

```text
9867bfa HEAD@{1}: commit: fix: include shipping in taxable order total
```

Recover the lost commit:

```bash
git cherry-pick 9867bfa
```

Recovery created:

`f775d53 fix: include shipping in taxable order total`

The recovered commit restored the corrective implementation.

This demonstrates that a commit removed from the current branch history may still be recoverable through the reflog.

## Final Verification

Run the checkout tests:

```powershell
python .\integrated-investigation-workflows\exercises\05-end-to-end-investigation-report\test_checkout.py
```

Observed result after recovery:

```text
PASS: checkout tests are correct
```

Final commit history:

```text
f775d53 fix: include shipping in taxable order total
0718690 merge: integrate tax and shipping refactor
39c4919 feat: add order tax calculation
f806642 refactor: extract shipping calculation utility
dff1648 test: add end-to-end investigation baseline
```

The original fix commit `9867bfa` was recovered as a new commit `f775d53` through cherry-pick.

## Final Investigation Report

| Investigation Area | Finding |
|---|---|
| Regression | Tax calculation excluded shipping |
| Expected result | 226.05 |
| Actual result | 225.50 |
| First bad commit | `0718690` |
| Merge parents | `f806642`, `39c4919` |
| Merge investigation | `git show --remerge-diff` |
| Code attribution | `git blame` |
| Historical reconstruction | `git log --follow`, `git show` |
| Root cause | Tax calculated on subtotal only |
| Corrective fix | Include shipping in taxable amount |
| Original fix commit | `9867bfa` |
| Recovery method | `git reflog` and `git cherry-pick` |
| Recovered commit | `f775d53` |
| Final test result | PASS |

## Conclusion

This exercise demonstrates an end-to-end Git investigation involving divergent development histories, a merge-introduced regression, historical code reconstruction, code attribution, and recovery of a lost corrective commit.

The investigation used Git history and repository evidence to identify not only which commit introduced the defect, but also how the manual conflict resolution caused it.

The final implementation was corrected, the lost fix was recovered, and the checkout tests passed.
