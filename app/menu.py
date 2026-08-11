from rich.console import Console
from rich.table import Table

console = Console()


MENU_OPTIONS: tuple[tuple[str, str], ...] = (
    ("1", "Usuarios"),
    ("2", "Telefonos"),
    ("3", "Correos"),
    ("4", "Dominios"),
    ("5", "Metadatos"),
    ("6", "Redes Sociales"),
    ("7", "Herramientas"),
    ("8", "Casos"),
    ("9", "Informes"),
    ("10", "Configuracion"),
    ("0", "Salir"),
)


def mostrar_menu() -> str:
    """Muestra el menu principal y devuelve la opcion seleccionada."""

    tabla = Table(title="OSINT LAB PRO")

    tabla.add_column("Opción", style="cyan", justify="center")
    tabla.add_column("Descripción", style="green")

    for opcion, descripcion in MENU_OPTIONS:
        tabla.add_row(opcion, descripcion)

    console.print(tabla)

    return console.input("\n[bold yellow]Selecciona una opción > [/]")
