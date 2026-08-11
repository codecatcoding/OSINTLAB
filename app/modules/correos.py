from rich.console import Console
from rich.table import Table

from app.ui.navigation import pausar
from app.utils.investigation_runner import run_tool_and_save
from app.utils.validators import is_email

console = Console()


def menu_correos() -> None:
    """Muestra el menu del modulo de correos."""

    while True:
        console.clear()

        tabla = Table(title="INVESTIGACION DE CORREOS")
        tabla.add_column("Opcion", justify="center", style="cyan")
        tabla.add_column("Accion", style="green")
        tabla.add_row("1", "Buscar registros con Holehe")
        tabla.add_row("2", "Investigar dominio del correo con theHarvester")
        tabla.add_row("0", "Volver")

        console.print(tabla)

        opcion = console.input("\n[bold yellow]Selecciona una opcion > [/]").strip()

        if opcion == "0":
            break

        acciones = {
            "1": _buscar_holehe,
            "2": _investigar_dominio_correo,
        }
        accion = acciones.get(opcion)

        if accion is None:
            console.print("\n[bold red]Opcion no valida.[/bold red]")
            pausar()
            continue

        accion()


def _buscar_holehe() -> None:
    correo = _pedir_correo()

    if correo is None:
        return

    run_tool_and_save(
        tool_name="Holehe",
        command=["holehe", "--no-color", "--no-clear", "--only-used", correo],
        target=correo,
        title=f"holehe-{correo}",
        timeout=180,
    )


def _investigar_dominio_correo() -> None:
    correo = _pedir_correo()

    if correo is None:
        return

    dominio = correo.split("@", 1)[1]
    run_tool_and_save(
        tool_name="theHarvester",
        command=["theHarvester", "-d", dominio, "-b", "duckduckgo", "-l", "100", "-q"],
        target=dominio,
        title=f"theharvester-{dominio}",
        timeout=240,
    )


def _pedir_correo() -> str | None:
    correo = console.input("\nCorreo electronico: ").strip()

    if not is_email(correo):
        console.print("\n[bold red]Correo no valido.[/bold red]")
        pausar()
        return None

    return correo
