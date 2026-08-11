from rich.console import Console

from app.banner import mostrar_banner
from app.menu import mostrar_menu
from app.router import MenuRouter
from app.utils.logger import get_logger, setup_logging
from app.utils.system_status import mostrar_estado

console = Console()
logger = get_logger(__name__)


def main() -> None:
    """Arranca el bucle principal de OSINT LAB PRO."""

    setup_logging()
    router = MenuRouter()
    logger.info("OSINT LAB PRO iniciado")

    running = True

    while running:
        console.clear()
        mostrar_banner()
        mostrar_estado()

        opcion = mostrar_menu()
        running = router.dispatch(opcion)

    logger.info("OSINT LAB PRO finalizado")
