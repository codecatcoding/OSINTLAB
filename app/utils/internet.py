from urllib.request import urlopen


def internet_disponible(timeout: float = 3.0) -> bool:
    """Comprueba si hay conexion a Internet sin depender de ping."""

    try:
        with urlopen("https://www.google.com", timeout=timeout):
            return True
    except Exception:
        return False
