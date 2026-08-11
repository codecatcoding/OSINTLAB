import re
from pathlib import Path


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DOMAIN_PATTERN = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))+$"
)
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9()\s.-]{5,24}$")


def is_email(value: str) -> bool:
    """Valida un correo electronico."""

    return EMAIL_PATTERN.match(value.strip()) is not None


def is_domain(value: str) -> bool:
    """Valida un dominio."""

    return DOMAIN_PATTERN.match(value.strip()) is not None


def is_username(value: str) -> bool:
    """Valida un nombre de usuario compatible con herramientas OSINT."""

    return USERNAME_PATTERN.match(value.strip()) is not None


def is_phone(value: str) -> bool:
    """Valida un telefono en formato flexible."""

    return PHONE_PATTERN.match(value.strip()) is not None


def is_existing_file(value: str) -> bool:
    """Comprueba si el valor apunta a un archivo existente."""

    return Path(value).expanduser().is_file()
