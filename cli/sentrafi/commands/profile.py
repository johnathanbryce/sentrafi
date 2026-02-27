import typer
import httpx
import keyring  # type: ignore (backend venv activated as primary interpreter)

from ..config import API_BASE_URL, API_VERSION_PREFIX, OLLAMA_URL


def profile_setup_command():
    typer.secho("\nWelcome to SentraFi profile setup.\n", fg="cyan", bold=True)
    typer.echo(
        "Your profile helps SentraFi provide personalized financial analysis. Understanding\n"
        "your income, location, and currency means more accurate insights on spending,\n"
        "savings targets, and tax implications.\n"
    )
    typer.secho(
        "All fields are optional. Press Enter to skip any you'd prefer not to answer.",
        fg="yellow",
    )
    typer.secho(
        "You can update these later with 'sentra profile --edit'.\n",
        fg="yellow",
    )

    # build user profile details
    profile_data = {}
    goals_data = []

    # profession
    typer.secho("[ Profession ]", fg="blue", bold=True)
    profession = typer.prompt(
        "  Profession / occupation", default="", show_default=False
    )
    if profession:
        profile_data["profession"] = profession

    # income (has to match pydantic model Numeric(12, 2) -- no "$" or "75K")
    typer.secho("\n[ Income ]", fg="blue", bold=True)
    while True:
        annual_salary = typer.prompt(
            "  Annual salary (numbers only, e.g. 75000 or 75000.50)",
            default="",
            show_default=False,
        )
        if not annual_salary:
            break
        try:
            profile_data["annual_salary"] = str(float(annual_salary))
            break
        except ValueError:
            typer.secho(
                "  Invalid input. Enter a number (e.g. 75000 or 75000.50).", fg="red"
            )
    pay_frequency = typer.prompt(
        "  Pay frequency (weekly / biweekly / semimonthly / monthly)",
        default="biweekly",
    )
    profile_data["pay_frequency"] = pay_frequency

    # location
    typer.secho("\n[ Location ]", fg="blue", bold=True)
    country = typer.prompt(
        "  Country code (e.g. USA, CAN, GBR)", default="", show_default=False
    )
    if country:
        profile_data["country"] = country.upper()
    province_or_state = typer.prompt(
        "  Province or state (e.g. British Columbia, Ontario, California)",
        default="",
        show_default=False,
    )
    if province_or_state:
        profile_data["province_or_state"] = province_or_state

    # currency
    typer.secho("\n[ Currency ]", fg="blue", bold=True)
    currency = typer.prompt("  Currency code (e.g. USD, CAD, EUR)", default="CAD")
    profile_data["currency"] = currency.upper()

    # financial goals
    typer.secho("\n[ Financial Goals ]", fg="blue", bold=True)
    typer.echo(
        "  List your financial goals in order of priority (most important first)."
    )
    typer.echo("  Press Enter to skip a goal.\n")

    for i in range(1, 6):
        if i > 3:
            if not typer.confirm(f"  Add goal #{i}?", default=False):
                break

        typer.secho(f"  Goal #{i}", fg="cyan")
        goal_name = typer.prompt(
            "    Name (e.g. Emergency fund, Pay off debt)",
            default="",
            show_default=False,
        )
        if not goal_name:
            if i <= 3:
                continue
            else:
                break

        goal = {"name": goal_name, "priority": i}

        target_amount = typer.prompt(
            "    Target amount", default="", show_default=False
        )
        if target_amount:
            goal["target_amount"] = target_amount

        deadline = typer.prompt(
            "    Deadline (YYYY-MM-DD)", default="", show_default=False
        )
        if deadline:
            goal["deadline"] = deadline

        goals_data.append(goal)
        typer.echo("")

    # additional context
    typer.secho("\n[ Additional Context ]", fg="blue", bold=True)
    typer.echo("  Anything else SentraFi should know about your financial situation?")
    typer.echo(
        "  (e.g. self-employed, rental income, side business, saving for a goal)"
    )
    additional_context = typer.prompt(
        "  Max 500 characters", default="", show_default=False
    )
    if additional_context:
        if len(additional_context) > 500:
            typer.secho(
                f"  Input truncated from {len(additional_context)} to 500 characters.",
                fg="yellow",
            )
        profile_data["additional_context"] = additional_context[:500]

    # update db with profile details

    # show success/summary to user
    typer.secho("\n--- Profile Summary ---\n", fg="green", bold=True)

    if profile_data:
        for key, value in profile_data.items():
            label = key.replace("_", " ").title()
            typer.echo(f"  {label}: {value}")

    if goals_data:
        typer.secho("\n  Financial Goals:", bold=True)
        for goal in goals_data:
            line = f"    #{goal['priority']}  {goal['name']}"
            if "target_amount" in goal:
                line += f"  —  ${goal['target_amount']}"
            if "deadline" in goal:
                line += f"  —  by {goal['deadline']}"
            typer.echo(line)

    if not profile_data and not goals_data:
        typer.secho(
            "  No details provided. You can set these up later with 'sentra profile --edit'.",
            fg="yellow",
        )

    typer.echo("")

    # confirm before saving
    typer.confirm("  Save profile?", abort=True)

    # TODO: POST profile_data and goals_data to backend
    typer.secho("\n  Profile saved successfully!", fg="green")


def profile_edit_command():
    typer.secho("\nEntering Profile Edit.\n", fg="cyan", bold=True)
    typer.echo("\n")  # TODO: enter appropriate edit profile intro message
