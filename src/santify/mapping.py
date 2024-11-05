# ruff: noqa: D100
import random
from dataclasses import dataclass

from santify.logging import logger

Constraint = tuple[str, str]


@dataclass(frozen=True)
class Person:
    """A person in the secret Santa game."""

    name: str
    email: str
    alias: str | None = None
    partner: str | None = None
    is_active: bool = True

    def __hash__(self) -> int:
        """Return the hash of the person."""
        return hash((self.name, self.email))


@dataclass
class Mapping:
    """A mapping of santas to santees."""

    year: int
    mapping: dict[str, str]

    def __repr__(self) -> str:
        """Return a string representation of the mapping.

        The output is a string with one line per mapping, with the format
        "santa -> santee".
        """
        output = ""
        n = max([len(k) for k in self.mapping])
        for k, v in self.mapping.items():
            output += f"{k.ljust(n)} -> {v}\n"
        return output


def get_active_santas(people: list[Person]) -> list[Person]:
    """Get all active santas."""
    return list(filter(lambda x: x.is_active, people))


def generate_partner_constraints(santas: list[Person]) -> list[Constraint]:
    """Generate constraints between santas and their partners."""
    santas_with_partners = filter(lambda x: x.partner, santas)
    return [(x.name, x.partner) for x in santas_with_partners]


def generate_constraints_from_past_mapping(
    past: Mapping,
    name_mapping: dict[str, str],
) -> list[Constraint]:
    """Generate constraints from a past mapping."""

    def _map_name(name: str) -> list[str]:
        output = name_mapping.get(name, name)
        if not isinstance(output, list):
            output = [output]
        return output

    return [
        (x, y)
        for santa, santee in past.mapping.items()
        for x in _map_name(santa)
        for y in _map_name(santee)
    ]


def generate_permutation(santa_names: list[str]) -> list[str]:
    """Generate a permutation of santas."""
    return random.sample(santa_names, len(santa_names))


def is_mapping(
    names: list[str],
    permutation: list[str],
    constraints: list[Constraint],
) -> bool:
    """Determine if a permutation is a valid mapping of santas to santees.

    Valid mapping needs to meet two sets of conditions:
    i) a santa cannot give to himself/herself
    ii) a santa cannot give to his/her significant other (constraints)
    iii) a santa cannot give to a person that was their santee during the previous years
    """
    n = len(names)

    if len(permutation) != n:
        msg = (
            "Names and permutation must have the same length "
            f"[{len(names)} != {len(permutation)}]"
        )
        raise RuntimeError(msg)

    for x, y in zip(names, permutation, strict=True):
        # check i) cannot give to self
        if x == y:
            return False
        # check ii) cannot give if there is a constraint
        if (x, y) in constraints:
            return False

    return True  # otherwise, valid


def generate_mapping(
    santas: list[Person],
    constraints: list[Constraint],
    year: int | None = None,
    max_iter: int = 10_000,
) -> list[str]:
    """Generate a mapping of santas to santees.

    Parameters
    ----------
    santas : list[Person]
        The list of santas.
    constraints : list[Constraint]
        The list of constraints.
    year : int, optional
        The year of the mapping.
        Default is None.
    max_iter : int, optional
        The maximum number of iterations to generate a valid mapping.
        Default is 10_000.

    Returns
    -------
    list[str]
        The generated mapping of santas to santees.

    Raises
    ------
    RuntimeError
        If the maximum number of iterations is reached and no valid mapping
        can be generated.

    """
    names = [x.name for x in santas]

    # initialize to identity
    permutation = names.copy()
    counter = 0

    # keep regenerating permutations until we get a valid mapping
    while not is_mapping(names, permutation, constraints):
        if counter > max_iter:
            msg = f"Failed to generate a mapping after {max_iter} iterations"
            logger.error(msg)
            raise RuntimeError(msg)

        permutation = generate_permutation(names)
        counter += 1

    msg = f"Valid mapping generated after {counter} attempts"
    logger.info(msg)

    mapping = dict(zip(names, permutation, strict=True))

    return Mapping(year=year, mapping=mapping)
