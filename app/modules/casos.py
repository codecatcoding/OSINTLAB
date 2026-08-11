from rich.console import Console
from rich.table import Table

from app.ui.navigation import pausar
from app.utils.case_manager import CaseManager
from app.utils.evidence_manager import EvidenceManager

console = Console()


def menu_casos() -> None:
    """Muestra el menu del gestor de casos."""

    manager = CaseManager()
    evidence_manager = EvidenceManager()

    while True:
        console.clear()

        tabla = Table(title="GESTOR DE CASOS")
        tabla.add_column("Opcion", justify="center", style="cyan")
        tabla.add_column("Accion", style="green")
        tabla.add_row("1", "Listar casos")
        tabla.add_row("2", "Crear caso")
        tabla.add_row("3", "Crear carpeta de evidencias")
        tabla.add_row("0", "Volver")

        console.print(tabla)

        opcion = console.input("\n[bold yellow]Selecciona una opcion > [/]").strip()

        if opcion == "0":
            break

        acciones = {
            "1": lambda: _listar_casos(manager),
            "2": lambda: _crear_caso(manager),
            "3": lambda: _crear_carpeta_evidencias(evidence_manager),
        }
        accion = acciones.get(opcion)

        if accion is None:
            console.print("\n[bold red]Opcion no valida.[/bold red]")
            pausar()
            continue

        accion()


def _listar_casos(manager: CaseManager) -> None:
    cases = manager.list_cases()

    if not cases:
        console.print("\n[yellow]No hay casos registrados.[/yellow]")
        pausar()
        return

    tabla = Table(title="CASOS REGISTRADOS")
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Nombre", style="green")
    tabla.add_column("Estado")
    tabla.add_column("Creado")

    for case in cases:
        tabla.add_row(
            str(case.get("id", "")),
            str(case.get("name", "")),
            str(case.get("status", "")),
            str(case.get("created_at", "")),
        )

    console.print(tabla)
    pausar()


def _crear_caso(manager: CaseManager) -> None:
    nombre = console.input("\nNombre del caso: ").strip()

    if not nombre:
        console.print("\n[bold red]El nombre del caso no puede estar vacio.[/bold red]")
        pausar()
        return

    try:
        case = manager.create_case(nombre)
    except FileExistsError:
        console.print("\n[bold red]Ya existe un caso con ese identificador.[/bold red]")
        pausar()
        return

    EvidenceManager().create_evidence_folder(str(case["id"]))
    console.print(f"\n[green]Caso creado:[/green] {case['id']}")
    pausar()


def _crear_carpeta_evidencias(manager: EvidenceManager) -> None:
    case_id = console.input("\nID del caso: ").strip()

    if not case_id:
        console.print("\n[bold red]El ID del caso no puede estar vacio.[/bold red]")
        pausar()
        return

    path = manager.create_evidence_folder(case_id)
    console.print(f"\n[green]Carpeta lista:[/green] {path}")
    pausar()
