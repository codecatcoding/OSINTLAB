from rich.console import Console
from rich.table import Table

from app.ui.navigation import pausar
from app.utils.config_manager import ConfigManager

console = Console()


def menu_configuracion() -> None:
    """Muestra la configuracion actual del proyecto."""

    console.clear()

    manager = ConfigManager()
    config = manager.load()

    tabla = Table(title="CONFIGURACION")
    tabla.add_column("Clave", style="cyan")
    tabla.add_column("Valor", style="green")

    for key, value in sorted(config.items()):
        tabla.add_row(str(key), str(value))

    console.print(tabla)
    pausar()
