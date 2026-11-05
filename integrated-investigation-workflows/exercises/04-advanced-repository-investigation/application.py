def get_deployment_status():
    return "ready"


def get_deployment_region():
    return "ap-south-1"


def get_deployment_metadata():
    return {
        "status": get_deployment_status(),
        "region": get_deployment_region(),
    }
