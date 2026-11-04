import importlib.util
from pathlib import Path

APPLICATION_PATH = Path(__file__).with_name("application.py")

SPEC = importlib.util.spec_from_file_location(
    "recovery_application",
    APPLICATION_PATH,
)
application = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(application)


def test_deployment_status():
    result = application.get_deployment_status()
    expected = "ready"

    assert result == expected, f"Expected {expected!r}, got {result!r}"


if __name__ == "__main__":
    test_deployment_status()
    print("PASS: repository investigation baseline tests are correct")
