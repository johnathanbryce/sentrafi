# SentraFi

AI-powered personal finance CLI. Ingest bank statements, track spending against goals, and query your financial data using natural language — all running locally for privacy.

## Requirements

- Python 3.12+
- Docker (Postgres, Redis, FastAPI backend)
- Ollama (local LLM inference)

## Installation

```bash
cd cli
pip install -e .
```

## Usage

```bash
sentra init        # First-time setup: env checks, registration, keychain storage
sentra login       # Authenticate and refresh stored credentials
sentra --help      # Show all available commands
```
