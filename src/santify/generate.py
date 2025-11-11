# ruff: noqa: D100

import json
import os
import random
import sys
from pathlib import Path

from cryptography.fernet import Fernet
from dotenv import load_dotenv

from santify.email import send_email as _send_email
from santify.logging import logger
from santify.mapping import (
    Mapping,
    Person,
    generate_constraints_from_past_mapping,
    generate_mapping,
    generate_partner_constraints,
    get_active_santas,
)

_ = load_dotenv()


def generate_mapping_and_send_email(  # noqa: C901, PLR0915
    config_file: Path,
    output_dir: str | None = None,
    *,
    send_email: bool = False,
    encrypt: bool = True,
    debug_mode: bool = True,
) -> None:
    """Generate a mapping of santas to santees and send email to santas.

    Parameters
    ----------
    config_file : Path
        The path to the configuration file.
    output_dir : str, optional
        The path to the output directory.
        Default is None.
    send_email : bool, optional
        Whether to send email to santas.
        Default is False.
    encrypt : bool, optional
        Whether to encrypt the output.
        Default is True.
    debug_mode : bool, optional
        Whether to enable debug mode.
        Default is True.

    Raises
    ------
    RuntimeError
        If the output directory does not exist.

    """
    seed = random.randrange(sys.maxsize)  # noqa: S311
    random.seed(seed)
    logger.info(f"random {seed=}")

    logger.info(f"Reading configuration from {config_file}")
    with config_file.open() as f:
        config = json.load(f)

    # Construct people
    people = []
    for name, person_details in config["people"].items():
        person_details["name"] = name
        person = Person(**person_details)
        people.append(person)

    logger.info(f"Number of people: {len(people)}")
    logger.info(", ".join([x.name for x in people]))

    # Get active santas
    santas = get_active_santas(people)
    santas_by_name = {santa.name: santa for santa in santas}

    logger.info(f"Number of santas (active people): {len(santas)}")
    logger.info(", ".join([x.name for x in santas]))

    # Construct past mappings
    past_mappings = []
    for year, mapping in config["previous"].items():
        m = Mapping(year=year, mapping=mapping)
        past_mappings.append(m)

    name_mapping = config.get("name_mapping")

    # Generate constraints
    # -- partner constraints
    constraints = generate_partner_constraints(santas)
    # -- past mapping constraints
    for pm in past_mappings:
        constraints += generate_constraints_from_past_mapping(pm, name_mapping)

    # Generate mapping
    name_mapping = generate_mapping(
        santas=santas,
        constraints=constraints,
        year=config["year"],
    )

    if debug_mode:
        logger.info(f"DEBUG MODE: Generated mapping:\n{name_mapping}")

    if send_email:

        def get_env_var_or_die(var_name: str) -> str:
            """Get the value of an environment variable."""
            value = os.getenv(var_name)
            if value is None:
                msg = f"{var_name} environment variable is not set"
                logger.error(msg)
                raise RuntimeError(msg)
            return value

        gmail_account = get_env_var_or_die("GMAIL_ACCOUNT")
        gmail_password = get_env_var_or_die("GMAIL_APP_PASSWORD")

        logger.info("Sending email")
        for santa_name, santee_name in name_mapping.mapping.items():
            santa = santas_by_name[santa_name]
            santee = santas_by_name[santee_name]
            _send_email(
                santa=santa,
                santee=santee,
                year=config["year"],
                sender=gmail_account,
                password=gmail_password,
                family_name=config["name"],
                budget=config["budget"],
                theme=config.get("theme"),
                debug_mode=debug_mode,
            )
            # Only send one email in debug mode
            if debug_mode:
                break
    else:
        logger.info("Not sending email")

    if output_dir:
        mapping_file = output_dir / f"mapping_{config['id']}_{config['year']}.json"
        logger.info(
            f"Saving {'encrypted ' if encrypt else ''}mapping to {mapping_file}",
        )
        if encrypt:
            key = Fernet.generate_key()
            fernet = Fernet(key)
        else:
            key = None
            fernet = None
        _o = {}
        _o["_fernet_key"] = key.decode("utf8") if key else None
        _o["_seed"] = seed
        _o["_year"] = config["year"]
        _o["_budget"] = config["budget"]
        _o["_name"] = config["name"]
        _o["_id"] = config["id"]
        for santa, santee in name_mapping.mapping.items():
            _o[santa] = fernet.encrypt(santee.encode()).decode() if fernet else santee
        with mapping_file.open("w") as f:
            json.dump(_o, f, indent=4, sort_keys=True, ensure_ascii=False)
