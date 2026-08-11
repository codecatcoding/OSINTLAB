from rich.console import Console
from rich.table import Table

from app.ui.navigation import pausar
from app.utils.investigation_runner import run_tool_and_save
from app.utils.validators import is_username

console = Console()


def menu_usuarios() -> None:
    """Muestra el menu del modulo de usuarios."""

    while True:
        console.clear()

        tabla = Table(title="INVESTIGACIÓN DE USUARIOS")

        tabla.add_column("Opción", justify="center", style="cyan")
        tabla.add_column("Acción", style="green")

        tabla.add_row("1", "Buscar usuario con Sherlock")
        tabla.add_row("2", "Buscar usuario con Maigret")
        tabla.add_row("3", "Busqueda combinada Sherlock + Maigret")
        tabla.add_row("0", "Volver")

        console.print(tabla)

        opcion = console.input("\n[bold yellow]Selecciona una opción > [/]")

        if opcion == "0":
            break

        acciones = {
            "1": _buscar_con_sherlock,
            "2": _buscar_con_maigret,
            "3": _busqueda_combinada,
        }
        accion = acciones.get(opcion)

        if accion is None:
            console.print("\n[yellow]Opcion todavia no implementada.[/yellow]")
            pausar("\nPulsa ENTER...")
            continue

        accion()


def _buscar_con_sherlock() -> None:
    usuario = _pedir_usuario()

    if usuario is None:
        return

    run_tool_and_save(
        tool_name="Sherlock",
        command=["sherlock", usuario, "--print-found"],
        target=usuario,
        title=f"sherlock-{usuario}",
        timeout=240,
    )


def _buscar_con_maigret() -> None:
    usuario = _pedir_usuario()

    if usuario is None:
        return

    run_tool_and_save(
        tool_name="Maigret",
        command=["maigret", usuario, "--no-color"],
        target=usuario,
        title=f"maigret-{usuario}",
        timeout=300,
    )


def _busqueda_combinada() -> None:
    usuario = _pedir_usuario()

    if usuario is None:
        return

    run_tool_and_save(
        tool_name="Sherlock",
        command=["sherlock", usuario, "--print-found"],
        target=usuario,
        title=f"sherlock-{usuario}",
        timeout=240,
    )
    run_tool_and_save(
        tool_name="Maigret",
        command=["maigret", usuario, "--no-color"],
        target=usuario,
        title=f"maigret-{usuario}",
        timeout=300,
    )


def _pedir_usuario() -> str | None:
    usuario = console.input("\nNombre de usuario: ").strip()

    if not is_username(usuario):
        console.print(
            "\n[bold red]Usuario no valido. Usa letras, numeros, punto, guion o guion bajo.[/bold red]"
        )
        pausar()
        return None

    return usuario
