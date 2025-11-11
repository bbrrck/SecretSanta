# ruff: noqa: D100

import yagmail

from santify.logging import console
from santify.mapping import Person


def send_email(  # noqa: PLR0913
    sender: str,
    santa: Person,
    santee: Person,
    password: str,
    year: int,
    family_name: str,
    theme: str | None = None,
    budget: int | None = None,
    email_subject_suffix: str = "",
    *,
    debug_mode: bool = True,
) -> None:
    """Send an email to Santa."""
    theme_message = f"Tohtoročná téma je: <strong>{theme}</strong>" if theme else ""
    budget_message = f"Limit na darček: {budget}€. " if budget else ""
    santa_email = sender if debug_mode else santa.email
    santee_name = santee.alias if santee.alias else santee.name

    yag = yagmail.SMTP(sender, password=password)
    yag.send(
        to=santa_email,
        subject=f"{family_name} Secret Santa {year}! 🎄🎅 {email_subject_suffix}",
        contents=f"""Ahoj {santa.name},

Tento rok si Secret Santa pre: <strong>{santee_name}</strong>.

Pšt, nikomu to nehovor! 🤫

{theme_message}

<small>{budget_message}Túto správu poslal Tiborov SecretSantaBot3.0.</small>""",
    )

    console.success(f"Email sent to '{santa.name}' <{santa_email}>")
