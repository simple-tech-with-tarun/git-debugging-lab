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
    assert application.get_deployment_status() == "ready"


def test_deployment_region():
    assert application.get_deployment_region() == "ap-south-1"


def test_deployment_metadata():
    expected = {
        "status": "ready",
        "region": "ap-south-1",
    }

    assert application.get_deployment_metadata() == expected


if __name__ == "__main__":
    test_deployment_status()
    test_deployment_region()
    test_deployment_metadata()
    print("PASS: deployment recovery tests are correct")
