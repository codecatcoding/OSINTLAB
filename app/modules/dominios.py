from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.ui.navigation import pausar
from app.utils.dns_lookup import resolve_domain
from app.utils.evidence_manager import EvidenceManager
from app.utils.investigation_runner import run_tool_and_save
from app.utils.validators import is_domain

console = Console()


def menu_dominios() -> None:
    """Muestra el menu del modulo de dominios."""

    while True:
        console.clear()

        tabla = Table(title="INVESTIGACION DE DOMINIOS")
        tabla.add_column("Opcion", justify="center", style="cyan")
        tabla.add_column("Accion", style="green")
        tabla.add_row("1", "Resolver DNS basico")
        tabla.add_row("2", "Recolectar OSINT con theHarvester")
        tabla.add_row("3", "Escaneo pasivo con SpiderFoot")
        tabla.add_row("0", "Volver")

        console.print(tabla)

        opcion = console.input("\n[bold yellow]Selecciona una opcion > [/]").strip()

        if opcion == "0":
            break

        acciones = {
            "1": _resolver_dns_basico,
            "2": _theharvester,
            "3": _spiderfoot_pasivo,
        }
        accion = acciones.get(opcion)

        if accion is None:
            console.print("\n[bold red]Opcion no valida.[/bold red]")
            pausar()
            continue

        accion()


def _resolver_dns_basico() -> None:
    dominio = _pedir_dominio()

    if dominio is None:
        return

    addresses, error_text = resolve_domain(dominio)

    lines = [f"# Resolucion DNS basica: {dominio}", ""]
    lines.extend(f"- {address}" for address in addresses)

    if error_text:
        lines.extend(["", "## Error", "", error_text])

    evidence_path = EvidenceManager().add_note(
        "general",
        f"dns-basico-{dominio}",
        "\n".join(lines),
    )

    output = "\n".join(addresses) if addresses else error_text or "Sin resultados."
    console.print(Panel(output, title="DNS basico", border_style="green" if addresses else "red"))
    console.print(f"\n[green]Evidencia guardada:[/green] {evidence_path}")
    pausar()


def _theharvester() -> None:
    dominio = _pedir_dominio()

    if dominio is None:
        return

    run_tool_and_save(
        tool_name="theHarvester",
        command=["theHarvester", "-d", dominio, "-b", "duckduckgo", "-l", "100", "-q"],
        target=dominio,
        title=f"theharvester-{dominio}",
        timeout=240,
    )


def _spiderfoot_pasivo() -> None:
    dominio = _pedir_dominio()

    if dominio is None:
        return

    run_tool_and_save(
        tool_name="SpiderFoot",
        command=["spiderfoot", "-s", dominio, "-u", "passive", "-o", "tab", "-q"],
        target=dominio,
        title=f"spiderfoot-passive-{dominio}",
        timeout=300,
    )


def _pedir_dominio() -> str | None:
    dominio = console.input("\nDominio: ").strip().lower()

    if not is_domain(dominio):
        console.print("\n[bold red]Dominio no valido.[/bold red]")
        pausar()
        return None

    return dominio
