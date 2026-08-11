from collections.abc import Callable
from dataclasses import dataclass

from rich.console import Console

from app.modules.casos import menu_casos
from app.modules.configuracion import menu_configuracion
from app.modules.correos import menu_correos
from app.modules.dominios import menu_dominios
from app.modules.herramientas import menu_herramientas
from app.modules.informes import menu_informes
from app.modules.metadatos import menu_metadatos
from app.modules.redes_sociales import menu_redes_sociales
from app.modules.telefonos import menu_telefonos
from app.modules.usuarios import menu_usuarios
from app.ui.navigation import pausar
from app.utils.logger import get_logger

console = Console()


@dataclass(frozen=True)
class MenuRoute:
    """Representa una ruta disponible en el menu principal."""

    option: str
    title: str
    handler: Callable[[], None] | None = None
    exits_app: bool = False


class MenuRouter:
    """Router central para evitar bloques if/elif en el menu principal."""

    def __init__(self) -> None:
        self.logger = get_logger(__name__)
        self.routes = self._build_routes()

    def dispatch(self, option: str) -> bool:
        """Ejecuta la ruta seleccionada y devuelve si la app debe continuar."""

        route = self.routes.get(option.strip())

        if route is None:
            console.print("\n[bold red]Opcion no valida.[/bold red]")
            pausar()
            return True

        if route.exits_app:
            console.print("\n[bold red]Cerrando OSINT LAB PRO...[/bold red]")
            return False

        if route.handler is None:
            console.print("\n[yellow]Ruta sin manejador configurado.[/yellow]")
            pausar()
            return True

        self.logger.info("Ejecutando modulo: %s", route.title)
        route.handler()
        return True

    @staticmethod
    def _build_routes() -> dict[str, MenuRoute]:
        return {
            "1": MenuRoute("1", "Usuarios", menu_usuarios),
            "2": MenuRoute("2", "Telefonos", menu_telefonos),
            "3": MenuRoute("3", "Correos", menu_correos),
            "4": MenuRoute("4", "Dominios", menu_dominios),
            "5": MenuRoute("5", "Metadatos", menu_metadatos),
            "6": MenuRoute("6", "Redes Sociales", menu_redes_sociales),
            "7": MenuRoute("7", "Herramientas", menu_herramientas),
            "8": MenuRoute("8", "Casos", menu_casos),
            "9": MenuRoute("9", "Informes", menu_informes),
            "10": MenuRoute("10", "Configuracion", menu_configuracion),
            "0": MenuRoute("0", "Salir", exits_app=True),
        }
