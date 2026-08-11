from rich.console import Console
from rich.table import Table

from app.ui.navigation import pausar
from app.utils.report_manager import ReportManager

console = Console()


def menu_informes() -> None:
    """Muestra el menu del gestor de informes."""

    manager = ReportManager()

    while True:
        console.clear()

        tabla = Table(title="GESTOR DE INFORMES")
        tabla.add_column("Opcion", justify="center", style="cyan")
        tabla.add_column("Accion", style="green")
        tabla.add_row("1", "Listar informes")
        tabla.add_row("2", "Crear informe basico")
        tabla.add_row("3", "Crear informe desde evidencias")
        tabla.add_row("0", "Volver")

        console.print(tabla)

        opcion = console.input("\n[bold yellow]Selecciona una opcion > [/]").strip()

        if opcion == "0":
            break

        acciones = {
            "1": lambda: _listar_informes(manager),
            "2": lambda: _crear_informe(manager),
            "3": lambda: _crear_informe_evidencias(manager),
        }
        accion = acciones.get(opcion)

        if accion is None:
            console.print("\n[bold red]Opcion no valida.[/bold red]")
            pausar()
            continue

        accion()


def _listar_informes(manager: ReportManager) -> None:
    reports = manager.list_reports()

    if not reports:
        console.print("\n[yellow]No hay informes registrados.[/yellow]")
        pausar()
        return

    tabla = Table(title="INFORMES")
    tabla.add_column("Archivo", style="cyan")
    tabla.add_column("Ruta", style="green")

    for report in reports:
        tabla.add_row(report.name, str(report))

    console.print(tabla)
    pausar()


def _crear_informe(manager: ReportManager) -> None:
    case_id = console.input("\nID del caso: ").strip()
    title = console.input("Titulo del informe: ").strip()

    if not case_id or not title:
        console.print("\n[bold red]Caso y titulo son obligatorios.[/bold red]")
        pausar()
        return

    report_path = manager.create_basic_report(case_id, title)
    console.print(f"\n[green]Informe creado:[/green] {report_path}")
    pausar()


def _crear_informe_evidencias(manager: ReportManager) -> None:
    case_id = console.input("\nID del caso o ENTER para general: ").strip() or "general"
    title = console.input("Titulo del informe: ").strip()

    if not title:
        console.print("\n[bold red]El titulo es obligatorio.[/bold red]")
        pausar()
        return

    report_path = manager.create_report_from_evidence(case_id, title)
    console.print(f"\n[green]Informe desde evidencias creado:[/green] {report_path}")
    pausar()
