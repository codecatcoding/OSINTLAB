from rich.console import Console
from rich.table import Table

from app.config.settings import EXTERNAL_TOOLS
from app.utils.internet import internet_disponible
from app.utils.tool_manager import ToolManager

console = Console()


def mostrar_estado() -> None:
    """Muestra el estado de herramientas clave del laboratorio."""

    tabla = Table(title="Estado del laboratorio")

    tabla.add_column("Herramienta")
    tabla.add_column("Estado")

    for nombre, comando in EXTERNAL_TOOLS.items():
        estado = ToolManager.existe(comando)

        if estado:
            tabla.add_row(nombre, "[green]OK[/green]")
        else:
            tabla.add_row(nombre, "[red]NO[/red]")

    if internet_disponible():
        tabla.add_row("Internet", "[green]OK[/green]")
    else:
        tabla.add_row("Internet", "[red]NO[/red]")

    console.print(tabla)
