from rich.console import Console
from rich.table import Table

from app.ui.navigation import pausar
from app.utils.investigation_runner import run_tool_and_save
from app.utils.validators import is_phone

console = Console()


def menu_telefonos() -> None:
    """Muestra el menu del modulo de telefonos."""

    while True:
        console.clear()

        tabla = Table(title="INVESTIGACION DE TELEFONOS")
        tabla.add_column("Opcion", justify="center", style="cyan")
        tabla.add_column("Accion", style="green")
        tabla.add_row("1", "Analizar telefono con PhoneInfoga")
        tabla.add_row("0", "Volver")

        console.print(tabla)

        opcion = console.input("\n[bold yellow]Selecciona una opcion > [/]").strip()

        if opcion == "0":
            break

        acciones = {"1": _analizar_phoneinfoga}
        accion = acciones.get(opcion)

        if accion is None:
            console.print("\n[bold red]Opcion no valida.[/bold red]")
            pausar()
            continue

        accion()


def _analizar_phoneinfoga() -> None:
    telefono = console.input("\nTelefono en formato internacional recomendado (+34...): ").strip()

    if not is_phone(telefono):
        console.print("\n[bold red]Telefono no valido.[/bold red]")
        pausar()
        return

    run_tool_and_save(
        tool_name="PhoneInfoga",
        command=["phoneinfoga", "scan", "-n", telefono],
        target=telefono,
        title=f"phoneinfoga-{telefono}",
        timeout=180,
    )
