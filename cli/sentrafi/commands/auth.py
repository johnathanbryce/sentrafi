import typer
import httpx
import keyring  # type: ignore (backend venv activated as primary interpreter)

from ..config import API_BASE_URL, API_VERSION_PREFIX, OLLAMA_URL


def login_command():
    user_email = typer.prompt("Enter email:")
    user_password = typer.prompt("Enter password:", hide_input=True)
    user_data = {"email": user_email, "password": user_password}

    # login user and store access token in keyring
    login_res = httpx.post(f"{API_BASE_URL}{API_VERSION_PREFIX}/login", json=user_data)

    if login_res.status_code == 200:
        user_access_token = login_res.json()["access_token"]

        # store in keyring
        keyring.set_password("sentrafi", "access_token", user_access_token)
        typer.secho("Login successful.", fg="green")

    elif login_res.status_code == 401:
        detail = login_res.json()["detail"]
        if detail == "User does not exist. Please register.":
            typer.secho(
                "This email does not exist, please use either 'sentra init' to create a SentraFi account",
                fg="red",
            )
        elif detail == "Incorrect password.":
            typer.secho("Incorrect password. Please try again.", fg="yellow")
        raise typer.Exit(code=1)

    else:
        typer.secho("Login failed. Please try again.", fg="red")
        raise typer.Exit(code=1)
