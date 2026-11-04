# Historical Code Reconstruction

## Objective

Investigate a shipping-cost regression involving a moved module, a renamed function, and an incorrect calculation change. Reconstruct the implementation history and identify the commit responsible for the defect.

## 1. Initial Implementation

The original implementation was in `application.py`.

```python
def calculate_shipping_cost(weight, distance):
    base_cost = weight * 2
    distance_cost = distance * 0.5
    return base_cost + distance_cost
```

Baseline test:

```powershell
python .\integrated-investigation-workflows\exercises\03-historical-code-reconstruction\test_reconstruction.py
```

Expected result:

```text
PASS: historical reconstruction baseline tests are correct
```

Baseline commit: `eb4f052`

## 2. Code Evolution

| Commit | Change |
|---|---|
| `eb4f052` | Add historical reconstruction baseline |
| `1ff3fb7` | Move shipping calculation into `shipping_utils.py` |
| `92b851a` | Rename `calculate_shipping_cost` to `estimate_shipping_cost` |
| `db78131` | Incorrectly reduce the distance multiplier |
| `9183997` | Restore the original distance multiplier |

The module move preserved the original calculation. The function rename also preserved its behavior.

## 3. Reproducing the Regression

The distance multiplier was changed from `0.5` to `0.05`:

```python
distance_cost = distance * 0.05
```

Running the reconstruction tests produced:

```text
AssertionError: Expected 30.0, got 21.0
```

For weight 10 and distance 20:

- Expected base cost: 10 * 2 = 20
- Expected distance cost: 20 * 0.5 = 10
- Expected shipping cost: 30
- Actual distance cost after the regression: 20 * 0.05 = 1
- Actual shipping cost: 21

## 4. Historical Investigation

### Trace file history

```powershell
git log --follow --find-renames --oneline -- .\integrated-investigation-workflows\exercises\03-historical-code-reconstruction\shipping_utils.py
```

This traced the utility file through its rename and module creation commits. The original implementation in `application.py` was verified separately using `git show eb4f052:<path>`.

### Find the exact faulty change

```powershell
git log --oneline -S "distance * 0.05" --all -- .\integrated-investigation-workflows\exercises\03-historical-code-reconstruction
```

The search identified `db78131`.

### Compare changed lines

```powershell
git log --oneline -G "distance \* 0\.[05]" --all -- .\integrated-investigation-workflows\exercises\03-historical-code-reconstruction
```

This searches changed lines matching the multiplier pattern. It can include earlier commits that introduced matching lines, so its results need interpretation.

### Attribute the current implementation

```powershell
git blame -L 1,5 .\integrated-investigation-workflows\exercises\03-historical-code-reconstruction\shipping_utils.py
```

The output attributed the incorrect multiplier to `db78131`.

### Inspect the introducing commit

```powershell
git show db78131 -- .\integrated-investigation-workflows\exercises\03-historical-code-reconstruction\shipping_utils.py
```

The diff confirmed the exact change:

```diff
-    distance_cost = distance * 0.5
+    distance_cost = distance * 0.05
```

### Trace moved and copied code

```powershell
git blame -M -C -C -L 1,4 -- .\integrated-investigation-workflows\exercises\03-historical-code-reconstruction\shipping_utils.py
```

The calculation lines were attributed to `1ff3fb7`, while the renamed function definition was attributed to `92b851a`. The faulty multiplier remained attributed to `db78131`.

### Retrieve the original implementation

```powershell
git show eb4f052:integrated-investigation-workflows/exercises/03-historical-code-reconstruction/application.py
```

This recovered the original implementation before the module move and confirmed that the original multiplier was `0.5`.

## 5. Root Cause

The distance multiplier was unintentionally reduced from `0.5` to `0.05` in commit `db78131`.

This caused the distance component of the shipping cost to be underestimated by a factor of ten.

The defect was introduced by a direct calculation change, not by the module move or function rename.

## 6. Fix and Validation

Restored the original calculation:

```python
distance_cost = distance * 0.5
```

Fix commit: `9183997`

Ran the reconstruction tests again:

```powershell
python .\integrated-investigation-workflows\exercises\03-historical-code-reconstruction\test_reconstruction.py
```

Result:

```text
PASS: historical reconstruction tests are correct
```

## 7. Investigation Conclusion

The investigation established the implementation's evolution from its original location through a module move and function rename, then identified the exact commit that introduced the incorrect multiplier.

Evidence included:

- File history using `git log --follow`.
- Exact string and regex searches using `git log -S` and `git log -G`.
- Line attribution using `git blame` and `git blame -M -C -C`.
- Commit-level diff inspection using `git show`.
- Historical source retrieval using `git show <commit>:<path>`.
- Test failure before the fix and successful validation afterward.

The original implementation and the regression were independently verified using repository history and executable tests.
