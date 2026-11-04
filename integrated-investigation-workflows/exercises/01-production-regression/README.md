# Production Regression Investigation

## 1. Problem Description

The invoice calculation returned an incorrect total after a discount calculation change.

Input:
- Price: 100
- Quantity: 2
- Discount: 0.10 (10%)

Expected:
- Invoice total: $180.00

Actual:
- Invoice total: $199.80

## 2. Reproduction

Command:

```powershell
python .\integrated-investigation-workflows\exercises\01-production-regression\test_discount.py
```

Failure:

```text
AssertionError: Expected 'Invoice total: $180.00', got 'Invoice total: $199.80'
```

## 3. Historical Investigation

File history:

```powershell
git log --oneline -10 -- .\application.py
```

Relevant commits:

| Commit | Description |
|---|---|
| b6d8d75 | Add production regression baseline test |
| b8a5e9e | Add discount input validation |
| 4b697ee | Extract discount amount calculation |
| 63e0ea6 | Introduce incorrect discount percentage conversion |
| 2edc698 | Correct discount amount calculation |

git show 63e0ea6 -- .\application.py

## 4. Code Attribution

Command:

```powershell
git blame -L 1,8 .\application.py
```

Finding:

Commit `63e0ea6` introduced the faulty calculation:

```python
return (discount / 100) * total
```

The previous implementation was:

```python
return discount * total
```

The application already receives the discount as a fractional value. Dividing it by 100 again caused the defect.

## 5. Regression Detection

Commands:

```powershell
git bisect start
git bisect bad
git bisect good b6d8d75
```

The selected intermediate commit `4b697ee` passed the regression test.

It was marked good:

```powershell
git bisect good
```

Git then identified:

```text
63e0ea6 is the first bad commit
```

This independently confirmed the regression-introducing commit.

The investigation was completed with:

```powershell
git bisect reset
```

## 6. Root Cause

The discount value was interpreted as a whole percentage even though the application contract uses a fractional rate.

For a 10% discount:
- Correct rate: 0.10
- Incorrect converted rate: 0.001

This caused the application to calculate a discount of $0.20 instead of $20.00.

## 7. Resolution and Validation

The calculation was restored to:

```python
return discount * total
```

Fix commit:

`2edc698 fix: correct discount amount calculation`

The regression test passed after the fix:

```text
PASS: discount tests are correct
```

The invalid discount test also passed, confirming that input validation remained intact.

## 8. Conclusion

The regression was introduced by commit `63e0ea6`.

The finding is supported by:
- Historical commit diff.
- Line-level code attribution using `git blame`.
- Regression detection using `git bisect`.
- Reproduction before the fix.
- Successful validation after the fix.

The investigation demonstrates how Git history, code attribution, and automated regression detection can be combined to identify and verify a production defect.
