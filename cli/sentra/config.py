import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "prod")

API_BASE_URL = ""
if ENVIRONMENT == "dev":
    API_BASE_URL = "http://localhost:8000"
else:
    API_BASE_URL = ""  # TODO: PROD
