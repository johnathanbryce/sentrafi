from datetime import datetime

import typer
import httpx
import keyring  # type: ignore

from ..config import API_BASE_URL, API_VERSION_PREFIX


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
        "  Country code (e.g. CAN, USA, GBR)", default="", show_default=False
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
    currency = typer.prompt("  Currency code (e.g. CAD, USD, EUR)", default="CAD")
    profile_data["currency"] = currency.upper()

    # financial goals
    typer.secho("\n[ Financial Goals ]", fg="blue", bold=True)
    if typer.confirm("  Would you like to set financial goals?", default=True):
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

            while True:
                target_amount = typer.prompt(
                    "    Target amount (numbers only)", default="", show_default=False
                )
                if not target_amount:
                    break
                try:
                    goal["target_amount"] = str(float(target_amount))
                    break
                except ValueError:
                    typer.secho(
                        "    Invalid input. Enter a number (e.g. 15000 or 15000.50).",
                        fg="red",
                    )

            while True:
                deadline = typer.prompt(
                    "    Deadline (YYYY-MM-DD)", default="", show_default=False
                )
                if not deadline:
                    break
                try:
                    datetime.strptime(deadline, "%Y-%m-%d")
                    goal["deadline"] = deadline
                    break
                except ValueError:
                    typer.secho(
                        "    Invalid date. Use YYYY-MM-DD format (e.g. 2027-06-01).",
                        fg="red",
                    )

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
    typer.confirm("  Save profile?", abort=True, default=True)

    token = keyring.get_password("sentrafi", "access_token")
    create_profile_payload = {**profile_data, "financial_goals": goals_data}
    try:
        create_profile_res = httpx.post(
            f"{API_BASE_URL}{API_VERSION_PREFIX}/profile/create",
            json=create_profile_payload,
            headers={"Authorization": f"Bearer {token}"},
        )

        if create_profile_res.status_code == 409:
            typer.secho("\n  This profile already exists in our system.", fg="yellow")
        elif create_profile_res.status_code == 201:
            typer.secho("\n  Profile saved successfully!", fg="green")
        else:
            typer.secho("\n  Profile did not save.", fg="red")
    except httpx.ConnectError:
        typer.secho("\n  Error reaching backend during profile creation.", fg="red")


def profile_edit_command():
    typer.secho("\nEntering Profile Edit.\n", fg="cyan", bold=True)

    token = keyring.get_password("sentrafi", "access_token")

    # check if user is logged in / a real user
    try:
        verify_user = httpx.get(
            f"{API_BASE_URL}{API_VERSION_PREFIX}/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        if verify_user.status_code == 401:
            typer.secho(
                "This account is not recognized by SentraFi. Please login and create an account before editing.",
                fg="red",
            )
            raise typer.Exit()
    except httpx.NetworkError:
        typer.secho("\n  Error reaching SentraFi's backend.", fg="red")
        raise typer.Exit()

    # fetch user details from db & show full profile
    try:
        user_details_res = httpx.get(
            f"{API_BASE_URL}{API_VERSION_PREFIX}/profile/details",
            headers={"Authorization": f"Bearer {token}"},
        )

        if user_details_res.status_code == 404:
            typer.secho(
                "Account not found. No user details are available to edit",
                fg="red",
            )
            raise typer.Exit()

        user_details = user_details_res.json()
    except httpx.NetworkError:
        typer.secho("\n  Error reaching SentraFi's backend.", fg="red")
        raise typer.Exit()

    # display current profile
    typer.secho("\n  --- Current Profile ---\n", fg="green", bold=True)
    for key, value in user_details["profile_details"].items():
        if key == "id":
            continue
        label = key.replace("_", " ").title()
        styled_label = typer.style(f"    {label}: ", fg="cyan")
        styled_value = typer.style(f"{value or '—'}", fg="yellow")
        typer.echo(styled_label + styled_value)

    # display financial goals
    goals = user_details["financial_goals"]
    if goals:
        typer.secho("\n  --- Financial Goals ---\n", fg="green", bold=True)
        for goal in goals:
            line = typer.style(f"    #{goal['priority']}  ", fg="cyan", bold=True)
            line += typer.style(goal["name"], fg="yellow", bold=True)
            if goal["target_amount"]:
                line += typer.style(f"  —  ${goal['target_amount']}", fg="white")
            if goal["deadline"]:
                line += typer.style(f"  —  by {goal['deadline']}", fg="white")
            typer.echo(line)
    else:
        typer.secho("\n  No financial goals set.", fg="yellow")

    typer.confirm("\n  Would you like to edit your profile?", abort=True, default=True)

    typer.secho("\n  What would you like to edit?\n", fg="cyan", bold=True)
    typer.echo("    1. Profession")
    typer.echo("    2. Income (salary + pay frequency)")
    typer.echo("    3. Location (country + province/state)")
    typer.echo("    4. Currency")
    typer.echo("    5. Additional Context")
    typer.echo("    6. Financial Goals")
    typer.echo("")

    # walk through one by one what they want to edit
    while True:
        choices = typer.prompt("  Select sections to edit (e.g. 1,3,6)")
        # rejects input that is not comma separated or restricted to nums 1 -> 6
        selected_edit_items = [
            int(c.strip())
            for c in choices.split(",")
            if c.strip().isdigit() and 1 <= int(c.strip()) <= 6
        ]
        if selected_edit_items:
            break
        typer.secho(
            "  Please select numbers between 1-6, separated by commas.", fg="red"
        )

    # prompt user to edit each editable item they select and build new edit obj
    edited_user_details_payload = {}
    for item in selected_edit_items:
        if item == 1:
            profession_update = typer.prompt(
                "  Profession",
                default=user_details["profile_details"]["profession"] or "",
            )
            if profession_update != user_details["profile_details"]["profession"]:
                edited_user_details_payload["profession"] = profession_update

        if item == 2:
            while True:
                salary_update = typer.prompt(
                    "  Annual Salary (numbers only)",
                    default=user_details["profile_details"]["annual_salary"] or "",
                )
                if not salary_update:
                    break
                try:
                    float(salary_update)
                    if str(salary_update) != str(user_details["profile_details"]["annual_salary"]):
                        edited_user_details_payload["annual_salary"] = str(float(salary_update))
                    break
                except ValueError:
                    typer.secho(
                        "  Invalid input. Enter a number (e.g. 75000 or 75000.50).",
                        fg="red",
                    )
            pay_freq_update = typer.prompt(
                "  Pay Frequency (weekly / biweekly / semimonthly / monthly)",
                default=user_details["profile_details"]["pay_frequency"] or "biweekly",
            )
            if pay_freq_update != user_details["profile_details"]["pay_frequency"]:
                edited_user_details_payload["pay_frequency"] = pay_freq_update

        if item == 3:
            country_update = typer.prompt(
                "  Country Code (e.g. CAN, USA, GBR)",
                default=user_details["profile_details"]["country"] or "",
            )
            if country_update != user_details["profile_details"]["country"]:
                edited_user_details_payload["country"] = country_update.upper()
            province_update = typer.prompt(
                "  Province or State",
                default=user_details["profile_details"]["province_or_state"] or "",
            )
            if province_update != user_details["profile_details"]["province_or_state"]:
                edited_user_details_payload["province_or_state"] = province_update

        if item == 4:
            currency_update = typer.prompt(
                "  Currency Code (e.g. CAD, USD, EUR)",
                default=user_details["profile_details"]["currency"] or "CAD",
            )
            if currency_update != user_details["profile_details"]["currency"]:
                edited_user_details_payload["currency"] = currency_update.upper()

        if item == 5:
            context_update = typer.prompt(
                "  Additional Context (max 500 chars)",
                default=user_details["profile_details"]["additional_context"] or "",
            )
            if context_update != user_details["profile_details"]["additional_context"]:
                edited_user_details_payload["additional_context"] = context_update[:500]

        if item == 6:
            edited_goals = []
            for i, goal in enumerate(user_details["financial_goals"]):
                typer.secho(f"\n  Goal #{i+1}", fg="cyan", bold=True)
                name = typer.prompt("    Name", default=goal["name"])
                target = typer.prompt(
                    "    Target Amount", default=goal["target_amount"] or ""
                )
                while True:
                    deadline = typer.prompt(
                        "    Deadline (YYYY-MM-DD)", default=goal["deadline"] or ""
                    )
                    if not deadline:
                        break
                    try:
                        datetime.strptime(deadline, "%Y-%m-%d")
                        break
                    except ValueError:
                        typer.secho(
                            "    Invalid date. Use YYYY-MM-DD format (e.g. 2027-06-01).",
                            fg="red",
                        )
                edited_goals.append(
                    {
                        "name": name,
                        "target_amount": target or None,
                        "priority": goal["priority"],
                        "deadline": deadline or None,
                    }
                )

            edited_user_details_payload["financial_goals"] = edited_goals

    if not edited_user_details_payload:
        typer.secho("\n  No changes detected. Profile was not updated.", fg="yellow")
        return

    # send to api to update
    try:
        update_profile_res = httpx.put(
            f"{API_BASE_URL}{API_VERSION_PREFIX}/profile/update",
            json=edited_user_details_payload,
            headers={"Authorization": f"Bearer {token}"},
        )

        if update_profile_res.status_code == 400:
            typer.secho(
                "\n  There was an error updating your profile, please try again",
                fg="red",
            )
        elif update_profile_res.status_code == 200:
            typer.secho("\n  Profile updated successfully!", fg="green")
        else:
            typer.secho("\n  Profile did not update.", fg="red")
    except httpx.ConnectError:
        typer.secho(
            "\n  Error reaching SentraFi backend during profile update.", fg="red"
        )
