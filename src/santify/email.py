# ruff: noqa: D100

import yagmail

from santify.logging import logger
from santify.mapping import Person


def send_email(  # noqa: PLR0913
    sender: str,
    santa: Person,
    santee: Person,
    password: str,
    year: int,
    family_name: str,
    budget: int | None = None,
    *,
    debug_mode: bool = True,
) -> None:
    """Send an email to Santa."""
    budget_message = f"Limit na darček: {budget}€. " if budget else ""
    santa_email = sender if debug_mode else santa.email
    santee_name = santee.alias if santee.alias else santee.name

    yag = yagmail.SMTP(sender, password=password)
    yag.send(
        to=santa_email,
        subject=f"{family_name} Secret Santa {year}! 🎄🎅",
        contents=f"""Ahoj {santa.name},

Tento rok si Secret Santa pre: <strong>{santee_name}</strong>.

Pšt, nikomu to nehovor!

<small>{budget_message}Túto správu poslal Tiborov SecretSantaBot3.0.</small>""",
    )

    msg = f"email sucessfully sent to '{santa.name}' <{santa_email}>"
    logger.info(msg)
