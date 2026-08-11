from collections.abc import Sequence

from rich.console import Console
from rich.panel import Panel

from app.ui.navigation import pausar
from app.utils.evidence_manager import EvidenceManager
from app.utils.tool_manager import ToolManager

console = Console()


def run_tool_and_save(
    *,
    tool_name: str,
    command: Sequence[str],
    target: str,
    title: str,
    case_id: str = "general",
    timeout: int = 180,
) -> None:
    """Ejecuta una herramienta OSINT y guarda su salida como evidencia."""

    if not ToolManager.existe(command[0]):
        console.print(f"\n[bold red]{tool_name} no esta disponible.[/bold red]")
        pausar()
        return

    console.print(f"\n[bold cyan]Ejecutando {tool_name} contra:[/bold cyan] {target}\n")

    result = ToolManager.ejecutar_captura(command, timeout=timeout)
    evidence_path = EvidenceManager().add_command_result(case_id, title, target, result)

    output = result.stdout.strip() or result.stderr.strip() or "Sin salida."
    preview = output[:3500]

    console.print(
        Panel(
            preview,
            title=f"{tool_name} | {'OK' if result.ok else 'ERROR'}",
            border_style="green" if result.ok else "red",
        )
    )
    console.print(f"\n[green]Evidencia guardada:[/green] {evidence_path}")
    pausar()
