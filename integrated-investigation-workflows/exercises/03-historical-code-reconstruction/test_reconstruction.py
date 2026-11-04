import importlib.util
from pathlib import Path

APPLICATION_PATH = Path(__file__).with_name("application.py")

SPEC = importlib.util.spec_from_file_location(
    "historical_reconstruction_application",
    APPLICATION_PATH,
)
application = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(application)

calculate_shipping_cost = application.calculate_shipping_cost
process_shipment = application.process_shipment


def test_shipping_cost():
    result = calculate_shipping_cost(10, 20)
    expected = 30.0

    assert result == expected, f"Expected {expected}, got {result}"


def test_process_shipment():
    result = process_shipment(10, 20)
    expected = 30.0

    assert result == expected, f"Expected {expected}, got {result}"


if __name__ == "__main__":
    test_shipping_cost()
    test_process_shipment()
    print("PASS: historical reconstruction baseline tests are correct")
