# Typer API reference — everything you need for sentra init and sentra login:
#
# Core:
#   typer.Typer()                        — create the app instance. Pass help="..." for the top-level --help description
#   @app.command()                       — register a function as a CLI command (e.g., sentra init)
#   @app.callback()                      — runs before any command; use for global setup or top-level --version flag
#
# Output:
#   typer.echo("message")               — print to stdout (preferred over print() for CLI tools)
#   typer.style("text", fg="green")     — color a string (colors: green, red, yellow, blue, magenta, cyan, white)
#   typer.echo(typer.style(...))        — combine them to print colored output
#   typer.secho("text", fg="green")     — shorthand: style + echo in one call
#
# User input:
#   typer.prompt("Email")               — ask user for text input, returns their answer as a string
#   typer.prompt("Password", hide_input=True)  — same but hides what they type (for passwords)
#   typer.confirm("Continue?")          — yes/no prompt, returns True/False
#   typer.confirm("Sure?", abort=True)  — same but auto-exits if they say no
#
# Exit & errors:
#   raise typer.Exit(code=0)            — exit cleanly (code=0 success, code=1 error)
#   raise typer.Abort()                 — abort with "Aborted." message
#
# Arguments & Options (type hints on your function params):
#   name: str                                          — required positional argument
#   name: str = typer.Argument(help="User's name")     — positional arg with help text
#   verbose: bool = typer.Option(False, "--verbose")    — optional flag (--verbose)
#   email: str = typer.Option(..., prompt=True)         — option that prompts if not provided via flag

import typer

app = typer.Typer()

# TODO: remove — test command
@app.command()
def hello(name: str):
    print(f"Hello {name}")
    typer.echo("Testing. Hello world!")


if __name__ == "__main__":
    app()
