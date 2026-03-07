import typer

from .commands.init import init_command
from .commands.auth import login_command
from .commands.profile import (
    profile_setup_command,
    profile_edit_command,
    profile_delete_command,
)

app = typer.Typer()


# tells typer that the app has subcommands so sentra init can function
@app.callback()
def main():
    pass


@app.command()
def init():
    init_command()


@app.command()
def login():
    login_command()


@app.command()
def profile(
    setup: bool = typer.Option(False, "--setup", help="Create your profile"),
    edit: bool = typer.Option(False, "--edit", help="Edit your profile"),
    delete: bool = typer.Option(False, "--delete", help="Delete your profile"),
):
    if setup:
        profile_setup_command()
    elif edit:
        profile_edit_command()
    elif delete:
        profile_delete_command()
    else:
        typer.echo("Please use a profile command: --setup, --edit, or --delete")


if __name__ == "__main__":
    app()
