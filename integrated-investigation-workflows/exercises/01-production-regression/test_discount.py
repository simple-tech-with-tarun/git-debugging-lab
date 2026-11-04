import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from application import process_order


def test_discount_calculation():
    result = process_order(100, 2, 0.10)
    expected = "Invoice total: $180.00"

    assert result == expected, f"Expected {expected!r}, got {result!r}"


def test_invalid_discount():
    try:
        process_order(100, 2, 1.5)
    except ValueError as error:
        assert str(error) == "Discount must be between 0 and 1"
        return

    raise AssertionError("Expected ValueError for invalid discount")


if __name__ == "__main__":
    test_discount_calculation()
    test_invalid_discount()
    print("PASS: discount tests are correct")
