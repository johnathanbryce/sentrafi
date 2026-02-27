import typer
import httpx
import keyring

from ..config import API_BASE_URL, API_VERSION_PREFIX, OLLAMA_URL


def init_sentrafi():

    # test  health
    res_health = httpx.get(f"{API_BASE_URL}/health")
    if res_health.json()["status"] == "ok":
        typer.secho(
            "API server running and database connection is successful!", fg="green"
        )
    else:
        typer.secho("API server and database connection failed.", fg="red")
        raise typer.Exit(code=1)

    # test ollama connection
    try:
        ollama_health = httpx.get(f"{OLLAMA_URL}/api/tags")
        ollama_models = [model["name"] for model in ollama_health.json()["models"]]
        typer.secho(
            f"Successfully connected to Ollama with your following models available: {", ".join(ollama_models)}",
            fg="green",
        )
    except:
        typer.secho(
            "Ollama not detected. Without Ollama, the free tier (local, private AI) is unavailable. "
            "You can still use SentraFi with your own API key (BYOK tier), but your data will be sent to a cloud provider.",
            fg="yellow",
        )
        if not typer.confirm("Continue without Ollama?"):
            typer.secho(
                "Run 'sentra init' again after installing Ollama: https://ollama.com",
                fg="yellow",
            )
            raise typer.Exit(code=0)

    # setup account
    typer.echo(
        "Let's setup your SentraFi account... please enter your preferred email and password"
    )
    user_email = typer.prompt("Enter email:")
    user_password = typer.prompt("Enter password:", hide_input=True)
    user_data = {"email": user_email, "password": user_password}
    register_res = httpx.post(
        f"{API_BASE_URL}{API_VERSION_PREFIX}/register", json=user_data
    )
    if register_res.status_code == 201:
        typer.secho(
            f"your SentraFi account successfully has been created: {register_res.json()['email']}",
            fg="green",
        )
    elif register_res.status_code == 409:
        typer.secho(
            "An account with this email already exists. Run 'sentra login' instead.",
            fg="yellow",
        )
        raise typer.Exit(code=0)
    else:
        typer.secho(
            f"Account registration failed: {register_res.json().get('detail', 'Unknown error')}",
            fg="red",
        )
        raise typer.Exit(code=1)

    # login user and store access token in keyring
    login_res = httpx.post(f"{API_BASE_URL}{API_VERSION_PREFIX}/login", json=user_data)
    user_access_token = login_res.json()["access_token"]

    # store in keyring
    keyring.set_password("sentrafi", user_email, user_access_token)

    # verify with /me
    headers = {"Authorization": f"Bearer {user_access_token}"}
    verify_res = httpx.get(f"{API_BASE_URL}{API_VERSION_PREFIX}/me", headers=headers)
    print(verify_res.json())
