import os
from dotenv import load_dotenv

# load local .env vars
load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT", "prod")


API_BASE_URL = (
    "http://localhost:8000" if ENVIRONMENT == "dev" else ""
)  # TODO: update prod api

API_VERSION_PREFIX = "/api/v1"

OLLAMA_URL = "http://localhost:11434"


KEYCHAIN_SERVICE = "sentrafi"
