import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "prod")


API_BASE_URL = (
    "http://localhost:8000" if ENVIRONMENT == "dev" else ""
)  # TODO: update prod api

API_VERSION_PREFIX = "/api/v1"

KEYCHAIN_SERVICE = "sentrafi"
