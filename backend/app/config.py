import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "prod")


# main.py
ALLOWED_ORIGINS = (
    ["*"] if ENVIRONMENT == "dev" else ["http://localhost:8000"]
)  # TODO: update prod origins

DOCS_URL = "/docs" if ENVIRONMENT == "dev" else None
REDOC_URL = "/redoc" if ENVIRONMENT == "dev" else None
