from rich.console import Console
from rich.table import Table

from app.config.settings import EXTERNAL_TOOLS
from app.ui.navigation import pausar
from app.utils.internet import internet_disponible
from app.utils.tool_manager import ToolManager

console = Console()


def menu_herramientas() -> None:
    """Muestra el estado de las herramientas OSINT integrables."""

    console.clear()

    tabla = Table(title="HERRAMIENTAS")
    tabla.add_column("Herramienta", style="cyan")
    tabla.add_column("Comando", style="green")
    tabla.add_column("Estado", justify="center")

    for nombre, comando in EXTERNAL_TOOLS.items():
        estado = "[green]OK[/green]" if ToolManager.existe(comando) else "[red]NO[/red]"
        tabla.add_row(nombre, comando, estado)

    estado_internet = "[green]OK[/green]" if internet_disponible() else "[red]NO[/red]"
    tabla.add_row("Internet", "-", estado_internet)

    console.print(tabla)
    pausar()
