from config import DEFAULT_ENVIRONMENT


def get_application_metadata():
    return {
        "name": "Git Debugging Lab",
        "environment": DEFAULT_ENVIRONMENT,
        "version": "1.0.0",
    }


def get_application_version():
    return "1.0.0"
