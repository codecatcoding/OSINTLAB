from rich.console import Console
from rich.table import Table

from app.ui.navigation import pausar
from app.utils.investigation_runner import run_tool_and_save
from app.utils.validators import is_username

console = Console()


def menu_redes_sociales() -> None:
    """Muestra el menu del modulo de redes sociales."""

    while True:
        console.clear()

        tabla = Table(title="REDES SOCIALES")
        tabla.add_column("Opcion", justify="center", style="cyan")
        tabla.add_column("Accion", style="green")
        tabla.add_row("1", "Buscar perfiles con Sherlock")
        tabla.add_row("2", "Buscar perfiles con Maigret")
        tabla.add_row("0", "Volver")

        console.print(tabla)

        opcion = console.input("\n[bold yellow]Selecciona una opcion > [/]").strip()

        if opcion == "0":
            break

        acciones = {
            "1": _sherlock_social,
            "2": _maigret_social,
        }
        accion = acciones.get(opcion)

        if accion is None:
            console.print("\n[bold red]Opcion no valida.[/bold red]")
            pausar()
            continue

        accion()


def _sherlock_social() -> None:
    usuario = _pedir_usuario()

    if usuario is None:
        return

    run_tool_and_save(
        tool_name="Sherlock",
        command=["sherlock", usuario, "--print-found"],
        target=usuario,
        title=f"social-sherlock-{usuario}",
        timeout=240,
    )


def _maigret_social() -> None:
    usuario = _pedir_usuario()

    if usuario is None:
        return

    run_tool_and_save(
        tool_name="Maigret",
        command=["maigret", usuario, "--no-color"],
        target=usuario,
        title=f"social-maigret-{usuario}",
        timeout=300,
    )


def _pedir_usuario() -> str | None:
    usuario = console.input("\nUsuario/perfil: ").strip()

    if not is_username(usuario):
        console.print(
            "\n[bold red]Usuario no valido. Usa letras, numeros, punto, guion o guion bajo.[/bold red]"
        )
        pausar()
        return None

    return usuario
