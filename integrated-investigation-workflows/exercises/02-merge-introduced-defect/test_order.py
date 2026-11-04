import importlib.util
from pathlib import Path

APPLICATION_PATH = Path(__file__).with_name("application.py")

SPEC = importlib.util.spec_from_file_location(
    "merge_investigation_application",
    APPLICATION_PATH,
)
application = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(application)

calculate_order_total = application.calculate_order_total


def test_order_total_with_discount():
    result = calculate_order_total(100, 2, 0.10)
    expected = 180.0

    assert result == expected, f"Expected {expected}, got {result}"


def test_tax_is_calculated_after_discount():
    result = calculate_order_total(100, 2, 0.10, 0.10)
    expected = 198.0

    assert result == expected, f"Expected {expected}, got {result}"


if __name__ == "__main__":
    test_order_total_with_discount()
    test_tax_is_calculated_after_discount()
    print("PASS: all order tests are correct")
    